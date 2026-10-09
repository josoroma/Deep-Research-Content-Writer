"""Parse actual Markdown headings and derive stable document navigation."""

import re
from dataclasses import dataclass

from markdown_it import MarkdownIt


@dataclass(frozen=True)
class Heading:
    """A heading's plain title, line span, and unique GitHub-style anchor."""

    level: int
    title: str
    start: int
    end: int
    anchor: str


def headings(text: str) -> list[Heading]:
    """Read CommonMark headings, ignoring code fences and inline formatting."""
    tokens = MarkdownIt("commonmark").parse(text)
    result: list[Heading] = []
    used: set[str] = set()
    for index, token in enumerate(tokens):
        if token.type != "heading_open" or token.map is None:
            continue
        inline = tokens[index + 1]
        title = "".join(
            child.content
            for child in inline.children or []
            if child.type in {"text", "code_inline", "image"}
        )
        base = re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-")
        anchor, suffix = base, 0
        while anchor in used:
            suffix += 1
            anchor = f"{base}-{suffix}"
        used.add(anchor)
        result.append(Heading(int(token.tag[1:]), title, token.map[0], token.map[1], anchor))
    return result


def sections(text: str) -> list[tuple[int, str, str]]:
    """Return heading bodies through the next heading, excluding fenced headings."""
    found, lines = headings(text), text.splitlines(keepends=True)
    return [
        (
            item.level,
            item.title,
            "".join(
                lines[item.end : found[index + 1].start if index + 1 < len(found) else len(lines)]
            ),
        )
        for index, item in enumerate(found)
    ]


def remove_sections(text: str, titles: set[str]) -> str:
    """Remove complete level-2 sections, including their nested subsections."""
    found, lines = headings(text), text.splitlines(keepends=True)
    removed: set[int] = set()
    for index, item in enumerate(found):
        if item.level != 2 or item.title not in titles:
            continue
        end = next((other.start for other in found[index + 1 :] if other.level <= 2), len(lines))
        removed.update(range(item.start, end))
    return "".join(line for index, line in enumerate(lines) if index not in removed).strip() + "\n"


def table_of_contents(text: str) -> str:
    """Build navigation from final H2/H3 headings with escaped visible labels."""
    entries = []
    for item in headings(text):
        if item.level not in {2, 3} or item.title == "Table of contents":
            continue
        title = item.title.replace("[", r"\[").replace("]", r"\]")
        entries.append(f"{'  ' if item.level == 3 else ''}- [{title}](#{item.anchor})")
    return "## Table of contents\n\n" + "\n".join(entries) + "\n"


def content_text(text: str) -> str:
    """Prose and table/diagram captions, without navigation, references, or code."""
    cleaned = remove_sections(text, {"Table of contents", "References"})
    tokens = MarkdownIt("commonmark").enable("table").parse(cleaned)
    return "\n".join(
        token.content
        for index, token in enumerate(tokens)
        if token.type == "inline" and (index == 0 or tokens[index - 1].type != "heading_open")
    )
