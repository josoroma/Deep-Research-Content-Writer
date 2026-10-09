"""Adaptive evidence contracts, document envelopes, and durable attempt budgets."""

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest
from langchain_core.messages import AIMessage, BaseMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from pydantic import HttpUrl, ValidationError

from application.job_service import normalize_payload, request_hash
from evaluations.authoring_fixtures import fixture_draft, fixture_plan
from evaluations.fakes import ScriptedChatModel
from evaluations.judge import ModelJudge
from evaluations.scoring import coverage, factual_claims
from schemas.api import SubmissionRequest
from schemas.authoring import DiagramPlan, Evidence, Synthesis
from schemas.config import RunSettings
from schemas.errors import AuthoringError
from schemas.requests import ResearchRequest
from schemas.responses import SearchResult, Source
from schemas.state import RunState, UrlOutcome
from schemas.tool_io import ValidateSynthesisOutput
from services.artifacts import write_json, write_text
from services.authoring import check_blog, check_summary, validate_citations
from services.authoring_pipeline import Stage, StageInvoker
from services.content_paths import content_path
from services.corpus import CorpusSource, write_index, write_source
from services.diagrams import validate_diagrams
from services.document_finalizer import document_violations, finalize_document
from services.llm_service import LLMService
from services.markdown_document import content_text, headings
from services.source_backend import ImmutableSourceBackend
from services.synthesis import (
    SYNTHESIS_PATH,
    authoring_state,
    commit_synthesis,
    file_fingerprint,
    save_authoring_state,
    saved_request,
    validate_synthesis,
)
from services.workspace import create_run_workspace
from tools.authoring_tools import AuthoringSession
from tools.registry import create_tool_registry
from workflows.authoring_run import run_authoring
from workflows.search_run import tool_runtime


def corpus(root: Path, *, goal: str | None = None) -> Path:
    request = ResearchRequest(topic="Framework deployment choices", goal=goal, max_urls=2)
    workspace = create_run_workspace(request, root)
    bodies = [
        "Framework A supports local deployment. Its measurements use version 1. "
        "These results cannot establish performance across different workloads.",
        "Framework B requires a hosted service. Its measurements use version 2. "
        "The two sources do not establish a performance ranking.",
    ]
    records = []
    for rank, body in enumerate(bodies, 1):
        record = CorpusSource(
            source=Source(
                source_id=f"S-{rank:02d}",
                url=HttpUrl(f"https://example.com/{rank}"),
                title=f"Deployment evidence {rank}",
                author=None,
                published=None,
                fetched_at=datetime(2026, 10, 9, tzinfo=UTC),
                body_markdown=body,
                word_count=len(body.split()),
            ),
            path=f"research/{rank:03d}_evidence.md",
            rank=rank,
        )
        write_source(workspace.root, record)
        records.append(record)
    write_index(workspace.root, records)
    results = [
        SearchResult(
            url=item.source.url,
            title=item.source.title,
            snippet="Evidence",
            rank=item.rank,
            query=request.topic,
        )
        for item in records
    ]
    run = RunState(
        run_id=workspace.run_id,
        topic=request.topic,
        completed_phases=["plan", "search", "normalize", "fetch", "index"],
        clean_results=results,
        url_outcomes={
            str(item.url): UrlOutcome(
                rank=item.rank, url=item.url, outcome="extracted", source_id=f"S-{item.rank:02d}"
            )
            for item in results
        },
    )
    write_json(workspace.root / "corpus_state.json", run.model_dump(mode="json"))
    return workspace.root


def settings() -> RunSettings:
    return RunSettings(_env_file=None)


def persist_plan(root: Path, plan: Synthesis) -> None:
    write_json(root / SYNTHESIS_PATH, plan.model_dump(mode="json"))


def invocation(
    root: Path, plan: Synthesis, calls: list[str], *, unknown: bool = False
) -> StageInvoker:
    def invoke(stage: Stage, prompt: str, run: RunState) -> None:
        calls.append(stage)
        assert run.run_id == root.name
        if stage == "synthesize":
            assert plan.input_fingerprint in prompt
            persist_plan(root, plan)
        elif stage == "write":
            assert check_summary(root).passed
            assert authoring_state(root).generation == "in_progress"
            if plan.goal:
                assert plan.goal in prompt
            text = fixture_draft(plan, words_per_section=700)
            if unknown:
                text = text.replace("[S-01]", "[S-99]", 1)
            write_text(root / content_path(root), text)
        else:
            assert authoring_state(root).repair_in_progress
            path = root / content_path(root)
            write_text(path, path.read_text().replace("[S-99]", "[S-01]"))

    return invoke


