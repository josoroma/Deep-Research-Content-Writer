"""Shared research execution: the phases the CLI and the worker both run.

Phase ordering is owned here, not by a milestone workflow, so the worker and the
legacy CLI execute the same business rules. Each phase persists authoritative
state before the next one begins, and a phase completion is recorded only after
its artifacts validate.

Deterministic phases run through the registered tools so business rules stay in
one place. The model-driven synthesis/write phase uses the compiled agent graph,
which writes ``research/summary.md`` and the run's dated content document through the workspace
backend, followed by the deterministic citation gate.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from contextlib import closing
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

from langgraph.checkpoint.base import BaseCheckpointSaver

from application.context import ExecutionContext
from schemas.config import RunSettings
from schemas.errors import AuthoringError, ResearchError
from schemas.requests import ResearchRequest
from schemas.responses import RunReport
from schemas.search import QueryVariants
from schemas.state import RunState
from services.artifacts import write_json
from services.authoring import validate_citations
from services.authoring_pipeline import Stage, StageInvoker
from services.checkpoints import make_sqlite_checkpointer
from services.content_paths import content_path
from services.reporting import (
    authoring_reasons,
    build_run_report,
    classify_outcome,
    write_run_report,
)
from services.synthesis import saved_request
from workflows.authoring_run import run_authoring
from workflows.corpus_run import run_corpus
from workflows.resume import load_saved_run, next_phase
from workflows.search_run import run_search

AUTHORING_GATE = "output/authoring.json"
MAX_REPAIR_PASSES = 2
AuthoringMode = Literal["agent", "fixture"]


class SearchPhaseError(ResearchError, RuntimeError):
    """A deterministic search failure, safe to surface as a terminal reason."""

    code = "search_failed"


@dataclass
class ExecutionOutcome:
    """The terminal result of one attempt, ready to record on the job."""

    run: RunState
    status: str
    status_reasons: list[str] = field(default_factory=list)
    report: RunReport | None = None
    error: str | None = None
    search_only: bool = False

    @property
    def terminal_state(self) -> str:
        """The job state to record: search success, or the final report's status."""
        if self.search_only:
            return "succeeded" if self.error is None else "failed"
        if self.report is None:
            return "failed"
        return self.status


