# Synthesis summary — RAG vs fine-tuning

- **Run ID:** rag-vs-fine-tuning-20261009T203530Z
- **Topic:** RAG vs fine-tuning
- **Input fingerprint:** `3203f9afdde9d3cd6e72f4ab4b3359f82e85b40739b7e37009338a7806da0c33`
- **Contract version:** 2
- **Authoritative artifact:** `research/synthesis.json` (this file is a rendered summary)
- **Corpus considered:** 15 sources — S-01, S-03, S-05, S-06, S-07, S-08, S-09, S-10, S-14, S-17, S-20, S-22, S-23, S-26, S-28
- **Objective origin:** explicit (caller supplied the goal)

## Reader objective

Decide, for a specific enterprise AI assistant, whether to build on RAG, fine-tuning, or a combined
architecture, by weighing data freshness, evaluation approach, latency, cost and total cost of
ownership, and security/privacy/governance — while knowing which of those comparisons the collected
evidence can and cannot support.

## Format decision

**Evidence-graded comparison decision brief, organised by the five comparison axes the reader named** (confidence: strong).

Why: thirteen of fifteen sources are themselves RAG-vs-fine-tuning comparisons and the strongest usable
material is tabular, checklist-shaped, or claim-based rather than procedural or measured. Walking the
reader's own axes lets each criterion be judged separately and keeps qualification/contradiction
evidence beside the claim it limits; it also gives an explicit home for an evidence-quality section so
vendor figures are reported as claims, not converted into a ranking.

Alternatives rejected: structured literature review (no peer-reviewed source, no independent benchmark);
implementation tutorial (procedural detail fragmentary and uneven); ranked "which one wins" scorecard
(no shared metric, percentage claims lack methodology — would be unsupported); chronological timeline
(no dated capability shifts reported).

## Findings (20)

### Freshness and the core distinction
- **F-01** Every source addressing knowledge currency agrees directionally: RAG supplies current knowledge at query time without retraining; fine-tuning freezes knowledge into weights until the next training run. *(S-08, S-14, S-28, S-09, S-05)*
- **F-02** The corpus's deciding distinction: RAG changes what the model can *see*; fine-tuning changes how it *behaves*. Choosing fine-tuning to add knowledge is named as the most common architectural error. *(S-05, S-08, S-09, S-28, S-14)*
- **F-03** Counter-position: fine-tuning on moving facts fails silently — confident, correct-sounding, stale answers with no error signal — and two sources claim it can increase hallucination on knowledge tasks. *(S-14, S-09, S-28 contradicts, S-08 contradicts)*

### Evaluation
- **F-07** Evaluation guidance is RAG-centric: fixed query set with expected answers, re-run after every pipeline change, reranker/retrieval metrics; fine-tuning gets a held-out validation set; hybrid retrieval adds recall/precision/faithfulness. *(S-05, S-10, S-22)*
- **F-08** One source reframes evaluation economically: quality-per-dollar, a weighted quality/cost/latency composite, percentile latency over days — with caveats that routing can hide edge-case failures. *(S-17)*
- **F-19** RAG accuracy is bounded by retrieval quality (chunking, index freshness, reranker, context size), so choosing RAG means committing to a maintained, evaluated retrieval pipeline. *(S-06, S-10, S-07, S-17, S-05)*

### Latency
- **F-04** Direction is agreed (retrieval adds per-query penalty; internalised behaviour avoids lookup), but only one numeric budget exists (50–200 ms), and mitigation advice comes from a short community answer. *(S-08, S-01, S-06, S-07, S-14, S-20 qualifies)*

### Cost
- **F-05** Cost shapes are opposite: cheap-to-start plus ongoing per-query/index cost versus high upfront training plus cheap predictable per-query serving and recurring retraining. Crossover described qualitatively. *(S-05, S-08, S-09, S-07)*
- **F-06** Published figures conflict by orders of magnitude and lack stated methods; usable as sanity-check ranges only, not budgeting inputs. *(S-05, S-09 contradicts, S-03 qualifies, S-17 qualifies, S-08 qualifies)*

### Security, privacy, governance
- **F-09** Dominant governance argument favours RAG (citation, purge, lineage); one source reverses it, arguing fine-tuning limits leakage via data control. Not reconciled anywhere in the corpus. *(S-08, S-09, S-07, S-01 contradicts, S-28 qualifies)*

### Hybrid
- **F-10** RAG + fine-tuning (RAFT; "behaviour in weights, knowledge in context") is presented as the enterprise default, with differing mechanics across sources. *(S-08, S-07, S-14, S-09, S-26)*
- **F-11** "Hybrid" means two unrelated things: retrieval-modality fusion (S-22, S-23) versus RAG-plus-fine-tuning (S-07, S-10); fusion benchmarks do not transfer to this decision. *(S-22, S-23, S-10, S-09 qualifies)*
- **F-20** Hybrids are not free: added complexity, orchestration latency, drift management, broader monitoring, and a reintroduced retraining obligation. *(S-22, S-10, S-09, S-23, S-05)*