@pytest.mark.parametrize("value", [None, "", " \n "])
def test_goal_blank_normalizes_and_preserves_legacy_hash(value: str | None) -> None:
    plain = SubmissionRequest(topic="A research topic")
    supplied = SubmissionRequest(topic="A research topic", goal=value)
    assert supplied.to_research_request().goal is None
    assert normalize_payload(plain) == normalize_payload(supplied)
    assert "goal" not in normalize_payload(supplied)


@pytest.mark.parametrize("value", [True, 3, [], "x" * 1001])
def test_goal_rejects_invalid_inputs(value: object) -> None:
    with pytest.raises(ValidationError):
        ResearchRequest.model_validate({"topic": "A research topic", "goal": value})


def test_goal_trimming_and_idempotency() -> None:
    first = normalize_payload(SubmissionRequest(topic="A research topic", goal=" Choose a tool "))
    second = normalize_payload(SubmissionRequest(topic="A research topic", goal="Choose a tool"))
    other = normalize_payload(
        SubmissionRequest(topic="A research topic", goal="Learn the mechanism")
    )
    assert request_hash(first) == request_hash(second)
    assert request_hash(first) != request_hash(other)


@pytest.mark.parametrize(
    "label,titles,goal",
    [
        (
            "Qualified comparison",
            ("Decision criteria", "What is comparable", "Unknowns"),
            "Choose a framework",
        ),
        (
            "Conceptual tutorial",
            ("Prerequisites", "Understand execution", "Limits of this guide"),
            "Learn execution",
        ),
        ("Literature review", ("Review method", "Published findings", "Review limitations"), None),
    ],
)
def test_custom_format_handoff_and_complete_document(
    tmp_path: Path,
    label: str,
    titles: tuple[str, ...],
    goal: str | None,
) -> None:
    root = corpus(tmp_path, goal=goal)
    plan = fixture_plan(root, label=label, titles=titles)
    calls: list[str] = []
    source_before = file_fingerprint(root / "research/001_evidence.md")
    result = run_authoring(root, settings(), invoke=invocation(root, plan, calls))
    assert result.status == "completed", result
    assert calls == ["synthesize", "write"]
    assert result.format_label == label
    text = (root / content_path(root)).read_text()
    found = headings(text)
    assert [item.title for item in found][1:2] == ["Table of contents"]
    assert [item.title for item in found][2:-2] == list(titles)
    assert [item.title for item in found][-2:] == ["References", "Why this format"]
    assert not document_violations(text, plan)
    assert validate_citations(root).passed and check_summary(root).passed
    assert file_fingerprint(root / "research/001_evidence.md") == source_before
    assert saved_request(root).goal == goal
    assert authoring_state(root).generation == "completed"
    assert authoring_state(root).synthesis_completed
    second = run_authoring(root, settings(), invoke=invocation(root, plan, calls))
    assert second.status == "completed" and calls == ["synthesize", "write"]
    assert (root / content_path(root)).read_text() == text


def test_nested_and_repeated_unicode_headings_ignore_code(tmp_path: Path) -> None:
    root = corpus(tmp_path)
    plan = fixture_plan(root, titles=("Café: **evidence**", "Café evidence", "Café evidence"))
    plan.outline[0].title = "Café evidence"
    plan.outline[1].level = 3
    plan.outline[2].level = 3
    persist_plan(root, plan)
    commit_synthesis(root)
    text = fixture_draft(plan) + ""
    text = text.replace(
        "## Why this format",
        "```python\n# Not a title\n## Not a section\n```\n\n## Why this format",
    )
    write_text(root / content_path(root), text)
    finalize_document(root, plan)
    final = (root / content_path(root)).read_text()
    assert check_blog(root).headings_valid
    assert "(#café-evidence-1)" in final and "(#café-evidence-2)" in final
    assert "Not a section" not in [item.title for item in headings(final)]


def test_synthesis_retry_and_invalid_excerpt_blocks_writing(tmp_path: Path) -> None:
    root = corpus(tmp_path)
    plan = fixture_plan(root)
    calls: list[str] = []

    def invoke(stage: Stage, prompt: str, run: RunState) -> None:
        calls.append(stage)
        invalid = plan.model_copy(deep=True)
        invalid.findings[0].evidence[0].excerpt = "This passage was never collected."
        persist_plan(root, invalid)

    result = run_authoring(root, settings(), invoke=invoke)
    assert result.reason == "synthesis_invalid"
    assert calls == ["synthesize", "synthesize"]
    assert not (root / content_path(root)).exists()
    assert authoring_state(root).synthesis_attempts == 2
    run_authoring(root, settings(), invoke=invoke)
    assert len(calls) == 2


