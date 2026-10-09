"""Idempotent TOC/reference rendering and adaptive document validation."""

import re
from pathlib import Path

from schemas.authoring import Synthesis
from schemas.errors import AuthoringError
from services.artifacts import write_text
from services.content_paths import content_path
from services.corpus import read_corpus
from services.markdown_document import headings, remove_sections, sections, table_of_contents
from services.synthesis import SOURCE_CITATION


def reference_entries(root: Path, text: str) -> str:
    """Render known cited sources once; unknown IDs stay visible to the gate."""
    corpus = {record.source.source_id: record.source for record in read_corpus(root)}
    cited = dict.fromkeys(SOURCE_CITATION.findall(text))
    lines = [f"- [{sid}] {corpus[sid].title} — {corpus[sid].url}" for sid in cited if sid in corpus]
    return "## References\n\n" + "\n".join(lines) + "\n"


def finalize_document(root: Path, plan: Synthesis) -> None:
    """Add navigation and references without another model generation."""
    path = root / content_path(root)
    if not path.is_file():
        raise AuthoringError("Writer produced no document", code="blog_structure")
    text = remove_sections(path.read_text(encoding="utf-8"), {"Table of contents", "References"})
    found = headings(text)
    if not found or found[0].level != 1 or found[0].start != 0:
        raise AuthoringError("Document must begin with a title", code="blog_structure")
    rationale = next((item for item in found if item.title == "Why this format"), None)
    if rationale is None:
        text = text.rstrip() + f"\n\n## Why this format\n\n{plan.closing_rationale}\n"
        rationale = headings(text)[-1]
    lines = text.splitlines(keepends=True)
    before = "".join(lines[: rationale.start]).rstrip()
    after = "".join(lines[rationale.start :]).strip()
    text = before + "\n\n" + reference_entries(root, text) + "\n" + after + "\n"
    lines = text.splitlines(keepends=True)
    title_end = headings(text)[0].end
    text = (
        "".join(lines[:title_end]).rstrip()
        + "\n\n"
        + table_of_contents(text)
        + "\n"
        + "".join(lines[title_end:]).lstrip()
    )
    write_text(path, text)


def document_violations(text: str, plan: Synthesis) -> list[str]:
    """Validate the envelope and selected outline, including navigation integrity."""
    found = headings(text)
    expected = [(1, found[0].title if found else ""), (2, "Table of contents")]
    expected.extend(
        (item.level, headings(f"{'#' * item.level} {item.title}")[0].title) for item in plan.outline
    )
    expected.extend([(2, "References"), (2, "Why this format")])
    violations = []
    if [(item.level, item.title) for item in found] != expected:
        violations.append("heading_outline")
    if not found or found[0].start != 0:
        violations.append("title_position")
    bodies = {(level, title): body for level, title, body in sections(text)}
    toc = bodies.get((2, "Table of contents"), "").strip()
    if toc != table_of_contents(text).split("\n\n", 1)[1].strip():
        violations.append("table_of_contents")
    if len(found) > 1:
        lines = text.splitlines()
        if any(line.strip() for line in lines[found[0].end : found[1].start]):
            violations.append("toc_position")
    rationale = bodies.get((2, "Why this format"), "").strip()
    if not rationale:
        violations.append("format_rationale")
    violations.extend(_body_violations(text, plan))
    reference_ids = re.findall(r"^[-*]\s+\[(S-\d{2,})\]", bodies.get((2, "References"), ""), re.M)
    if len(reference_ids) != len(set(reference_ids)):
        violations.append("duplicate_references")
    return violations


def _body_violations(text: str, plan: Synthesis) -> list[str]:
    found, lines = headings(text), text.splitlines()
    violations: list[str] = []
    for index, item in enumerate(found[2:-2], 2):
        end = next(
            (other.start for other in found[index + 1 :] if other.level <= item.level), len(lines)
        )
        section_body = "\n".join(lines[item.end : end]).strip()
        if not section_body:
            violations.append("empty_section")
        if (
            index - 2 < len(plan.outline)
            and plan.outline[index - 2].finding_ids
            and not SOURCE_CITATION.findall(section_body)
        ):
            violations.append("section_citations")
    return violations
