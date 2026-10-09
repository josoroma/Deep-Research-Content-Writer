# Evidence-driven authoring implementation

Date: 2026-10-09, America/Costa_Rica. Based on the [implementation plan](../workspace/plan/EVIDENCE-DRIVEN-AUTHORING.md) and [ADR 0012](../adr/0012-evidence-driven-authoring.md).

## Delivered behavior

The API and CLI accept an optional trimmed `goal` of up to 1000 characters. Null/blank goals preserve topic-only idempotency hashes. Goal survives stored job reconstruction, request persistence, author-only execution, and resume. Existing requests cannot silently change their goal during workspace reuse.

Synthesize reads the corpus and writes typed `research/synthesis.json`: findings with exact supporting/qualifying/contradicting source excerpts, reader objective, source assessment and gaps, descriptive format decision, adaptive H2/H3 outline, optional diagram plan, and closing rationale. The coordinator validates identity and corpus fingerprints and renders `research/summary.md` before invoking Write.

Write follows the chosen outline once. A Markdown parser handles real headings, nested/duplicate/non-ASCII titles, inline formatting, and code fences. Finalization derives TOC and reference entries from the actual document and corpus metadata. The final envelope is title → TOC → adaptive body → References → Why this format. References includes citations in the last rationale and diagram captions.

The worker, full CLI, author-only milestone, and actual CLI resume share authoring rules. Versioned state reserves synthesis, generation, and citation-repair attempts before model work. Resume reuses validated artifacts, rejects changed inputs/decisions, and reconciles complete drafts after interrupted acknowledgements. Ambiguous attempts report `authoring_interrupted` rather than regenerate. Agents cannot overwrite coordinator-owned request or reservation files. Legacy version-1 runs retain compatible prompts/checks.

Source-aware evaluation now supplies bounded relevant source excerpts, including multi-source claims. TOC/References do not inflate source coverage or claim counts. A separate evaluation assesses goal fit, format fit, and preservation of nuance. Offline scripted verdicts are explicitly labeled fixture assessments.

## Reviewing different goals

The focused authoring fixtures use the same deployment-choice topic and two source passages: one describes local deployment, the other a hosted service, and neither establishes a cross-workload performance ranking. They exercise these different organizations:

| Reader goal | Chosen fixture format | Body outline |
| --- | --- | --- |
| Choose a framework | Qualified comparison | Decision criteria → What is comparable → Unknowns |
| Learn execution | Conceptual tutorial | Prerequisites → Understand execution → Limits of this guide |
| No supplied goal | Literature review with an inferred objective | Review method → Published findings → Review limitations |

These scripted choices verify that arbitrary useful outlines and goals survive the handoff. They do not demonstrate autonomous format selection by a live model. The analyst prompt requires a qualified conceptual guide when evidence cannot support runnable steps, and separates literature review methods from original experiments.

## Optional diagram setup

Run `make setup-diagrams` with Node.js 22 to install the locked Mermaid CLI. Development setup and CI install it for rendering tests. The manifests ship inside `services/mermaid` in the wheel; installed-package users run npm against that directory. Normal research without diagrams does not invoke Node.

Supported initial diagram kinds are Mermaid flowcharts and sequence diagrams. Each requires its planned ID, placement, cited prose caption, and successful local SVG rendering. Rendering has a 30-second timeout and an input-size limit. SVG checks use temporary files; the final document keeps the Mermaid block and readable caption. The KaTeX transitive dependency is pinned to the patched 0.18.2 release.

## Verification

The final document is `output/{yyyy-mm-dd-hh-mm-ss}-content.md`, dated by the run's UTC start. The coordinator persists `content_started_at` in `output/authoring_state.json`; repair and resume retain it. Existing `blog_path` fields in CLI/API records point to this path. Download clients should read the reported path or artifact `download_url` instead of calculating today's date.

Tests include custom comparison/tutorial/review outlines, contradictory evidence, goal validation/hashing and HTTP/CLI handoffs, nested headings, navigation/reference integrity, real diagram rendering, changed input rejection, single-generation reconciliation, and persistent repair limits. Filename checks cover second precision, UTC date rollover, custom run IDs, resumed research, reported artifact downloads, and safe failure reporting when authoring state is malformed. Legacy budget import also preserves citation repairs recorded before the versioned state file existed.

| Check | Result |
| --- | --- |
| Focused authoring tests | 45 passed |
| `make check` | Passed: locked dependencies, Ruff lint/format, strict typing across 154 files, 786 tests (3 live tests deselected), 87.95% coverage |
| `make boundary` | Passed |
| `make build` | Wheel and source distribution built successfully |
| Wheel inspection | New contracts, versioned prompts, and renderer manifests present; `node_modules` excluded |
| `make eval-offline` | All three fixture topics passed; editorial assessments explicitly use `fixture` mode |
| Renderer dependency audit | Zero known vulnerabilities reported by `npm audit` |

Offline evaluation ran with `EVAL_RUNS_ROOT=/tmp/evidence-authoring-eval/runs` and `EVAL_BENCHMARKS_DIR=/tmp/evidence-authoring-eval/benchmarks`, outside the repository's historical benchmarks. The benchmark records the base commit `f0eea9a`; implementation changes were uncommitted during verification.

No live search, model evaluation, hosted worker, or deployment is part of this implementation verification. Offline scripted models prove contracts and execution behavior; they do not establish a production model's editorial quality.
