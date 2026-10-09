"""Score an evaluated run against the PD-021 rubric (US-10.3, US-10.4).

Deterministic checks (citation validity, length, coverage, Definition of Done) read
the run workspace. Source-aware claim and editorial judges default to
DeepSeek V4.1 Flash on OpenRouter, the same model the agents use, and is injected as
a fake in tests.
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from pathlib import Path
from typing import Literal, Protocol, runtime_checkable

from pydantic import Field

from schemas.authoring import Synthesis
from schemas.common import Contract
from schemas.config import PRODUCTION_MODEL, RunSettings
from schemas.responses import RunReport
from services.authoring import MAX_WORDS, MIN_WORDS, check_blog, validate_citations
from services.content_paths import content_path
from services.corpus import read_corpus
from services.markdown_document import content_text
from services.synthesis import authoring_state, validate_synthesis

# PD-021 release thresholds.
MIN_COVERAGE = 0.5
MIN_GROUNDEDNESS = 0.9
MAX_HALLUCINATION_RATE = 0.05
MIN_EXTRACTED_SHARE = 0.8

CITATION = re.compile(r"\[(S-\d{2,})\]")
SENTENCE = re.compile(r"(?<=[.!?])\s+")


class ClaimVerdict(Contract):
    """One factual claim and the judge's decision about it."""

    claim: str = Field(min_length=1)
    source_id: str | None = None
    supported: bool = False
    source_ids: list[str] = Field(default_factory=list)
    source_excerpts: dict[str, str] = Field(default_factory=dict)
    factual: bool = True


class AuthoringQuality(Contract):
    """Separate semantic editorial assessment from structural gate success."""

    goal_fit: bool
    format_fit: bool
    nuance_preserved: bool
    explanation: str
    mode: Literal["source_aware", "fixture"] = "source_aware"

    @property
    def passed(self) -> bool:
        """Require a useful format for the goal without losing evidence nuance."""
        return self.goal_fit and self.format_fit and self.nuance_preserved


@runtime_checkable
class StructureJudge(Protocol):
    """Optional evaluation of organization against the actual plan and evidence."""

    def judge_structure(self, plan: Synthesis, document: str) -> AuthoringQuality:
        """Assess the finished document against its evidence and reader objective."""
        ...


class Judge(Protocol):
    """A claim-level judge. The production judge calls a model; tests inject a fake."""

    def judge(self, claims: Sequence[ClaimVerdict]) -> list[ClaimVerdict]: ...


class DefinitionOfDone(Contract):
    """Each PRD.md §13 item, with the evidence that decided it."""

    results_processed: bool
    corpus_and_index: bool
    summary_written: bool
    blog_written: bool
    blog_length: bool
    zero_dangling_citations: bool
    references_section: bool
    run_report_written: bool
    trace_visible: bool

    @property
    def passed(self) -> bool:
        return all(self.model_dump().values())

    @property
    def failed_items(self) -> list[str]:
        return [name for name, value in self.model_dump().items() if not value]


class TopicScore(Contract):
    """One golden topic's scores and the PD-021 threshold verdict."""

    topic_id: str
    topic: str
    run_id: str
    workspace: str
    status: Literal["succeeded", "degraded", "failed"]
    citation_validity: bool
    dangling_citations: int
    word_count: int
    length_ok: bool
    coverage: float = Field(ge=0, le=1)
    groundedness: float = Field(ge=0, le=1)
    hallucination_rate: float = Field(ge=0, le=1)
    definition_of_done: DefinitionOfDone
    thresholds: dict[str, bool]
    passed: bool
    failures: list[str] = Field(default_factory=list)
    authoring_quality: AuthoringQuality | None = None


def _blog_text(workspace: Path) -> str:
    path = workspace / content_path(workspace)
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def coverage(workspace: Path) -> float:
    """PD-021: the share of corpus sources cited in the blog."""
    records = read_corpus(workspace)
    if not records:
        return 0.0
    cited = set(CITATION.findall(content_text(_blog_text(workspace))))
    known = {record.source.source_id for record in records}
    return len(cited & known) / len(known)


def source_excerpt(body: str, claim: str) -> str:
    """Keep a bounded relevant passage plus surrounding context and qualifications."""
    words = set(re.findall(r"\w{4,}", claim.casefold()))
    chunks = [body[index : index + 2000] for index in range(0, len(body), 1500)]
    if not chunks:
        return ""
    return max(chunks, key=lambda chunk: len(words & set(re.findall(r"\w{4,}", chunk.casefold()))))


