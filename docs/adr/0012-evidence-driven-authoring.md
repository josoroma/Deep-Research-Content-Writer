# 0012 — Evidence-driven authoring with a versioned synthesis contract

Date: 2026-10-09. Status: accepted for this implementation.

## Context

The analyst and writer prompts, validators, and product requirements imposed fixed headings. Topic and evidence could not determine the output structure. The optional reader goal also had no request field. Citation validity checked source identity rather than semantic support, and synthesis/write/repair progress needed durable stage boundaries.

## Decision

New workspaces use authoring version 2. Carry optional normalized `goal` through API/CLI admission, payload hashing, persistence, author-only execution, and resume. Preserve topic-only idempotency hashes by omitting empty goals from canonical job payloads.

The analyst writes a typed `research/synthesis.json` containing findings, exact evidence excerpts, qualifications/conflicts, gaps, a descriptive format decision, an adaptive H2/H3 outline, optional diagrams, and a closing editorial rationale. Validate the plan against request/corpus fingerprints before rendering `research/summary.md` and invoking Write.

The shared authoring pipeline reserves attempts before model calls. Generate the document once, derive TOC/References deterministically, and finish with Why this format. Use source-aware claim and structure judges during evaluation, distinct from deterministic structural/provenance gates. Optional Mermaid flowcharts/sequences must render with the locked local CLI and carry cited descriptions.

Version-1 runs without a marker retain compatible prompts/checks. Invalid version-2 artifacts never select legacy behavior. The CLI and worker share execution rules; CLI resume now performs continuation.

## Consequences

Custom and hybrid outlines are allowed without losing inspectable evidence and navigation requirements. Changes to prompts, schemas, validators, fixtures, and product docs must remain coordinated. Source excerpts establish provenance, not proof of semantic support. Offline scripted judges verify wiring; real semantic quality still needs source-aware model evaluation.

The renderer adds an optional Node.js 22 installation for runtime diagrams and a required development/CI dependency for rendering tests. Its manifests ship with the Python package. Ambiguous model attempts preserve the draft and reservations and report `authoring_interrupted`; the pipeline does not silently regenerate.