### Decision conditions and risks
- **F-12** Decision checklists converge: prompt first, volatile/citable knowledge → RAG, behaviour/format/stable domain → fine-tuning, both → combined. *(S-07, S-05, S-08, S-09, S-28)*
- **F-13** Numeric gates conflict (>10,000 labelled examples vs "a few thousand"); one source denies any universal rule; none derived from published experiments. *(S-05, S-14 contradicts, S-08 qualifies)*
- **F-14** Two bounding failure modes: RAG fails on cross-domain reasoning and behaviour shaping; fine-tuning fails on drifting facts. *(S-14, S-08, S-09)*
- **F-15** Strongest practical case for starting with RAG is reversibility and time to production; supporting figures are assertions/ranges. *(S-14, S-08, S-09)*
- **F-16** Recurring fine-tuning risks: catastrophic forgetting, overfitting on small/narrow data, adapter/version sprawl. *(S-08, S-07, S-01, S-10)*
- **F-17** Sources disagree on whether a default exists at all (80–90% / 70-20-10 claims vs "the binary framing is the mistake"). *(S-20, S-09, S-05, S-14 contradicts, S-07 contradicts)*

### Evidence quality
- **F-18** All quantified performance claims are vendor/agency/consultancy sourced, sometimes borrowing AWS/IBM authority second-hand; no independently reproduced head-to-head benchmark exists. *(S-08, S-09, S-23, S-07, S-03)*

## Outline

| section_id | level | title | findings |
| --- | --- | --- | --- |
| frame | H2 | The choice is three options and one distinction | F-02, F-10, F-17 |
| freshness | H2 | Data freshness: what happens when the facts move | F-01, F-03 |
| freshness-runtime | H3 | RAG reads the current source at query time | F-01 |
| freshness-staleness | H3 | Fine-tuning goes stale silently — and may get worse, not better | F-03 |
| evaluation | H2 | Evaluation: what to measure before you commit | F-07, F-08, F-19 |
| eval-retrieval | H3 | Measuring retrieval- and grounding-side quality | F-07, F-19 |
| eval-cost-latency | H3 | Scoring quality against cost and latency, not accuracy alone | F-08 |
| latency | H2 | Latency: the retrieval tax, and how large it actually is | F-04 |
| cost | H2 | Cost and total cost of ownership | F-05, F-06 |
| cost-shape | H3 | Opposite cost shapes: pay to operate versus pay to change | F-05 |
| cost-figures | H3 | Published figures disagree by orders of magnitude | F-06 |
| security | H2 | Security, privacy, and governance | F-09 |
| hybrid | H2 | Hybrid architectures: what the sources actually mean | F-10, F-11, F-20 |
| hybrid-raft | H3 | RAFT and 'behaviour in weights, knowledge in context' | F-10 |
| hybrid-naming | H3 | Two different things are called 'hybrid' here | F-11 |
| hybrid-cost | H3 | What the combination costs you in maintenance and latency | F-20 |
| decision | H2 | Conditions that point to each option | F-12, F-13, F-14, F-15, F-16 |
| decision-tests | H3 | The question sequence the sources converge on | F-12, F-13 |
| decision-failure-modes | H3 | Where each option fails, so you can plan the failure | F-14 |
| decision-reversibility | H3 | Reversibility, time to production, and the risks you take on | F-15, F-16 |
| evidence-quality | H2 | How much weight these sources can carry | F-18, F-17 |
| open-questions | H2 | What this corpus does not settle | F-18 |

## Diagram plan (1)

- **decision-routing-flow** — flowchart in `decision-tests`, findings F-02 / F-12 / F-10: shows the order in which the corpus's decision questions are asked and where each answer points, with sources cited per step. Branch conditions are qualitative; the two data-volume thresholds (>10,000 vs "a few thousand") are shown as unreconciled.

## Limitations (10) and gaps (8)

Highlights: 12 of 15 sources are vendor/agency/consultancy/institute content marketing and only S-14 reads as an independent practitioner account; S-20 (~360 words, community Q&A) and S-28 (~454 words, vendor note with a "not legal or compliance advice" disclaimer) carry little weight; quantified figures lack methods and conflict; no independent reproducible head-to-head benchmark; no measured security/compliance outcomes; publication dates span 2024-04 to 2026-07, so older sources may understate current parameter-efficient fine-tuning feasibility; percentage-of-cases claims cannot be aggregated or turned into a recommendation.
Named gaps: no measured TCO for a defined workload; no latency comparison of a hybrid versus pure RAG or pure fine-tuning; no evidence on how fine-tuning and retrieval interact in production; no failure-rate/incident-cost/rollback data behind the reversibility argument; no shared evaluation methodology; no comparison of retrieval-fusion hybrids against RAG-plus-fine-tuning hybrids; no guidance on which behaviours or document slices to fine-tune; no direct regulator or auditor guidance cited.

## Closing rationale

A criterion-by-criterion brief is what the corpus dictates: most of its strongest passages are already
tabular or checklist-shaped, and evidence quality is uneven in a specific way — the freshness,
behaviour-vs-knowledge, and hybrid-design claims repeat consistently across sources, while numeric
claims (cost, latency, accuracy, hallucination reduction) are single-source, method-free vendor figures
that contradict each other. An explicit evidence-quality section lets the brief hold both kinds of
material honestly; a ranked scorecard could not, and the caller's goal rules one out. Evaluation is the
thinnest axis (mainly S-17 and S-22), and "hybrid" is overloaded, so both get separated treatment. The
brief ends where the evidence ends: a routing the reader can apply, plus what must be settled by their
own pilot.