def factual_claims(workspace: Path) -> list[ClaimVerdict]:
    """Sentences that carry a citation or a number/date, with their cited source.

    Heading lines are removed first, so a heading never merges with the sentence
    that follows it.
    """
    body = content_text(_blog_text(workspace))
    corpus = {item.source.source_id: item.source.body_markdown for item in read_corpus(workspace)}
    claims: list[ClaimVerdict] = []
    for sentence in SENTENCE.split(body):
        text = sentence.strip()
        if not text:
            continue
        cited = CITATION.findall(text)
        claims.append(
            ClaimVerdict(
                claim=text,
                source_id=cited[0] if cited else None,
                source_ids=list(dict.fromkeys(cited)),
                source_excerpts={
                    sid: source_excerpt(corpus[sid], text) for sid in cited if sid in corpus
                },
            )
        )
    return claims


def groundedness_and_hallucination(
    claims: Sequence[ClaimVerdict], judged: Sequence[ClaimVerdict]
) -> tuple[float, float]:
    """PD-021: groundedness over cited claims, hallucination over all factual claims.

    A claim is unsupported when the judge rejects it or when it carries no citation.
    """
    nonfactual = {item.claim for item in judged if not item.factual}
    claims = [item for item in claims if item.claim not in nonfactual]
    if not claims:
        return 1.0, 0.0
    supported = {item.claim for item in judged if item.supported}
    cited = [item for item in claims if item.source_id is not None]
    grounded = sum(1 for item in cited if item.claim in supported)
    unsupported = sum(1 for item in claims if item.claim not in supported)
    groundedness = grounded / len(cited) if cited else 1.0
    return groundedness, unsupported / len(claims)


def definition_of_done(workspace: Path, report: RunReport) -> DefinitionOfDone:
    """PRD.md §13, each item decided from the workspace and the report."""
    blog = check_blog(workspace)
    finding = validate_citations(workspace)
    extracted_share = report.urls_extracted / report.urls_clean if report.urls_clean else 0.0
    return DefinitionOfDone(
        results_processed=report.urls_clean > 0 and extracted_share >= MIN_EXTRACTED_SHARE,
        corpus_and_index=(workspace / "research/index.md").is_file(),
        summary_written=(workspace / "research/summary.md").is_file(),
        blog_written=blog.present,
        blog_length=blog.within_length,
        zero_dangling_citations=finding.passed,
        references_section=blog.headings_valid,
        run_report_written=(workspace / "output/run.json").is_file(),
        trace_visible=(workspace / "logs/execution.log").is_file(),
    )


def score_topic(
    workspace: Path,
    report: RunReport,
    *,
    topic_id: str,
    judge: Judge | None = None,
) -> TopicScore:
    """Score one evaluated run and decide whether it passes every PD-021 threshold."""
    blog = check_blog(workspace)
    finding = validate_citations(workspace)
    claims = factual_claims(workspace)
    judged = judge.judge(claims) if judge is not None else claims
    grounded, hallucination = groundedness_and_hallucination(claims, judged)
    done = definition_of_done(workspace, report)
    quality = None
    adaptive = authoring_state(workspace).contract_version == 2
    if adaptive and isinstance(judge, StructureJudge):
        quality = judge.judge_structure(validate_synthesis(workspace), _blog_text(workspace))
    thresholds = {
        "zero_dangling_citations": finding.passed,
        "length_2000_5000": blog.within_length,
        "definition_of_done": done.passed,
        "coverage_min_0.5": coverage(workspace) >= MIN_COVERAGE,
        "groundedness_min_0.9": grounded >= MIN_GROUNDEDNESS,
        "hallucination_max_0.05": hallucination <= MAX_HALLUCINATION_RATE,
    }
    if adaptive:
        thresholds["format_goal_nuance"] = quality.passed if quality is not None else False
    failures = [name for name, ok in thresholds.items() if not ok]
    return TopicScore(
        topic_id=topic_id,
        topic=report.topic,
        run_id=report.run_id,
        workspace=str(workspace),
        status=report.status,
        citation_validity=finding.passed,
        dangling_citations=len(finding.dangling_source_ids) + len(finding.mismatched_source_ids),
        word_count=blog.word_count,
        length_ok=blog.within_length,
        coverage=coverage(workspace),
        groundedness=grounded,
        hallucination_rate=hallucination,
        definition_of_done=done,
        thresholds=thresholds,
        passed=not failures,
        failures=failures,
        authoring_quality=quality,
    )


class Benchmark(Contract):
    """One `make eval` run: every topic's scores, keyed by date and commit."""

    date: str
    commit: str
    model: str
    judge_model: str
    topics: list[TopicScore]
    passed: bool
    failures: list[str] = Field(default_factory=list)


def benchmark_name(date: str, commit: str) -> str:
    return f"{date}-{commit}.json"


def judge_model_id(settings: RunSettings) -> str:
    """PD-021: the judge defaults to the production model unless overridden."""
    return settings.models.orchestrator or PRODUCTION_MODEL


def word_range() -> tuple[int, int]:
    return MIN_WORDS, MAX_WORDS
