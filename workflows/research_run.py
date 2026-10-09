"""Run research through the same shared use case as the HTTP worker."""

from pathlib import Path
from typing import Any, Literal

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage
from langgraph.graph.state import CompiledStateGraph

from application.context import ExecutionContext
from application.run_service import RunService
from schemas.common import Contract
from schemas.config import RunSettings
from schemas.requests import ResearchRequest
from schemas.search import QueryVariants
from schemas.state import RunState
from schemas.workspace import RunWorkspace
from services.content_paths import content_path
from services.extraction_service import ExtractionService
from services.fetch_service import Fetcher, crawler_user_agent
from services.llm_service import LLMService
from services.observability import (
    observed_config,
    observed_workflow,
)
from services.search_provider import SearchProvider, create_search_provider
from services.synthesis import saved_request
from services.workspace import create_run_workspace
from workflows.resume import load_saved_run


class RunSummary(Contract):
    """What the run command prints on exit."""

    run_id: str
    workspace: str
    status: Literal["completed", "degraded", "failed"]
    blog_path: str
    blog_exists: bool
    error: str | None = None
    status_reasons: list[str] = []


@observed_workflow("research")
def run_research(
    request: ResearchRequest,
    settings: RunSettings,
    *,
    runs_root: Path,
    fake_model: BaseChatModel | None = None,
    search_provider: SearchProvider | None = None,
    fetcher: Fetcher | None = None,
    extractor: ExtractionService | None = None,
    variants: QueryVariants | None = None,
) -> RunSummary:
    """Execute the same validated research pipeline as the HTTP worker."""
    llm = LLMService(settings, fake_model=fake_model)
    llm.for_agent("orchestrator")
    provider = search_provider if search_provider is not None else create_search_provider(settings)
    provider.preflight(request.per_page)
    if fetcher is None:
        crawler_user_agent(settings)
    workspace = create_run_workspace(request, runs_root)
    context = ExecutionContext.open(
        run=RunState(run_id=workspace.run_id, topic=request.topic),
        workspace=workspace,
        settings=settings,
        search_provider=provider,
        llm=llm,
        fetcher=fetcher,
        extractor=extractor,
        variants=variants,
        pages=request.pages,
        per_page=request.per_page,
        max_urls=request.max_urls,
    )
    try:
        outcome = RunService(context, production=fake_model is None).execute()
    finally:
        context.close()
    status: Literal["completed", "degraded", "failed"] = "failed"
    if outcome.status == "succeeded":
        status = "completed"
    elif outcome.status == "degraded":
        status = "degraded"
    blog = workspace.root / content_path(workspace.root)
    return RunSummary(
        run_id=workspace.run_id,
        workspace=str(workspace.root),
        status=status,
        blog_path=str(blog),
        blog_exists=blog.exists(),
        error=outcome.error,
        status_reasons=outcome.status_reasons,
    )


def invoke_agent(
    agent: CompiledStateGraph[Any, Any, Any, Any], request: ResearchRequest, settings: RunSettings
) -> dict[str, Any]:
    """Invoke a built agent with the validated request as its initial message."""
    return agent.invoke(
        {"messages": [HumanMessage(content=request.model_dump_json())]},
        config=observed_config(settings.recursion_limit),
    )


@observed_workflow("resume")
def resume_research(workspace: Path, settings: RunSettings) -> RunSummary:
    """Continue the same persisted request and phase/attempt budgets via the CLI."""
    request, run = saved_request(workspace), load_saved_run(workspace)
    context = ExecutionContext.open(
        run=run,
        workspace=RunWorkspace(root=workspace, run_id=run.run_id),
        settings=settings,
        search_provider=create_search_provider(settings),
        llm=LLMService(settings),
        pages=request.pages,
        per_page=request.per_page,
        max_urls=request.max_urls,
    )
    try:
        outcome = RunService(context).resume()
    finally:
        context.close()
    status: Literal["completed", "degraded", "failed"] = "failed"
    if outcome.status == "succeeded":
        status = "completed"
    elif outcome.status == "degraded":
        status = "degraded"
    return RunSummary(
        run_id=run.run_id,
        workspace=str(workspace),
        status=status,
        blog_path=str(workspace / content_path(workspace)),
        blog_exists=(workspace / content_path(workspace)).is_file(),
        error=outcome.error,
        status_reasons=outcome.status_reasons,
    )
