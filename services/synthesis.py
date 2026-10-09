"""Validate evidence plans against the authoritative request and immutable corpus."""

import hashlib
import json
import re
from pathlib import Path

from pydantic import ValidationError

from schemas.authoring import AuthoringResult, AuthoringState, Synthesis
from schemas.errors import AuthoringError
from schemas.requests import ResearchRequest
from services.artifacts import write_json, write_text
from services.content_paths import content_path, content_started_at
from services.corpus import read_corpus

SYNTHESIS_PATH = "research/synthesis.json"
AUTHORING_STATE = "output/authoring_state.json"
SOURCE_CITATION = re.compile(r"\[(S-\d{2,})\]")


def saved_request(root: Path) -> ResearchRequest:
    """Load the original topic, goal, and budget instead of reconstructing them."""
    return ResearchRequest.model_validate_json((root / "request.json").read_text(encoding="utf-8"))


def authoring_state(root: Path) -> AuthoringState:
    """An absent marker means legacy; a malformed marker never means legacy."""
    path = root / AUTHORING_STATE
    if not path.exists():
        return _legacy_state(root)
    try:
        return AuthoringState.model_validate_json(path.read_text(encoding="utf-8"))
    except (ValidationError, OSError) as error:
        raise AuthoringError("Invalid authoring state") from error


def _legacy_state(root: Path) -> AuthoringState:
    gate, draft = root / "output/authoring.json", root / content_path(root)
    if not gate.exists():
        return AuthoringState(contract_version=1)
    try:
        data = json.loads(gate.read_text(encoding="utf-8"))
        record = AuthoringResult.model_validate({"workspace": str(root), **data})
        return AuthoringState(
            contract_version=1,
            repair_passes=record.repair_passes,
            generation="completed" if draft.exists() else "not_started",
            draft_fingerprint=file_fingerprint(draft) if draft.exists() else None,
        )
    except (ValidationError, ValueError, OSError, TypeError) as error:
        raise AuthoringError("Invalid legacy authoring budget") from error


def save_authoring_state(root: Path, state: AuthoringState) -> None:
    """Commit model reservations and stage completion atomically."""
    if state.content_started_at is None:
        state.content_started_at = content_started_at(root)
    (root / "output").mkdir(exist_ok=True)
    write_json(root / AUTHORING_STATE, state.model_dump(mode="json"))


def input_fingerprint(root: Path) -> str:
    """Bind a writing decision to the normalized request and actual source bytes."""
    payload = saved_request(root).model_dump(mode="json")
    payload["sources"] = {
        record.source.source_id: hashlib.sha256((root / record.path).read_bytes()).hexdigest()
        for record in read_corpus(root)
    }
    canonical = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def file_fingerprint(path: Path) -> str:
    """Hash a completed artifact for interruption reconciliation."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_synthesis(root: Path) -> Synthesis:
    """Parse the schema and expose field errors without rejected input values."""
    try:
        return Synthesis.model_validate_json((root / SYNTHESIS_PATH).read_text(encoding="utf-8"))
    except ValidationError as error:
        problems = [
            ".".join(str(part) for part in item["loc"]) + ": " + item["msg"]
            for item in error.errors(include_input=False, include_url=False, include_context=False)
        ]
        raise AuthoringError("Invalid synthesis: " + "; ".join(problems)) from error
    except OSError as error:
        raise AuthoringError("Missing or invalid synthesis") from error


def validate_synthesis(root: Path) -> Synthesis:
    """Check identity, source completeness, excerpts, and all evidence references."""
    plan = _load_synthesis(root)
    request = saved_request(root)
    if (plan.run_id, plan.topic, plan.goal) != (root.name, request.topic, request.goal):
        raise AuthoringError("Synthesis does not match the saved request")
    if plan.input_fingerprint != input_fingerprint(root):
        raise AuthoringError("Synthesis inputs changed")
    corpus = {record.source.source_id: record.source for record in read_corpus(root)}
    if set(plan.considered_source_ids) != set(corpus):
        raise AuthoringError("Synthesis must consider the entire corpus")
    invalid_excerpts: list[str] = []
    for finding in plan.findings:
        for evidence in finding.evidence:
            source = corpus.get(evidence.source_id)
            if source is None or evidence.excerpt not in source.body_markdown:
                invalid_excerpts.append(f"{finding.finding_id}/{evidence.source_id}")
    if invalid_excerpts:
        raise AuthoringError(
            "Finding excerpts are absent from their sources: "
            + ", ".join(invalid_excerpts)
            + "; copy short, exact excerpts preserving each source's Markdown, "
            "whitespace, and punctuation"
        )
    if set(SOURCE_CITATION.findall(plan.model_dump_json())) - set(corpus):
        raise AuthoringError("Synthesis cites an unknown source")
    _validate_diagram_sources(plan)
    return plan


def _validate_diagram_sources(plan: Synthesis) -> None:
    findings = {item.finding_id: item for item in plan.findings}
    for diagram in plan.diagrams:
        sources = {e.source_id for fid in diagram.finding_ids for e in findings[fid].evidence}
        if not set(SOURCE_CITATION.findall(diagram.caption)) & sources:
            raise AuthoringError("Diagram caption must cite its supporting findings")


def render_summary(plan: Synthesis) -> str:
    """Render readable research following the chosen outline, from one decision."""
    blocks = [
        f"# Research synthesis: {plan.topic}",
        plan.reader_objective,
        f"Format: {plan.format.label}. {plan.format.why}",
    ]
    findings = {item.finding_id: item for item in plan.findings}
    for section in plan.outline:
        blocks.append(f"{'#' * section.level} {section.title}")
        blocks.append(section.purpose)
        for finding_id in section.finding_ids:
            finding = findings[finding_id]
            citations = " ".join(f"[{item.source_id}]" for item in finding.evidence)
            blocks.append(f"{finding.statement} {citations}")
            blocks.extend(f"- Qualification: {item}" for item in finding.qualifications)
            blocks.extend(
                f"- {item.role}: {item.excerpt} [{item.source_id}]"
                for item in finding.evidence
                if item.role != "supports"
            )
        if section.limitation:
            blocks.append(f"Limitation: {section.limitation}")
    blocks.extend(f"Gap: {item}" for item in plan.gaps)
    blocks.extend(f"Corpus limitation: {item}" for item in plan.limitations)
    blocks.append(plan.closing_rationale)
    return "\n\n".join(blocks) + "\n"


def commit_synthesis(root: Path) -> Synthesis:
    """Validate before atomically canonicalizing JSON and rendering the summary."""
    plan = validate_synthesis(root)
    write_json(root / SYNTHESIS_PATH, plan.model_dump(mode="json"))
    write_text(root / "research/summary.md", render_summary(plan))
    return plan