@pytest.mark.parametrize("resumed", [False, True])
def test_synthesis_retry_identifies_invalid_evidence_and_can_correct_it(
    tmp_path: Path, resumed: bool
) -> None:
    root = corpus(tmp_path)
    plan = fixture_plan(root)
    invalid = plan.model_copy(deep=True)
    finding = invalid.findings[0]
    finding.evidence[0].excerpt = "This passage was never collected."
    other = invalid.findings[1]
    other.evidence[0].excerpt = "Another passage that was never collected."
    calls: list[str] = []
    normal = invocation(root, plan, calls)
    if resumed:
        persist_plan(root, invalid)
        state = authoring_state(root)
        state.synthesis_attempts = 1
        save_authoring_state(root, state)

    def invoke(stage: Stage, prompt: str, run: RunState) -> None:
        if stage == "synthesize" and not resumed and not calls:
            calls.append(stage)
            persist_plan(root, invalid)
            return
        if stage == "synthesize":
            assert "Previous attempt failed validation" in prompt
            assert finding.finding_id in prompt
            assert finding.evidence[0].source_id in prompt
            assert other.finding_id in prompt
            assert other.evidence[0].source_id in prompt
            assert "Markdown, whitespace, and punctuation" in prompt
        normal(stage, prompt, run)

    result = run_authoring(root, settings(), invoke=invoke)
    assert result.status == "completed"
    assert authoring_state(root).synthesis_attempts == 2
    assert calls.count("write") == 1
    assert validate_citations(root).passed


def test_synthesis_retry_does_not_forward_untrusted_exception_details(tmp_path: Path) -> None:
    root = corpus(tmp_path)
    plan = fixture_plan(root)
    calls: list[str] = []
    normal = invocation(root, plan, calls)

    def invoke(stage: Stage, prompt: str, run: RunState) -> None:
        if not calls:
            calls.append(stage)
            raise RuntimeError("Provider response containing private credentials")
        if stage == "synthesize":
            assert "RuntimeError" in prompt
            assert "private credentials" not in prompt
        normal(stage, prompt, run)

    result = run_authoring(root, settings(), invoke=invoke)
    assert result.status == "completed"
    assert authoring_state(root).synthesis_attempts == 2


def test_synthesis_retry_receives_schema_validation_location_and_requirement(
    tmp_path: Path,
) -> None:
    root = corpus(tmp_path)
    plan = fixture_plan(root)
    invalid = plan.model_dump(mode="json")
    for evidence in invalid["findings"][0]["evidence"]:
        evidence["role"] = "qualifies"
    calls: list[str] = []
    normal = invocation(root, plan, calls)

    def invoke(stage: Stage, prompt: str, run: RunState) -> None:
        if not calls:
            calls.append(stage)
            write_json(root / SYNTHESIS_PATH, invalid)
            return
        if stage == "synthesize":
            assert "findings.0" in prompt
            assert "Every finding needs supporting evidence" in prompt
        normal(stage, prompt, run)

    result = run_authoring(root, settings(), invoke=invoke)
    assert result.status == "completed"
    assert authoring_state(root).synthesis_attempts == 2


def test_unknown_source_and_invalid_outline_rejected(tmp_path: Path) -> None:
    root = corpus(tmp_path)
    plan = fixture_plan(root)
    plan.findings[0].evidence[0].source_id = "S-99"
    persist_plan(root, plan)
    with pytest.raises(AuthoringError):
        validate_synthesis(root)
    data = fixture_plan(root).model_dump(mode="json")
    data["outline"][0]["finding_ids"] = ["unknown"]
    with pytest.raises(ValidationError):
        Synthesis.model_validate(data)


