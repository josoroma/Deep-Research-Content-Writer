# analyst_agent — contract

## Input

Saved topic/optional goal (`ResearchRequest`), every corpus source and index, run ID, input fingerprint, and the supplied `Synthesis` schema.

## Output

`research/synthesis.json`, validated before the coordinator renders `research/summary.md` and records Synthesize completion. Findings have real source excerpts, qualifications and disagreements; the outline is adaptive.

The analyst calls the read-only `validate_synthesis` tool before returning and corrects reported errors. The application coordinator independently validates the handoff and owns phase completion and attempt reservations.

## Success criteria

| Criterion | Source |
| --- | --- |
| Select a useful format from topic, goal, and evidence; read every source | PRD.md FR-7; SPECS.md PD-015 |
| Preserve qualifications, conflicts, and gaps; source excerpts resolve | PRD.md FR-7, FR-9 |
| Record outline, optional diagram plan, and concise cited rationale | PRD.md FR-7, FR-8 |

## Failure conditions

Invalid identity/fingerprint, schema, outline, source references, or excerpts fail with `synthesis_invalid`. One synthesis retry is persisted. Write cannot start before validation. Version-2 failures never fall back to legacy checks.
