"""Run the shared, durable synthesis/write/citation pipeline for a corpus."""

import json
from pathlib import Path
from typing import Any

from langchain_core.messages import HumanMessage
from langgraph.checkpoint.base import BaseCheckpointSaver

from agents.deep_research import build_deep_agent
from schemas.authoring import AuthoringResult as AuthoringSummary
from schemas.config import RunSettings
from schemas.errors import ResearchError
from schemas.state import RunState
from schemas.tool_io import ValidateCitationsOutput
from schemas.workspace import RunWorkspace
from services.artifacts import write_json
from services.authoring import validate_citations
from services.authoring_pipeline import AuthoringPipeline, Stage, StageInvoker
from services.content_paths import content_path
from services.llm_service import LLMService
from services.observability import bind_workspace, observed_config, observed_workflow
from services.synthesis import authoring_state
from tools.authoring_tools import AuthoringSession
from tools.registry import create_tool_registry

MAX_REPAIR_PASSES = 2
GATE_REPORT = "output/authoring.json"
__all__ = ["AuthoringSummary", "load_corpus_run", "run_authoring", "validate_now"]


def load_corpus_run(workspace: Path) -> RunState:
    """Load the authoritative progress saved after corpus collection."""
    return RunState.model_validate(json.loads((workspace / "corpus_state.json").read_text()))


def validate_now(workspace: Path) -> ValidateCitationsOutput:
    """Inspect citations without recording phase completion."""
    finding = validate_citations(workspace)
    return ValidateCitationsOutput(**finding.model_dump(), run=load_corpus_run(workspace))


def _agent_invoker(
    workspace: Path,
    run: RunState,
    settings: RunSettings,
    service: LLMService,
    checkpointer: BaseCheckpointSaver[Any] | None,
) -> StageInvoker:
    agent = build_deep_agent(
        service,
        RunWorkspace(root=workspace, run_id=run.run_id),
        tool_registry=create_tool_registry(authoring_session=AuthoringSession(workspace, run)),
        checkpointer=checkpointer,
        authoring_version=authoring_state(workspace).contract_version,
    )

    def invoke(stage: Stage, prompt: str, current: RunState) -> None:
        state = authoring_state(workspace)
        attempt = state.synthesis_attempts if stage == "synthesize" else 1
        if stage == "repair":
            attempt = state.repair_passes
        thread_id = run.run_id
        if state.contract_version == 2:
            thread_id = f"{run.run_id}:{stage}:{attempt}"
        config = observed_config(settings.recursion_limit)
        config["configurable"] = {"thread_id": thread_id}
        agent.invoke({"messages": [HumanMessage(content=prompt)], "run": current}, config=config)

    return invoke


@observed_workflow("authoring")
def run_authoring(
    workspace: Path,
    settings: RunSettings,
    *,
    llm: LLMService | None = None,
    checkpointer: BaseCheckpointSaver[Any] | None = None,
    invoke: StageInvoker | None = None,
) -> AuthoringSummary:
    """Resume validated stages, reserve model attempts, and preserve failed drafts."""
    run = load_corpus_run(workspace)
    bind_workspace(workspace, run.topic)
    pipeline: AuthoringPipeline | None = None
    result = AuthoringSummary(run_id=run.run_id, workspace=str(workspace))
    try:
        callback = invoke or _agent_invoker(
            workspace, run, settings, llm or LLMService(settings), checkpointer
        )
        pipeline = AuthoringPipeline(workspace, run, callback)
        result = pipeline.execute()
    except Exception as error:  # noqa: BLE001 - isolation boundary records safe failure details
        if pipeline is not None:
            result = pipeline.result
            result.repair_passes = pipeline.state.repair_passes
        result.status = "failed"
        result.reason = error.code if isinstance(error, ResearchError) else "phase_failed"
        result.error = type(error).__name__
        path = content_path(workspace)
        result.blog_path = path if (workspace / path).exists() else None
    (workspace / "output").mkdir(exist_ok=True)
    write_json(workspace / GATE_REPORT, result.model_dump(mode="json"))
    return result
