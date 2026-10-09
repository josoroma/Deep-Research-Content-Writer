"""Evidence-bearing adaptive fixtures; these test plumbing, not model judgment."""

from pathlib import Path

from schemas.authoring import Evidence, Finding, FormatDecision, OutlineSection, Synthesis
from services.corpus import read_corpus
from services.synthesis import input_fingerprint, saved_request

FIXTURE_TITLES = (
    "Evidence in context",
    "Supported findings",
    "Scope and assumptions",
    "Contrasting perspectives",
    "Practical implications",
    "Open questions",
)


def fixture_plan(
    root: Path,
    *,
    label: str = "Evidence review",
    titles: tuple[str, ...] = FIXTURE_TITLES,
) -> Synthesis:
    """Build a plan with actual excerpts and an arbitrary, editable outline."""
    records, request = read_corpus(root), saved_request(root)
    if not records:
        raise ValueError("Authoring fixture requires a source corpus")
    findings = [
        Finding(
            finding_id=f"finding-{index}",
            statement=record.source.body_markdown[:160],
            evidence=[
                Evidence(
                    source_id=record.source.source_id, excerpt=record.source.body_markdown[:400]
                )
            ],
        )
        for index, record in enumerate(records)
    ]
    outline = [
        OutlineSection(
            section_id=f"section-{index}",
            title=title,
            purpose=f"Explain {title.lower()} using the collected evidence.",
            finding_ids=[item.finding_id for item in findings[index :: len(titles)]]
            or [findings[0].finding_id],
        )
        for index, title in enumerate(titles)
    ]
    return Synthesis(
        run_id=root.name,
        topic=request.topic,
        goal=request.goal,
        input_fingerprint=input_fingerprint(root),
        reader_objective=request.goal or "Understand the available evidence and its limitations.",
        objective_origin="explicit" if request.goal else "inferred",
        considered_source_ids=[item.source.source_id for item in records],
        evidence_types=["Collected source passages"],
        findings=findings,
        outline=outline,
        limitations=["Offline fixtures demonstrate contracts, not editorial quality."],
        format=FormatDecision(label=label, why="The source passages support a qualified overview."),
        closing_rationale=f"This {label.lower()} organizes the available source passages "
        f"around the reader objective [{records[0].source.source_id}].",
    )


def fixture_draft(plan: Synthesis, *, words_per_section: int = 320) -> str:
    """Render a scripted draft with all planned evidence links and closing citations."""
    findings = {item.finding_id: item for item in plan.findings}
    blocks = [f"# {plan.topic}"]
    for section in plan.outline:
        cited = [e.source_id for fid in section.finding_ids for e in findings[fid].evidence]
        body = " ".join(["fixture-evidence"] * words_per_section)
        blocks.append(
            f"{'#' * section.level} {section.title}\n\n{body} "
            + " ".join(f"[{sid}]" for sid in dict.fromkeys(cited))
            + "."
        )
    blocks.append("## Why this format\n\n" + plan.closing_rationale)
    return "\n\n".join(blocks) + "\n"
