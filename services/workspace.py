"""Run workspace creation: topic slug, UTC run id, and the persisted request."""

import re
import time
import unicodedata
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

from schemas.authoring import AuthoringState
from schemas.errors import InvalidInputError
from schemas.requests import ResearchRequest
from schemas.workspace import RunWorkspace
from services.artifacts import write_json, write_text
from services.content_paths import content_started_at
from services.observability import bind_workspace

MAX_SLUG_LENGTH = 60
REQUEST_FILENAME = "request.json"


def slugify(topic: str) -> str:
    """Lowercase ASCII words joined by hyphens, at most 60 characters."""
    ascii_topic = unicodedata.normalize("NFKD", topic).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_topic.lower()).strip("-")
    return slug[:MAX_SLUG_LENGTH].strip("-") or "topic"


def run_id_for(topic: str, now: datetime) -> str:
    """`<slug>-<YYYYMMDDTHHMMSSZ>`; naive timestamps are rejected."""
    if now.tzinfo is None:
        raise ValueError("run id timestamps must be timezone-aware")
    stamp = now.astimezone(UTC).strftime("%Y%m%dT%H%M%SZ")
    return f"{slugify(topic)}-{stamp}"


def create_run_workspace(
    request: ResearchRequest,
    runs_root: Path,
    *,
    now: datetime | None = None,
    run_id: str | None = None,
    create: bool = True,
    authoring_version: Literal[1, 2] = 2,
) -> RunWorkspace:
    """Create `runs/<run_id>/` and persist the validated request.

    The request is already validated, so an invalid topic never reaches this call.
    `exist_ok=False` guarantees a run never overwrites another run's workspace.
    When the worker already allocated the directory (`create=False`) it supplies the
    exact `run_id` so no second directory is invented for the same job.
    """
    moment = now if now is not None else datetime.now(UTC)
    resolved_id = run_id if run_id is not None else run_id_for(request.topic, moment)
    root = runs_root / resolved_id
    if create:
        root.mkdir(parents=True, exist_ok=False)
    elif not root.is_dir():
        raise ValueError(f"Run workspace does not exist: {resolved_id}")
    request_path = root / REQUEST_FILENAME
    if request_path.exists():
        saved = ResearchRequest.model_validate_json(request_path.read_text(encoding="utf-8"))
        if saved != request:
            raise InvalidInputError("Saved request differs from resumed request")
    else:
        write_text(request_path, request.model_dump_json(indent=2) + "\n")
        if authoring_version == 2:
            (root / "output").mkdir(exist_ok=True)
            write_json(
                root / "output/authoring_state.json",
                AuthoringState(
                    content_started_at=content_started_at(root, fallback=moment)
                ).model_dump(mode="json"),
            )
    bind_workspace(root, request.topic)
    return RunWorkspace(run_id=resolved_id, root=root)


def allocate_run_id(topic: str, runs_root: Path, *, attempts: int = 5) -> str:
    """Allocate a run id and directory, retrying only the timestamp collision.

    A collision means another run claimed this UTC second. Waiting for the next
    second is bounded; the research job itself is never retried to get a name.
    """
    runs_root.mkdir(parents=True, exist_ok=True)
    for _ in range(attempts):
        run_id = run_id_for(topic, datetime.now(UTC))
        try:
            (runs_root / run_id).mkdir(parents=True, exist_ok=False)
        except FileExistsError:
            # Wait for the next whole UTC second before trying a new timestamp.
            time.sleep(1.0 - (time.time() % 1.0) + 0.01)
            continue
        return run_id
    raise ValueError("Could not allocate a unique run id")
