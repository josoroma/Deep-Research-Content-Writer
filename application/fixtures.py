"""Deterministic fake providers and tools for the server fixture profile.

Selecting ``API_RUN_PROFILE=fixture`` swaps in these fakes at the worker boundary
only. They make no model, search or website calls, so an integration check can
exercise the real database, API process and worker without a network or keys.
Clients cannot enable this profile in a request.
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

from pydantic import HttpUrl

from evaluations.authoring_fixtures import fixture_draft, fixture_plan
from evaluations.fakes import ScriptedChatModel
from schemas.content import ExtractionResult, FetchResult, ParserAttempt, utc_now
from schemas.responses import FetchedPage, SearchResult, Source
from schemas.search import QueryVariants
from schemas.tool_io import ExtractMarkdownInput
from services.artifacts import write_json, write_text
from services.authoring_pipeline import Stage
from services.content_paths import content_path
from services.extraction_service import ExtractionService
from services.search_provider import FakeSearchProvider
from services.synthesis import validate_synthesis

FIXTURE_WORDS = 320


def fixture_search_pages(
    topic: str, *, pages: int, per_page: int
) -> Mapping[tuple[str, int], list[SearchResult]]:
    """Ten results per primary topic page; variant queries legitimately return none."""
    results: dict[tuple[str, int], list[SearchResult]] = {}
    for page in range(1, pages + 1):
        offset = (page - 1) * per_page
        results[(topic, page)] = [
            SearchResult(
                url=HttpUrl(f"https://fixture.test/article-{offset + index}"),
                title=f"Fixture source {offset + index}",
                snippet="Server fixture result",
                rank=offset + index,
                query=topic,
            )
            for index in range(1, per_page + 1)
        ]
    return results


class FixtureExtractionService(ExtractionService):
    """Produce a valid, long-enough source without parsing anything.

    Subclassing the real service keeps the tool boundary's type honest while the
    deterministic body avoids any parser or network call.
    """

    def __init__(self) -> None:
        """Register a single no-op parser so the base class invariants hold."""
        super().__init__((_FixtureExtractor(),))

    def extract(self, request: ExtractMarkdownInput) -> ExtractionResult:
        """Return a fixed, valid source for ``request.source_id``."""
        body = " ".join(["fixture-evidence"] * FIXTURE_WORDS)
        source = Source(
            source_id=request.source_id,
            url=request.page.final_url,
            title=f"Fixture source {request.source_id}",
            author=None,
            published=None,
            body_markdown=f"# Fixture source {request.source_id}\n\n{body}\n",
            word_count=FIXTURE_WORDS,
            fetched_at=request.fetched_at,
        )
        return ExtractionResult(
            outcome="extracted",
            source=source,
            attempts=[
                ParserAttempt(parser="fixture", outcome="extracted", word_count=FIXTURE_WORDS)
            ],
        )


class _FixtureExtractor:
    """A no-op extractor so the base service has at least one parser."""

    name = "fixture"

    def extract(self, page: FetchedPage) -> None:
        """Decline every page; the fixture service never reaches this parser."""
        del page


class FixtureFetcher:
    """A synchronous fetcher returning a fixed HTML page for every URL."""

    def fetch(self, url: HttpUrl) -> FetchResult:
        """Return a successful fetch of a fixed page without any network call."""
        html = "<html><head><title>Fixture</title></head><body><p>fixture</p></body></html>"
        page = FetchedPage(html=html, status=200, final_url=url)
        return FetchResult(
            url=url,
            final_url=url,
            outcome="fetched",
            page=page,
            attempts=1,
            status=200,
            fetched_at=utc_now(),
        )


def fixture_model() -> ScriptedChatModel:
    """A scripted model for the fixture profile; prompts are ignored."""
    return ScriptedChatModel(script=[])


def fixture_search_provider(topic: str, *, pages: int, per_page: int) -> FakeSearchProvider:
    """Build an offline provider whose pages are derived from ``topic``."""
    return FakeSearchProvider(fixture_search_pages(topic, pages=pages, per_page=per_page))


def fixture_variants() -> QueryVariants:
    """Two deterministic variants that differ from any topic, for the fixture profile."""
    return QueryVariants(
        variants=["fixture framework architecture comparison", "fixture production evaluation"]
    )


def fixture_authoring(root: Path, stage: Stage = "synthesize") -> None:
    """Write only the assigned adaptive fixture stage under the real reservations.

    Args:
        root: A run workspace with collected immutable sources.
        stage: The synthesis, write, or repair stage assigned by the coordinator.
    """
    if stage == "synthesize":
        write_json(root / "research/synthesis.json", fixture_plan(root).model_dump(mode="json"))
    elif stage == "write":
        plan = validate_synthesis(root)
        write_text(root / content_path(root), fixture_draft(plan))
