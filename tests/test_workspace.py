"""US-3.1: run id derivation, workspace creation, and persisted input."""

from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path

import pytest
from pydantic import ValidationError

from schemas.requests import ResearchRequest
from schemas.workspace import RunWorkspace
from services.content_paths import content_path
from services.synthesis import authoring_state, save_authoring_state
from services.workspace import create_run_workspace, run_id_for, slugify

FIXED = datetime(2026, 10, 1, 8, 30, 0, tzinfo=UTC)


def test_slug_is_lowercase_ascii_words_joined_by_hyphens() -> None:
    assert slugify("2026 Agentic AI Frameworks") == "2026-agentic-ai-frameworks"
    assert slugify("LangGraph vs CrewAI: A 2026 Comparison") == (
        "langgraph-vs-crewai-a-2026-comparison"
    )
    assert slugify("Café — Résumé!") == "cafe-resume"


def test_slug_is_capped_and_falls_back_for_non_ascii() -> None:
    assert len(slugify("word " * 40)) <= 60
    assert slugify("日本語のトピック") == "topic"


def test_run_id_is_slug_hyphen_utc_timestamp() -> None:
    assert run_id_for("2026 agentic AI frameworks", FIXED) == (
        "2026-agentic-ai-frameworks-20261001T083000Z"
    )


def test_run_id_converts_offsets_to_utc() -> None:
    offset = timezone(timedelta(hours=2))
    assert run_id_for("topic", datetime(2026, 10, 1, 10, 30, tzinfo=offset)).endswith(
        "-20261001T083000Z"
    )


def test_run_id_rejects_naive_timestamps() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        run_id_for("topic", datetime(2026, 10, 1, 8, 30))


def test_workspace_is_created_and_request_is_persisted(tmp_path: Path) -> None:
    request = ResearchRequest(topic="  2026 agentic AI frameworks  ")
    workspace = create_run_workspace(request, tmp_path, now=FIXED)
    assert isinstance(workspace, RunWorkspace)
    assert workspace.run_id == "2026-agentic-ai-frameworks-20261001T083000Z"
    assert workspace.root == tmp_path / workspace.run_id
    assert workspace.root.is_dir()
    stored = ResearchRequest.model_validate_json(
        (workspace.root / "request.json").read_text(encoding="utf-8")
    )
    assert stored == request
    assert stored.topic == "2026 agentic AI frameworks"


def test_workspace_never_overwrites_an_existing_run(tmp_path: Path) -> None:
    request = ResearchRequest(topic="2026 agentic AI frameworks")
    create_run_workspace(request, tmp_path, now=FIXED)
    with pytest.raises(FileExistsError):
        create_run_workspace(request, tmp_path, now=FIXED)


def test_document_timestamp_is_utc_and_survives_resume_with_a_custom_id(tmp_path: Path) -> None:
    request = ResearchRequest(topic="Evidence driven writing")
    start = datetime(2026, 1, 1, 0, 30, 37, tzinfo=timezone(timedelta(hours=2)))
    workspace = create_run_workspace(request, tmp_path, now=start, run_id="custom-run")
    expected = "output/2025-12-31-22-30-37-content.md"
    assert content_path(workspace.root) == expected
    resumed = create_run_workspace(
        request, tmp_path, now=FIXED, run_id=workspace.run_id, create=False
    )
    state = authoring_state(resumed.root)
    state.synthesis_attempts = 1
    save_authoring_state(resumed.root, state)
    assert content_path(resumed.root) == expected


def test_older_state_gets_document_timestamp_from_run_id(tmp_path: Path) -> None:
    root = tmp_path / "writing-20261001T083000Z"
    (root / "output").mkdir(parents=True)
    marker = root / "output/authoring_state.json"
    marker.write_text('{"contract_version": 2, "content_date": "2026-10-01"}', encoding="utf-8")
    state = authoring_state(root)
    save_authoring_state(root, state)
    assert content_path(root) == "output/2026-10-01-08-30-00-content.md"
    assert '"content_started_at": "2026-10-01T08:30:00Z"' in marker.read_text(encoding="utf-8")


def test_same_day_runs_get_distinct_second_precision_filenames(tmp_path: Path) -> None:
    request = ResearchRequest(topic="Evidence driven writing")
    first = create_run_workspace(request, tmp_path, now=FIXED, run_id="first-run")
    second = create_run_workspace(
        request, tmp_path, now=FIXED + timedelta(seconds=7), run_id="second-run"
    )
    assert content_path(first.root) == "output/2026-10-01-08-30-00-content.md"
    assert content_path(second.root) == "output/2026-10-01-08-30-07-content.md"


def test_invalid_topic_creates_no_directory(tmp_path: Path) -> None:
    with pytest.raises(ValidationError):
        ResearchRequest(topic="ab")
    assert list(tmp_path.iterdir()) == []
