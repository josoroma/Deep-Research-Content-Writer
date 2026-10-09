# writer_agent — contract

## Input

Saved topic/optional goal (`ResearchRequest`), immutable sources, validated synthesis, rendered summary, and any bounded citation-repair request.

## Output

`output/{yyyy-mm-dd-hh-mm-ss}-content.md`: one title, generated TOC, adaptive H2/H3 outline, References, and a final cited Why this format explanation. The coordinator supplies the concrete path using the saved UTC run start time; the writer retains it during repairs and resumes. Existing `blog_path` fields carry this dated path. Planned optional Mermaid diagrams include cited prose captions and pass rendering.

## Success criteria

| Criterion | Source |
| --- | --- |
| Follow the evidence-backed outline and preserve material nuance | PRD.md FR-8; SPECS.md PD-015 |
| Working TOC at the top; References and final format rationale at the end | PRD.md FR-8 |
| Every factual claim cites supporting corpus evidence | PRD.md FR-9 |
| Generate once; keep the soft 2000–5000 word target without filler | SPECS.md PD-015 |
| At most two citation repairs across resume | SPECS.md PD-016 |

## Failure conditions

Invalid structure records `blog_structure`; diagram failures record `diagram_invalid`. Invalid citations after two passes record `dangling_citations`. Out-of-range length records `blog_length` and preserves the draft. Ambiguous generation/repair records `authoring_interrupted` without automatically repeating model work. Legacy runs retain compatible prompts/checks.
