"""Versioned evidence, structure, and durable model-attempt contracts."""

from datetime import date
from typing import Annotated, Literal, Self

from pydantic import AwareDatetime, Field, StringConstraints, field_validator, model_validator

from schemas.common import Contract, Goal, SourceID, Topic

Text = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
Identifier = Annotated[str, Field(pattern=r"^[a-zA-Z0-9][a-zA-Z0-9_-]*$")]


class Evidence(Contract):
    """An exact corpus excerpt, with its relationship to the finding."""

    source_id: SourceID
    excerpt: str = Field(min_length=1, max_length=800)
    role: Literal["supports", "qualifies", "contradicts"] = "supports"
    context: str | None = None


class Finding(Contract):
    """A supported statement with explicit qualifications and dissent."""

    finding_id: Identifier
    statement: Text
    evidence: list[Evidence] = Field(min_length=1)
    qualifications: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def supported(self) -> Self:
        """A contradiction alone cannot support an affirmative finding."""
        if not any(item.role == "supports" for item in self.evidence):
            raise ValueError("Every finding needs supporting evidence")
        return self


class OutlineSection(Contract):
    """A reader-facing section grounded in findings or an explicit limitation."""

    section_id: Identifier
    title: Text
    level: Literal[2, 3] = 2
    purpose: Text
    finding_ids: list[Identifier] = Field(default_factory=list)
    limitation: str | None = None

    @field_validator("title")
    @classmethod
    def valid_title(cls, value: str) -> str:
        """Keep navigation and closing sections outside the adaptive outline."""
        if "\n" in value or not value.strip() or value != value.strip():
            raise ValueError("Section titles must be nonblank single lines")
        if value.casefold() in {"table of contents", "references", "why this format"}:
            raise ValueError("Reserved document section")
        return value

    @model_validator(mode="after")
    def grounded(self) -> Self:
        """A substantive section must have evidence or explain a gap."""
        if not self.finding_ids and not (self.limitation and self.limitation.strip()):
            raise ValueError("Section needs findings or an explicit limitation")
        return self


class DiagramPlan(Contract):
    """Purpose, placement, and provenance for an optional Mermaid diagram."""

    diagram_id: Identifier
    section_id: Identifier
    kind: Literal["flowchart", "sequenceDiagram"]
    purpose: Text
    finding_ids: list[Identifier] = Field(min_length=1)
    caption: Text


class FormatDecision(Contract):
    """A descriptive format label, not a selector for a fixed template."""

    label: Text
    why: Text
    alternatives: list[str] = Field(default_factory=list)
    confidence: Literal["limited", "moderate", "strong"] = "moderate"


class Synthesis(Contract):
    """The analyst's authoritative, evidence-backed writing plan."""

    contract_version: Literal[2] = 2
    run_id: Text
    topic: Topic
    goal: Goal = None
    input_fingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    reader_objective: Text
    objective_origin: Literal["explicit", "inferred"]
    considered_source_ids: list[SourceID] = Field(min_length=1)
    evidence_types: list[Text] = Field(min_length=1)
    limitations: list[str] = Field(default_factory=list)
    findings: list[Finding] = Field(min_length=1)
    gaps: list[str] = Field(default_factory=list)
    format: FormatDecision
    outline: list[OutlineSection] = Field(min_length=1)
    diagrams: list[DiagramPlan] = Field(default_factory=list)
    closing_rationale: Text

    @field_validator("closing_rationale", "reader_objective")
    @classmethod
    def nonblank_prose(cls, value: str) -> str:
        """Prose must not introduce hidden headings into the document envelope."""
        if not value.strip() or any(line.lstrip().startswith("#") for line in value.splitlines()):
            raise ValueError("Expected nonblank prose without headings")
        return value

    @model_validator(mode="after")
    def references_valid(self) -> Self:
        """Reject duplicate IDs, orphan findings, and impossible heading order."""
        findings = [item.finding_id for item in self.findings]
        sections = [item.section_id for item in self.outline]
        diagrams = [item.diagram_id for item in self.diagrams]
        for ids in (findings, sections, diagrams, self.considered_source_ids):
            if len(ids) != len(set(ids)):
                raise ValueError("Duplicate synthesis identifiers")
        if self.outline[0].level != 2:
            raise ValueError("The outline must begin with a level-2 section")
        referenced = [fid for section in self.outline for fid in section.finding_ids]
        referenced.extend(fid for diagram in self.diagrams for fid in diagram.finding_ids)
        if set(referenced) - set(findings):
            raise ValueError("Unknown finding in outline or diagram")
        if set(findings) - set(referenced):
            raise ValueError("Relevant findings must appear in the outline or diagrams")
        if any(item.section_id not in sections for item in self.diagrams):
            raise ValueError("Unknown diagram section")
        expected_origin = "explicit" if self.goal is not None else "inferred"
        if self.objective_origin != expected_origin:
            raise ValueError("Reader objective origin disagrees with goal")
        return self


class AuthoringState(Contract):
    """Persist attempt reservations before model work, including across restarts."""

    contract_version: Literal[1, 2] = 2
    content_started_at: AwareDatetime | None = None
    # Keep date-only markers readable when resuming older workspaces.
    content_date: date | None = None
    input_fingerprint: str = ""
    synthesis_attempts: int = Field(default=0, ge=0, le=2)
    synthesis_completed: bool = False
    generation: Literal["not_started", "in_progress", "completed"] = "not_started"
    repair_passes: int = Field(default=0, ge=0, le=2)
    repair_in_progress: bool = False
    draft_fingerprint: str | None = None
    synthesis_fingerprint: str | None = None


class AuthoringGate(Contract):
    """Inspection record shared by the worker, CLI, and final report."""

    contract_version: Literal[1, 2]
    format_label: str | None = None
    synthesis_path: str | None = None
    reason: str | None = None
    violations: list[str] = Field(default_factory=list)
    repair_passes: int = 0


class AuthoringResult(Contract):
    """The authoring milestone result and detailed, downloadable gate record."""

    run_id: str
    workspace: str
    status: Literal["completed", "failed"] = "completed"
    contract_version: Literal[1, 2] = 2
    format_label: str | None = None
    synthesis_path: str | None = None
    summary_path: str | None = None
    blog_path: str | None = None
    word_count: int = 0
    citations_checked: int = 0
    repair_passes: int = 0
    dangling_source_ids: list[SourceID] = Field(default_factory=list)
    mismatched_source_ids: list[SourceID] = Field(default_factory=list)
    violations: list[str] = Field(default_factory=list)
    reason: str | None = None
    error: str | None = None
