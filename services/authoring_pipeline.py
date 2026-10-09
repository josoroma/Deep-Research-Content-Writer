"""One resumable authoring pipeline shared by CLI milestones and workers."""

import json
from collections.abc import Callable
from pathlib import Path
from typing import Literal

from schemas.authoring import AuthoringResult, Synthesis
from schemas.common import Phase
from schemas.errors import AuthoringError, AuthoringInterrupted
from schemas.state import RunState
from services.artifacts import write_json
from services.authoring import (
    SUMMARY_PATH,
    check_blog,
    check_summary,
    validate_citations,
)
from services.content_paths import content_path
from services.document_finalizer import finalize_document
from services.observability import current_observer
from services.synthesis import (
    SYNTHESIS_PATH,
    authoring_state,
    commit_synthesis,
    file_fingerprint,
    input_fingerprint,
    save_authoring_state,
    saved_request,
    validate_synthesis,
)

Stage = Literal["synthesize", "write", "repair"]
StageInvoker = Callable[[Stage, str, RunState], None]


class AuthoringPipeline:
    """Persist reservations before invoking models; validate before phase commits.

    Args:
        root: The owned run workspace.
        run: Authoritative corpus progress.
        invoke: The agent or fixture callback for one bounded stage.
    """

    def __init__(self, root: Path, run: RunState, invoke: StageInvoker) -> None:
        """Bind one pipeline to one run; no resources are shared across jobs."""
        self.root, self.run, self.invoke = root, run, invoke
        self.state = authoring_state(root)
        self.result = AuthoringResult(
            run_id=run.run_id, workspace=str(root), contract_version=self.state.contract_version
        )

    def execute(self) -> AuthoringResult:
        """Continue completed work and generate at most one substantive draft."""
        fingerprint = input_fingerprint(self.root)
        if self.state.input_fingerprint and self.state.input_fingerprint != fingerprint:
            raise AuthoringError("Authoring inputs changed")
        self.state.input_fingerprint = fingerprint
        self._save()
        plan = self._synthesize()
        self._write(plan)
        self._repair(plan)
        return self._finish()

    def _save(self) -> None:
        save_authoring_state(self.root, self.state)

    def _complete(self, phase: Phase) -> None:
        if phase not in self.run.completed_phases:
            self.run = self.run.replaced(completed_phases=[*self.run.completed_phases, phase])
            write_json(self.root / "corpus_state.json", self.run.model_dump(mode="json"))

    def _context(self) -> str:
        return (
            f"Run ID: {self.run.run_id}. Saved research request: "
            + saved_request(self.root).model_dump_json()
        )

    def _synthesize(self) -> Synthesis | None:
        if self.state.contract_version == 1:
            self._legacy_synthesis()
            return None
        if not self.state.synthesis_completed:
            self._attempt_synthesis()
        plan = validate_synthesis(self.root)
        if self.state.synthesis_fingerprint != file_fingerprint(self.root / SYNTHESIS_PATH):
            raise AuthoringError("Validated synthesis was modified")
        commit_synthesis(self.root)
        self.result.format_label = plan.format.label
        self.result.synthesis_path = SYNTHESIS_PATH
        self._complete("synthesize")
        return plan

    def _attempt_synthesis(self) -> None:
        feedback: str | None = None
        if self.state.synthesis_attempts and (self.root / SYNTHESIS_PATH).exists():
            try:
                validate_synthesis(self.root)
            except AuthoringError as error:
                feedback = str(error)
        while self.state.synthesis_attempts < 2:
            self.state.synthesis_attempts += 1
            self._save()
            prompt = (
                "Run only Synthesize. Delegate to analyst_agent; do not write a draft. "
                "Read every numbered corpus source and the index, choose an evidence-backed "
                "format and outline, and write research/synthesis.json. "
                "The analyst must call validate_synthesis and correct its reported errors "
                "before returning. Return the plan path only; the application will render "
                "research/summary.md after validation. Do not write that summary yourself. "
                + self._context()
                + f" Input fingerprint (copy exactly): {self.state.input_fingerprint}. "
                + "Required JSON schema: "
                + json.dumps(Synthesis.model_json_schema())
            )
            if feedback:
                prompt += (
                    " Previous attempt failed validation: "
                    + feedback
                    + ". Correct the existing synthesis against the immutable corpus; "
                    "do not write a draft or change the saved request."
                )
            try:
                self.invoke("synthesize", prompt, self.run)
                commit_synthesis(self.root)
            except Exception as error:
                if self.state.synthesis_attempts >= 2:
                    raise
                feedback = str(error) if isinstance(error, AuthoringError) else type(error).__name__
                observer = current_observer()
                if observer is not None:
                    observer.retry("synthesize", "synthesis_invalid")
                continue
            self.state.synthesis_completed = True
            self.state.synthesis_fingerprint = file_fingerprint(self.root / SYNTHESIS_PATH)
            self._save()
            return
        raise AuthoringError("Synthesis attempt budget exhausted")

    def _legacy_synthesis(self) -> None:
        if not self.state.synthesis_completed:
            if not (self.root / SUMMARY_PATH).exists():
                self.invoke(
                    "synthesize",
                    "Run only Synthesize. Read all sources and write "
                    "research/summary.md. " + self._context(),
                    self.run,
                )
            if not check_summary(self.root).passed:
                raise AuthoringError("Legacy summary is invalid")
            self.state.synthesis_completed = True
            self._save()
        self._complete("synthesize")

    def _write(self, plan: Synthesis | None) -> None:
        path = self.root / content_path(self.root)
        if (
            self.state.generation == "completed"
            and not self.state.repair_in_progress
            and (not path.exists() or self.state.draft_fingerprint != file_fingerprint(path))
        ):
            raise AuthoringInterrupted("Completed draft was modified outside a reserved repair")
        if self.state.generation == "not_started":
            if path.exists():
                if plan is not None:
                    raise AuthoringInterrupted("Unreserved draft requires reconciliation")
            else:
                self.state.generation = "in_progress"
                self._save()
                self.invoke(
                    "write",
                    "Run only Write. Delegate to writer_agent and write "
                    f"{content_path(self.root)} exactly once using the validated synthesis and "
                    "source corpus. Do not run research or change the outline. " + self._context(),
                    self.run,
                )
        if not path.exists():
            raise AuthoringInterrupted("Reserved generation produced no complete draft")
        if plan is not None:
            finalize_document(self.root, plan)
        checked = check_blog(self.root)
        if not checked.headings_valid:
            self.result.violations = checked.violations
            reason = (
                "diagram_invalid" if "diagram_invalid" in checked.violations else "blog_structure"
            )
            raise AuthoringError("Document structure is invalid", code=reason)
        self.state.generation = "completed"
        if not self.state.repair_in_progress:
            self.state.draft_fingerprint = file_fingerprint(path)
        self._save()
        self._complete("write")

    def _repair(self, plan: Synthesis | None) -> None:
        path = self.root / content_path(self.root)
        if self.state.repair_in_progress:
            unchanged = self.state.draft_fingerprint == file_fingerprint(path)
            if unchanged and not validate_citations(self.root).passed:
                raise AuthoringInterrupted("Interrupted citation repair requires reconciliation")
            self.state.repair_in_progress = False
            self._save()
        while not validate_citations(self.root).passed and self.state.repair_passes < 2:
            finding = validate_citations(self.root)
            outstanding = finding.dangling_source_ids + finding.mismatched_source_ids
            self.state.repair_passes += 1
            self.state.repair_in_progress = True
            self.state.draft_fingerprint = file_fingerprint(path)
            self._save()
            observer = current_observer()
            if observer is not None:
                observer.retry("citations", "citation_repair")
            self.invoke(
                "repair",
                "Fix or remove only these dangling/mismatched citations: "
                + ", ".join(outstanding)
                + ". Do not regenerate the document.",
                self.run,
            )
            if plan is not None:
                finalize_document(self.root, plan)
            if not check_blog(self.root).headings_valid:
                raise AuthoringError("Repair changed the outline", code="blog_structure")
            self.state.repair_in_progress = False
            self.state.draft_fingerprint = file_fingerprint(path)
            self._save()

    def _finish(self) -> AuthoringResult:
        blog, finding = check_blog(self.root), validate_citations(self.root)
        self.result.summary_path = SUMMARY_PATH
        self.result.blog_path = content_path(self.root)
        self.result.word_count = blog.word_count
        self.result.repair_passes = self.state.repair_passes
        self.result.citations_checked = finding.citations_checked
        self.result.dangling_source_ids = finding.dangling_source_ids
        self.result.mismatched_source_ids = finding.mismatched_source_ids
        if not finding.passed:
            self.result.status, self.result.reason = "failed", "dangling_citations"
        else:
            self._complete("citations")
            self.result.reason = None if blog.within_length else "blog_length"
        return self.result
