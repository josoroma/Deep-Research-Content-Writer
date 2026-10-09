"""Resume an interrupted run from its last completed phase (US-8.4, PD-019)."""

import json
from pathlib import Path

from schemas.common import Phase
from schemas.state import RunState

PHASE_ORDER: tuple[Phase, ...] = (
    "plan",
    "search",
    "normalize",
    "fetch",
    "index",
    "synthesize",
    "write",
    "citations",
    "report",
)


def checkpoint_path(workspace: Path) -> Path:
    return workspace / "checkpoints.sqlite"


def load_saved_run(workspace: Path) -> RunState:
    """Load the furthest contiguous phase progress, preferring corpus state on ties.

    A failed search also writes a corpus state to record its report. That earlier
    failure must not hide a successful search state written by a later attempt.
    """
    saved: list[RunState] = []
    for name in ("corpus_state.json", "fetch_state.json", "search_state.json"):
        path = workspace / name
        if path.exists():
            saved.append(RunState.model_validate(json.loads(path.read_text())))
    if not saved:
        raise ValueError(f"No saved run state in {workspace}")
    return max(saved, key=_progress)


def _progress(run: RunState) -> int:
    return next(
        (index for index, phase in enumerate(PHASE_ORDER) if phase not in run.completed_phases),
        len(PHASE_ORDER),
    )


def next_phase(completed: list[Phase]) -> Phase | None:
    """The first phase the run has not recorded, in pipeline order."""
    done = set(completed)
    return next((phase for phase in PHASE_ORDER if phase not in done), None)