def test_analyst_validation_tool_reports_errors_without_mutating_workspace(tmp_path: Path) -> None:
    root = corpus(tmp_path)
    plan = fixture_plan(root)
    plan.findings[0].evidence[0].excerpt = "This passage was never collected."
    persist_plan(root, plan)
    run = RunState.model_validate_json((root / "corpus_state.json").read_text())
    registry = create_tool_registry(authoring_session=AuthoringSession(root, run))
    before = {str(p.relative_to(root)): p.read_bytes() for p in root.rglob("*") if p.is_file()}
    rejected = registry["validate_synthesis"].invoke({}, tool_runtime(run))
    assert isinstance(rejected, ValidateSynthesisOutput)
    assert not rejected.passed
    assert plan.findings[0].finding_id in rejected.errors[0]
    assert plan.findings[0].evidence[0].source_id in rejected.errors[0]
    after = {str(p.relative_to(root)): p.read_bytes() for p in root.rglob("*") if p.is_file()}
    assert before == after
    persist_plan(root, fixture_plan(root))
    # Child agents need only the workspace binding, without the parent's run state.
    accepted = registry["validate_synthesis"].invoke({})
    assert isinstance(accepted, ValidateSynthesisOutput)
    assert accepted.passed and not accepted.errors
    assert authoring_state(root).synthesis_attempts == 0


def test_checkpointed_authoring_isolates_synthesis_from_writing(tmp_path: Path) -> None:
    root = corpus(tmp_path)
    plan = fixture_plan(root)
    writer_inputs: list[list[str]] = []

    def call(name: str, args: dict[str, object], number: int) -> AIMessage:
        return AIMessage(
            content="", tool_calls=[{"name": name, "args": args, "id": f"step-{number}"}]
        )

    def on_call(tools: list[str], messages: list[BaseMessage]) -> None:
        human = [str(message.content) for message in messages if message.type == "human"]
        if any(item.startswith("Run only Write.") for item in human):
            writer_inputs.append(human)

    fake = ScriptedChatModel(
        script=[
            call("task", {"subagent_type": "analyst_agent", "description": "Synthesize"}, 1),
            call(
                "write_file",
                {
                    "file_path": "/research/synthesis.json",
                    "content": json.dumps(plan.model_dump(mode="json")),
                },
                2,
            ),
            call("validate_synthesis", {}, 3),
            AIMessage(content="research/synthesis.json"),
            call("validate_synthesis", {}, 4),
            AIMessage(content="research/synthesis.json"),
            call("task", {"subagent_type": "writer_agent", "description": "Write"}, 5),
            call(
                "write_file",
                {
                    "file_path": "/" + content_path(root),
                    "content": fixture_draft(plan, words_per_section=700),
                },
                6,
            ),
            AIMessage(content=content_path(root)),
            AIMessage(content=content_path(root)),
        ],
        on_call=on_call,
    )
    with SqliteSaver.from_conn_string(str(root / "checkpoints.sqlite")) as saver:
        result = run_authoring(
            root, settings(), llm=LLMService(settings(), fake_model=fake), checkpointer=saver
        )
        assert saver.get_tuple({"configurable": {"thread_id": f"{root.name}:synthesize:1"}})
        assert saver.get_tuple({"configurable": {"thread_id": f"{root.name}:write:1"}})
    assert result.status == "completed"
    assert validate_citations(root).passed
    assert writer_inputs
    assert all(
        not any(text.startswith("Run only Synthesize.") for text in m) for m in writer_inputs
    )
    assert authoring_state(root).synthesis_attempts == 1
    assert authoring_state(root).generation == "completed"


def test_conflicting_evidence_and_qualifications_are_retained(tmp_path: Path) -> None:
    root = corpus(tmp_path)
    plan = fixture_plan(root)
    plan.findings[0].evidence.append(
        Evidence(
            source_id="S-02",
            role="contradicts",
            excerpt="The two sources do not establish a performance ranking.",
        )
    )
    plan.findings[0].qualifications.append("Measurements use different versions and workloads.")
    persist_plan(root, plan)
    commit_synthesis(root)
    summary = (root / "research/summary.md").read_text()
    assert "contradicts" in summary and "different versions" in summary and "[S-02]" in summary


def test_rationale_citations_in_references_and_toc_rebuilt(tmp_path: Path) -> None:
    root = corpus(tmp_path)
    plan = fixture_plan(root, titles=("Evidence",))
    plan.closing_rationale = "The sources use different versions [S-02]."
    persist_plan(root, plan)
    write_text(root / content_path(root), "# Findings\n\n## Evidence\n\nLocal deployment [S-01].\n")
    finalize_document(root, plan)
    text = (root / content_path(root)).read_text()
    assert "- [S-02] Deployment evidence 2" in text
    assert "[Why this format](#why-this-format)" in text
    assert validate_citations(root).passed
    write_text(
        root / content_path(root),
        text.replace("## Why this format", "## Appendix\n\nextra\n\n## Why this format"),
    )
    assert not check_blog(root).headings_valid