class RunService:
    """Execute and resume one run against an owned execution context.

    Args:
        context: Resources owned by this attempt.
        production: When true, stub tools are forbidden.
        authoring_mode: ``agent`` for model authoring, ``fixture`` for offline.
        synthesize: Replaces model synthesis, used by the fixture profile.
        checkpointer: A server saver; ``None`` selects the per-run SQLite saver.
    """

    def __init__(  # noqa: D107 - documented on the class
        self,
        context: ExecutionContext,
        *,
        production: bool = True,
        authoring_mode: AuthoringMode = "agent",
        synthesize: Callable[[Path, Stage], None] | None = None,
        checkpointer: BaseCheckpointSaver[Any] | None = None,
    ) -> None:
        self.context = context
        self.production = production
        self.authoring_mode = authoring_mode
        self.synthesize = synthesize
        self.checkpointer = checkpointer
        self.settings: RunSettings = context.settings
        self._started = time.monotonic()

    # -- phases ----------------------------------------------------------------
    def _phase_search(self, run: RunState) -> RunState:
        variants = None
        if self.context.variants is not None:
            variants = QueryVariants.model_validate(self.context.variants)
        summary = run_search(
            request=self._request(run),
            settings=self.settings,
            runs_root=self.context.workspace.root.parent,
            variants=variants,
            search_provider=self.context.search_provider,
            fake_model=self.context.llm.fake_model,
            workspace=self.context.workspace,
        )
        if summary.status != "completed":
            raise SearchPhaseError(summary.error or "search failed")
        return load_saved_run(self.context.workspace.root)

    def _phase_corpus(self, run: RunState) -> RunState:
        del run  # the corpus phase reloads authoritative state from the workspace
        summary = run_corpus(
            self.context.workspace.root,
            self.settings,
            fetcher=self.context.fetcher,
            extractor=self.context.extractor,
        )
        if summary.status != "completed":
            raise RuntimeError(summary.error or "corpus failed")
        return load_saved_run(self.context.workspace.root)

    def _phase_authoring(self, run: RunState) -> RunState:
        del run
        invoke: StageInvoker | None = None
        if self.authoring_mode == "fixture" and self.synthesize is not None:
            callback = self.synthesize

            def fixture_invoke(stage: Stage, prompt: str, current: RunState) -> None:
                del prompt, current
                callback(self.context.workspace.root, stage)

            invoke = fixture_invoke
        result = run_authoring(
            self.context.workspace.root,
            self.settings,
            llm=self.context.llm,
            checkpointer=self._checkpointer(self.context.workspace.root),
            invoke=invoke,
        )
        if result.status == "failed":
            raise AuthoringError("Authoring failed", code=result.reason or "phase_failed")
        return load_saved_run(self.context.workspace.root)

    def _phase_report(self, run: RunState, *, recorded_reasons: list[str]) -> RunReport:
        workspace = self.context.workspace.root
        finding = validate_citations(workspace)
        reasons = [*recorded_reasons, *authoring_reasons(workspace)]
        if not finding.passed and "dangling_citations" not in reasons:
            reasons.append("dangling_citations")
        status, status_reasons = classify_outcome(
            run, max_urls=self._max_urls(), recorded_reasons=reasons
        )
        report = build_run_report(
            run,
            self.context.ledger,
            workspace=workspace,
            blog_path=content_path(workspace),
            citation_count=finding.citations_checked,
            duration_seconds=time.monotonic() - self._started,
            status=status,
            status_reasons=status_reasons,
        )
        write_run_report(workspace, report)
        self._record_report_phase(run)
        return report

    def _record_report_phase(self, run: RunState) -> None:
        """Persist the report phase only after its artifact validates."""
        if "report" in run.completed_phases:
            return
        updated = run.replaced(completed_phases=[*run.completed_phases, "report"])
        write_json(
            self.context.workspace.root / "corpus_state.json", updated.model_dump(mode="json")
        )

    # -- public entry points ---------------------------------------------------
    def execute(self, *, operation: str = "research") -> ExecutionOutcome:
        """Run search, then (for ``research``) corpus, authoring, and the report.

        Never raises for a phase failure: the outcome carries a safe reason and,
        when possible, a failed report, so the worker can record it on the job.
        """
        self._started = time.monotonic()
        run = self.context.run
        try:
            run = self._phase_search(run)
        except Exception as error:  # noqa: BLE001 - worker records a safe reason only
            reason = str(error) if isinstance(error, SearchPhaseError) else type(error).__name__
            report = self._safe_report(run, reason=reason, failed=True)
            return ExecutionOutcome(
                run=run,
                status="failed",
                status_reasons=report.status_reasons,
                report=report,
                error=reason,
            )
        if operation == "search":
            return ExecutionOutcome(run=run, status="search_completed", search_only=True)
        try:
            run = self._phase_corpus(run)
            run = self._phase_authoring(run)
            report = self._phase_report(run, recorded_reasons=[])
        except Exception as error:  # noqa: BLE001
            report = self._safe_report(
                run,
                reason=error.code if isinstance(error, ResearchError) else "phase_failed",
                failed=True,
            )
            return ExecutionOutcome(
                run=run,
                status=report.status,
                status_reasons=report.status_reasons,
                report=report,
                error=type(error).__name__,
            )
        return ExecutionOutcome(
            run=run, status=report.status, status_reasons=report.status_reasons, report=report
        )

    def resume(self) -> ExecutionOutcome:
        """Continue an interrupted run from its first incomplete phase."""
        self._started = time.monotonic()
        run = load_saved_run(self.context.workspace.root)
        phase = next_phase(run.completed_phases)
        try:
            if phase in {"plan", "search", "normalize"}:
                run = self._phase_search(run)
                phase = next_phase(run.completed_phases)
            if phase in {"fetch", "index"}:
                run = self._phase_corpus(run)
                phase = next_phase(run.completed_phases)
            if phase in {"synthesize", "write", "citations"}:
                run = self._phase_authoring(run)
            report = self._phase_report(run, recorded_reasons=[])
        except Exception as error:  # noqa: BLE001
            report = self._safe_report(
                run,
                reason=error.code if isinstance(error, ResearchError) else "phase_failed",
                failed=True,
            )
            return ExecutionOutcome(
                run=run,
                status=report.status,
                status_reasons=report.status_reasons,
                report=report,
                error=type(error).__name__,
            )
        return ExecutionOutcome(
            run=run, status=report.status, status_reasons=report.status_reasons, report=report
        )

    # -- helpers ---------------------------------------------------------------
    def _max_urls(self) -> int:
        """The job's URL budget wins over the process default, then the setting."""
        return (
            self.context.max_urls if self.context.max_urls is not None else self.settings.max_urls
        )

    def _checkpointer(self, root: Path) -> BaseCheckpointSaver[Any] | None:
        """The server supplies a PostgreSQL saver; local CLI execution uses SQLite."""
        if self.checkpointer is not None:
            return self.checkpointer
        if not self.production:
            return None
        saver = make_sqlite_checkpointer(root / "checkpoints.sqlite")
        self.context.manage(closing(saver.conn))
        self.checkpointer = saver
        return saver

    def _request(self, run: RunState) -> ResearchRequest:
        request = saved_request(self.context.workspace.root)
        if request.topic != run.topic:
            raise AuthoringError("Run topic disagrees with the saved request")
        return request

    def _safe_report(self, run: RunState, *, reason: str, failed: bool) -> RunReport:
        """Always write a report, even after a failed phase."""
        workspace = self.context.workspace.root
        if (workspace / "corpus_state.json").exists():
            run = load_saved_run(workspace)
        finding = validate_citations(workspace)
        status, status_reasons = classify_outcome(
            run,
            max_urls=self._max_urls(),
            recorded_reasons=[reason, "phase_failed"] if failed else [reason],
        )
        if failed and status != "failed":
            # A raised phase is a phase failure, never an accidental success.
            status_reasons = [*status_reasons, "phase_failed"]
            status = "failed"
        report = build_run_report(
            run,
            self.context.ledger,
            workspace=workspace,
            blog_path=content_path(workspace),
            citation_count=finding.citations_checked,
            duration_seconds=time.monotonic() - self._started,
            status=status,
            status_reasons=status_reasons,
        )
        write_run_report(workspace, report)
        self._record_report_phase(run)
        return report
