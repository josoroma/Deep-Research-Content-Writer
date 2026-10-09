"""The citation gate, bound to one run's workspace.

Validation reads the draft and the corpus. It never rewrites either, so the
repair loop in the workflow decides what happens next (PD-016).
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from schemas.errors import AuthoringError
from schemas.state import RunState
from schemas.tool_io import (
    ValidateCitationsInput,
    ValidateCitationsOutput,
    ValidateSynthesisInput,
    ValidateSynthesisOutput,
)
from services.authoring import check_blog, validate_citations
from services.synthesis import validate_synthesis
from tools.base import TypedTool

if TYPE_CHECKING:
    from tools.base import Runtime, ToolRegistry


class AuthoringSession:
    """One run's workspace. Never shared across runs."""

    def __init__(self, root: Path, run: RunState) -> None:
        self.root = root
        self.run = run


def register_synthesis_tool(registry: ToolRegistry, session: AuthoringSession | None) -> None:
    """Let the analyst inspect the same gate the coordinator enforces."""

    def validate(
        request: ValidateSynthesisInput, runtime: Runtime | None
    ) -> ValidateSynthesisOutput:
        if session is None:
            raise ValueError("Synthesis validation requires an AuthoringSession")
        try:
            validate_synthesis(session.root)
        except AuthoringError as error:
            return ValidateSynthesisOutput(passed=False, errors=[str(error)])
        return ValidateSynthesisOutput(passed=True)

    registry.register(
        TypedTool[ValidateSynthesisInput, ValidateSynthesisOutput](
            name="validate_synthesis",
            input_model=ValidateSynthesisInput,
            output_model=ValidateSynthesisOutput,
            handler=validate,
            description=(
                "Check research/synthesis.json against the schema, saved request, "
                "fingerprint, whole corpus, exact excerpts, and evidence references. "
                "Returns actionable errors without changing any files or attempt counters. "
                "Correct the plan and check again before returning from Synthesize."
            ),
        )
    )


def register_authoring_tools(registry: ToolRegistry, session: AuthoringSession | None) -> None:
    def current(runtime: Runtime | None) -> tuple[AuthoringSession, RunState]:
        if session is None or runtime is None:
            raise ValueError("Citation tools require an AuthoringSession and ToolRuntime")
        run = RunState.model_validate(runtime.state["run"])
        if run.run_id != session.run.run_id:
            raise ValueError("AuthoringSession does not match the active run")
        return session, run

    def validate(
        request: ValidateCitationsInput, runtime: Runtime | None
    ) -> ValidateCitationsOutput:
        bound, run = current(runtime)
        finding = validate_citations(bound.root)
        phases = list(run.completed_phases)
        if finding.passed and check_blog(bound.root).headings_valid and "citations" not in phases:
            phases.append("citations")
        return ValidateCitationsOutput(
            citations_checked=finding.citations_checked,
            dangling_source_ids=finding.dangling_source_ids,
            mismatched_source_ids=finding.mismatched_source_ids,
            run=run.replaced(completed_phases=phases),
        )

    registry.register(
        TypedTool[ValidateCitationsInput, ValidateCitationsOutput](
            name="validate_citations",
            input_model=ValidateCitationsInput,
            output_model=ValidateCitationsOutput,
            handler=validate,
            updates_state=True,
            description=(
                "Check every [S-NN] in the run's dated content document against the corpus and the "
                "References section. Reports dangling and mismatched source ids."
            ),
        )
    )
