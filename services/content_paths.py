"""One timestamped document path shared by authoring, reporting, and downloads."""

import json
import re
from datetime import UTC, datetime
from pathlib import Path

RUN_TIMESTAMP = re.compile(r"-(\d{8}T\d{6}Z)$")


def content_started_at(root: Path, *, fallback: datetime | None = None) -> datetime:
    """Use the saved UTC start time, including when a run resumes on another day.

    Older workspaces derive it from their run ID, or the original request's
    timestamp for custom IDs. The coordinator persists that value on its next
    authoring-state write. A supplied fallback initializes custom run IDs.
    Damaged state must still allow a failure report to name
    the document; authoring validates the full state before any model work.
    Uninitialized fixture workspaces use the current UTC time.
    """
    marker = root / "output/authoring_state.json"
    if marker.exists():
        try:
            state = json.loads(marker.read_text(encoding="utf-8"))
            saved = state.get("content_started_at") if isinstance(state, dict) else None
            if isinstance(saved, str):
                started_at = datetime.fromisoformat(saved)
                if started_at.tzinfo is not None:
                    return started_at.astimezone(UTC).replace(microsecond=0)
        except (ValueError, OSError):
            pass
    stamp = RUN_TIMESTAMP.search(root.name)
    if stamp is not None:
        try:
            return datetime.strptime(stamp.group(1), "%Y%m%dT%H%M%SZ").replace(tzinfo=UTC)
        except ValueError:
            pass
    if fallback is not None:
        if fallback.tzinfo is None:
            raise ValueError("content timestamps must be timezone-aware")
        return fallback.astimezone(UTC).replace(microsecond=0)
    request = root / "request.json"
    if request.is_file():
        return datetime.fromtimestamp(request.stat().st_mtime, UTC).replace(microsecond=0)
    return datetime.now(UTC).replace(microsecond=0)


def content_path(root: Path) -> str:
    """Return ``output/{yyyy-mm-dd-hh-mm-ss}-content.md`` relative to the run."""
    return f"output/{content_started_at(root):%Y-%m-%d-%H-%M-%S}-content.md"
