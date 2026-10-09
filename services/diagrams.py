"""Render optional, evidence-linked Mermaid diagrams with a locked offline CLI."""

import json
import re
import shutil
import subprocess
import tempfile
from functools import lru_cache
from pathlib import Path

from markdown_it import MarkdownIt

from schemas.authoring import Synthesis
from schemas.errors import AuthoringError
from services.markdown_document import headings
from services.synthesis import SOURCE_CITATION

RENDER_TIMEOUT_SECONDS = 30
MAX_DIAGRAM_CHARACTERS = 20000


@lru_cache(maxsize=128)
def _render(code: str) -> None:
    bundled = Path(__file__).with_name("mermaid") / "node_modules/.bin/mmdc"
    executable = str(bundled) if bundled.is_file() else shutil.which("mmdc")
    if executable is None:
        raise AuthoringError(
            "Install the locked Mermaid renderer for diagrams", code="diagram_invalid"
        )
    with tempfile.TemporaryDirectory(prefix="research-diagram-") as temporary:
        directory = Path(temporary)
        source, output = directory / "diagram.mmd", directory / "diagram.svg"
        source.write_text(code, encoding="utf-8")
        config = directory / "config.json"
        config.write_text(json.dumps({"securityLevel": "strict"}), encoding="utf-8")
        try:
            result = subprocess.run(  # noqa: S603 - fixed renderer, argv only, bounded local input
                [executable, "-i", str(source), "-o", str(output), "-c", str(config)],
                capture_output=True,
                timeout=RENDER_TIMEOUT_SECONDS,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as error:
            raise AuthoringError("Mermaid renderer failed", code="diagram_invalid") from error
        if result.returncode or not output.is_file():
            raise AuthoringError("Mermaid diagram does not render", code="diagram_invalid")


def validate_diagrams(text: str, plan: Synthesis) -> None:
    """Check plan IDs, placement, captions, provenance, syntax, and actual rendering."""
    tokens = [
        token
        for token in MarkdownIt("commonmark").parse(text)
        if token.type == "fence" and token.info.strip() == "mermaid"
    ]
    if not tokens and not plan.diagrams:
        return
    found, lines = headings(text), text.splitlines()
    expected = {item.diagram_id: item for item in plan.diagrams}
    seen: set[str] = set()
    for token in tokens:
        if token.map is None:
            raise AuthoringError("Diagram has no placement", code="diagram_invalid")
        start, end = token.map
        before = "\n".join(lines[:start]).rstrip()
        match = re.search(r"<!-- diagram: ([a-zA-Z0-9_-]+) -->$", before)
        identifier = match.group(1) if match else ""
        if identifier not in expected or identifier in seen:
            raise AuthoringError("Unplanned or duplicate diagram", code="diagram_invalid")
        seen.add(identifier)
        diagram = expected[identifier]
        section = next(item for item in plan.outline if item.section_id == diagram.section_id)
        parent = next((item for item in reversed(found) if item.start < start), None)
        title = headings(f"{'#' * section.level} {section.title}")[0].title
        if parent is None or (parent.level, parent.title) != (section.level, title):
            raise AuthoringError("Diagram is in the wrong section", code="diagram_invalid")
        after = "\n".join(lines[end:]).lstrip()
        if not after.startswith(diagram.caption) or not SOURCE_CITATION.findall(diagram.caption):
            raise AuthoringError("Diagram needs its cited prose caption", code="diagram_invalid")
        code = token.content.strip()
        if len(code) > MAX_DIAGRAM_CHARACTERS or not code.startswith(diagram.kind):
            raise AuthoringError("Diagram kind or size is invalid", code="diagram_invalid")
        _render(code)
    if seen != set(expected):
        raise AuthoringError("A planned diagram is missing", code="diagram_invalid")