def test_reserved_generation_is_not_repeated(tmp_path: Path) -> None:
    root = corpus(tmp_path)
    plan = fixture_plan(root)
    calls: list[str] = []
    state = authoring_state(root)
    state.generation = "in_progress"
    save_authoring_state(root, state)
    result = run_authoring(root, settings(), invoke=invocation(root, plan, calls))
    assert result.reason == "authoring_interrupted"
    assert calls == ["synthesize"]


def test_completed_draft_after_interruption_is_reconciled(tmp_path: Path) -> None:
    root = corpus(tmp_path)
    plan = fixture_plan(root)
    calls: list[str] = []

    def interrupted(stage: Stage, prompt: str, run: RunState) -> None:
        invocation(root, plan, calls)(stage, prompt, run)
        if stage == "write":
            raise RuntimeError("after writing, before acknowledgement")

    assert run_authoring(root, settings(), invoke=interrupted).status == "failed"
    result = run_authoring(root, settings(), invoke=invocation(root, plan, calls))
    assert result.status == "completed"
    assert calls == ["synthesize", "write"]


def test_citation_repairs_are_persisted_and_limited(tmp_path: Path) -> None:
    root = corpus(tmp_path)
    plan = fixture_plan(root)
    calls: list[str] = []
    callback = invocation(root, plan, calls, unknown=True)

    def no_repair(stage: Stage, prompt: str, run: RunState) -> None:
        if stage == "repair":
            calls.append(stage)
        else:
            callback(stage, prompt, run)

    result = run_authoring(root, settings(), invoke=no_repair)
    assert result.reason == "dangling_citations" and result.repair_passes == 2
    assert calls == ["synthesize", "write", "repair", "repair"]
    second = run_authoring(root, settings(), invoke=no_repair)
    assert second.reason == "dangling_citations" and len(calls) == 4


def test_citation_repair_success_rebuilds_navigation(tmp_path: Path) -> None:
    root = corpus(tmp_path)
    plan = fixture_plan(root)
    calls: list[str] = []
    result = run_authoring(root, settings(), invoke=invocation(root, plan, calls, unknown=True))
    assert result.status == "completed" and result.repair_passes == 1
    assert validate_citations(root).passed


def test_changed_inputs_and_malformed_marker_never_fall_back(tmp_path: Path) -> None:
    root = corpus(tmp_path)
    plan = fixture_plan(root)
    calls: list[str] = []
    run_authoring(root, settings(), invoke=invocation(root, plan, calls))
    request = saved_request(root)
    request.goal = "A different objective"
    write_json(root / "request.json", request.model_dump(mode="json"))
    assert (
        run_authoring(root, settings(), invoke=invocation(root, plan, calls)).reason
        == "synthesis_invalid"
    )
    write_text(root / "output/authoring_state.json", "{invalid")
    with pytest.raises(AuthoringError):
        authoring_state(root)
    previous_calls = calls.copy()
    result = run_authoring(root, settings(), invoke=invocation(root, plan, calls))
    assert result.status == "failed" and result.reason == "synthesis_invalid"
    assert result.blog_path == content_path(root)
    assert (root / "output/authoring.json").is_file()
    assert calls == previous_calls
    assert (root / "output/authoring_state.json").read_text() == "{invalid"


def test_missing_synthesis_never_reverts_to_legacy(tmp_path: Path) -> None:
    root = corpus(tmp_path)
    write_text(root / content_path(root), "# Title\n\n## Introduction\n\nLegacy-looking text.")
    assert not check_blog(root).headings_valid
    assert check_blog(root).violations == ["synthesis_invalid"]


def test_agent_cannot_reset_coordinator_attempt_reservations(tmp_path: Path) -> None:
    root = corpus(tmp_path)
    backend = ImmutableSourceBackend(root_dir=root, virtual_mode=True)
    path = "/output/authoring_state.json"
    before = (root / path.lstrip("/")).read_bytes()
    assert backend.write(path, '{"contract_version": 1}').error
    assert backend.edit(path, '"contract_version": 2', '"contract_version": 1').error
    assert backend.delete(path).error
    assert (root / path.lstrip("/")).read_bytes() == before


def test_reference_only_ids_do_not_inflate_coverage_or_claims(tmp_path: Path) -> None:
    root = corpus(tmp_path)
    write_text(
        root / content_path(root),
        "# Title\n\n## Table of contents\n\n[S-02]\n\n"
        "## Evidence\n\nFramework A supports local deployment [S-01].\n\n"
        "## References\n\n- [S-02] Deployment evidence 2 https://example.com/2\n",
    )
    assert coverage(root) == 0.5
    claims = factual_claims(root)
    assert len(claims) == 1
    assert claims[0].source_ids == ["S-01"]
    assert "version 1" in claims[0].source_excerpts["S-01"]
    assert "References" not in content_text((root / content_path(root)).read_text())


def test_source_aware_judge_receives_actual_contradicting_passages(tmp_path: Path) -> None:
    root = corpus(tmp_path)
    write_text(
        root / content_path(root),
        "# Findings\n\n## Evidence\n\nFramework A requires hosted deployment [S-01] [S-02].\n",
    )
    claims = factual_claims(root)
    captured: list[str] = []

    def capture(tools: list[str], messages: list[BaseMessage]) -> None:
        captured.extend(str(item.content) for item in messages)

    model = ScriptedChatModel(
        script=[
            AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "Verdicts",
                        "args": {"verdicts": [{"index": 0, "supported": False}]},
                        "id": "judge",
                        "type": "tool_call",
                    }
                ],
            )
        ],
        on_call=capture,
    )
    judged = ModelJudge(settings(), model=model).judge(claims)
    assert not judged[0].supported
    assert set(claims[0].source_excerpts) == {"S-01", "S-02"}
    assert "supports local deployment" in "\n".join(captured)
    assert "do not establish a performance ranking" in "\n".join(captured)


def test_interrupted_repair_does_not_repeat_the_reserved_attempt(tmp_path: Path) -> None:
    root = corpus(tmp_path)
    plan = fixture_plan(root)
    calls: list[str] = []
    callback = invocation(root, plan, calls, unknown=True)

    def interrupt(stage: Stage, prompt: str, run: RunState) -> None:
        if stage == "repair":
            calls.append(stage)
            raise RuntimeError("interrupted before edit")
        callback(stage, prompt, run)

    assert run_authoring(root, settings(), invoke=interrupt).status == "failed"
    assert authoring_state(root).repair_passes == 1
    result = run_authoring(root, settings(), invoke=callback)
    assert result.reason == "authoring_interrupted"
    assert calls == ["synthesize", "write", "repair"]


def test_short_adaptive_draft_is_preserved_and_records_length(tmp_path: Path) -> None:
    root = corpus(tmp_path)
    plan = fixture_plan(root)

    def invoke(stage: Stage, prompt: str, run: RunState) -> None:
        if stage == "synthesize":
            persist_plan(root, plan)
        elif stage == "write":
            write_text(root / content_path(root), fixture_draft(plan, words_per_section=10))

    result = run_authoring(root, settings(), invoke=invoke)
    assert result.status == "completed" and result.reason == "blog_length"
    assert check_blog(root).word_count < 2000


@pytest.mark.parametrize(
    "kind,code",
    [
        ("flowchart", "flowchart TD\nA[Read sources] --> B[Assess evidence]"),
        (
            "sequenceDiagram",
            "sequenceDiagram\nReader->>Analyst: Review evidence\nAnalyst-->>Reader: Explain limits",
        ),
    ],
)
def test_supported_mermaid_diagrams_really_render(tmp_path: Path, kind: str, code: str) -> None:
    root = corpus(tmp_path)
    plan = fixture_plan(root, titles=("Evidence",))
    plan.diagrams = [
        DiagramPlan.model_validate(
            {
                "diagram_id": "evidence-flow",
                "section_id": "section-0",
                "kind": kind,
                "purpose": "Explain the conceptual evidence review",
                "finding_ids": ["finding-0"],
                "caption": "Conceptual evidence review; source scope remains limited [S-01].",
            }
        )
    ]
    text = "# Findings\n\n## Evidence\n\n<!-- diagram: evidence-flow -->\n```mermaid\n" + code
    text += "\n```\n\n" + plan.diagrams[0].caption + "\n"
    validate_diagrams(text, plan)
    with pytest.raises(AuthoringError, match="render"):
        validate_diagrams(text.replace(code, kind + "\n{{{ broken"), plan)
    with pytest.raises(AuthoringError):
        validate_diagrams(text.replace("<!-- diagram: evidence-flow -->", ""), plan)
    with pytest.raises(AuthoringError):
        validate_diagrams(text.replace(plan.diagrams[0].caption, "No citation"), plan)
