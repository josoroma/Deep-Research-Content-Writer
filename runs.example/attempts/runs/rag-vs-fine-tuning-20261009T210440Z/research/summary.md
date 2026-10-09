# Synthesis summary — RAG vs fine-tuning

- **Run ID:** rag-vs-fine-tuning-20261009T210440Z
- **Topic:** RAG vs fine-tuning
- **Input fingerprint:** 88fb906939e254068fbe435c72d2409239ec2e5239f1639fccafbe94dfbd70fb
- **Contract version:** 2
- **Objective origin:** explicit
- **Reader objective:** Help an engineering team choose between RAG, fine-tuning, and a hybrid approach for enterprise AI assistants by comparing data freshness, evaluation, latency, cost, and security while preserving evidence limits and avoiding unsupported rankings.
- **Sources considered (14):** S-01, S-03, S-05, S-06, S-09, S-10, S-13, S-15, S-16, S-24, S-25, S-27, S-28, S-30

## Format decision

**Axis-by-axis decision brief (comparative selection guide with explicit evidence-quality caveats)** — confidence: moderate.

The goal is a choice across five named axes (freshness, evaluation, latency, cost, security) plus hybrid, so a decision brief that walks each axis and then offers a conditional decision path serves the reader directly. The corpus supports an axis-by-axis treatment (S-09, S-06, S-13 provide comparison tables) but is vendor-heavy and has no head-to-head benchmark, so the format is built to surface evidence limits and avoid unsupported rankings, matching the warnings in S-09 and S-15 that no approach is universally better.

Alternatives rejected: literature review (only one peer-reviewed study, abstract-only), build tutorial (goal is a selection decision; procedural material is vendor-specific), ranked scorecard (corpus rejects universal rankings and supplies no comparable measurements).

## Findings

| id | statement (abridged) | evidence | qualifications |
| --- | --- | --- | --- |
| F-01 | RAG and fine-tuning are framed as complementary, not rivals: RAG supplies knowledge at query time, fine-tuning changes behaviour via weights. | S-05, S-09, S-06 | Vendor/practitioner framing; conceptual, no controlled head-to-head. |
| F-02 | RAG stays current by updating source data; a fine-tuned model reflects its training snapshot and goes stale. | S-09, S-06, S-01, S-10 | Directional only; assumes the index is maintained. |
| F-03 | The one controlled academic study reports no universal best technique; effectiveness depends on base model and dialogue type, and human evaluation is needed. | S-15, S-16 | S-15/S-16 are the same paper; abstract only; Llama-2/Mistral dialogue study, not enterprise assistants. |
| F-04 | Practitioner sources recommend a fixed, reusable eval set run after every change (100-query set, 1,000+ golden dataset, RAGAS 4-metric). | S-05, S-25, S-27, S-28 | Recommended but unvalidated; sizes/metrics differ between sources. |
| F-05 | RAG adds a retrieval step that increases latency; fine-tuning enables faster responses / shorter prompts. | S-01, S-06, S-10, S-09 | Directional, not measured; no shared-workload benchmark. |
| F-06 | Only concrete latency figures are one vendor's own model timings: ~1–3 s (14B) and ~4 s (72B) for a 200-token answer. | S-24 | Self-reported, generation only, not comparative. |
| F-07 | Inverted cost structure: RAG cheaper to start/maintain; fine-tuning higher upfront but can lower per-query cost at volume. | S-09, S-06, S-05 | Qualitative except a few vendor estimates; no full TCO model. |
| F-08 | Specific cost figures appear only in vendor/practitioner sources with differing scopes (RAG setup, per-query hop + LLM call, LoRA training, GPU hosting, multi-tenant LoRA sharing). | S-05, S-03, S-24 | Commercial interests; non-comparable units; S-03 second-hand. |
| F-09 | RAG is argued to be easier to govern: sensitive content stays in a store you control, fetched per query under your access rules. | S-09, S-10 | Architectural intuition, not audited compliance evidence. |
| F-10 | One source states the opposite: fine-tuning improves data control by limiting which data the model uses. | S-01 (contradicts) | Single source; addresses a different concern; unreconciled. |
| F-11 | Retrieval creates its own attack surface: indirect prompt injection, knowledge-base poisoning, embedding inversion, cross-tenant leakage; defense in depth recommended. | S-28, S-25 | One trade-press article + one vendor whitepaper; RAG-skewed. |
| F-12 | When both fresh knowledge and specific behaviour are needed, combine them; most common advice is prompting + RAG first, add fine-tuning for remaining behaviour gaps. | S-05, S-09, S-25 | Practitioner advice, untested orderings; no quantified hybrid benefit. |
| F-13 | One vendor reports an informal production ratio of ~70% pure RAG, 20% hybrid, 10% pure fine-tuning. | S-05 | Single-vendor anecdote, no methodology; not an industry distribution. |
| F-14 | Fine-tuning fits behaviour problems: consistent style/brand voice, strict output formats (exact JSON), narrow repeated tasks, domain vocabulary. | S-05, S-09, S-25 | No measurement of benefit vs careful prompting. |
| F-15 | The corpus mixes 2024–2026 timeframes; some specific architectural claims are forward-dated vendor assertions naming unverifiable model versions. | S-25, S-06 | Statements not synchronous; model names illustrative. |
| F-16 | Quantitative performance claims are self-reported by commercial vendors with no independent verification (e.g. 95% problem-solving rate; 62/78/85% chunking A/B). | S-24, S-27 | Vendors sell what they benchmark; not reproducible. |

## Outline

1. **The core framing: knowledge versus behaviour** (H2) — F-01
2. **Data freshness: where the design difference shows up first** (H2) — F-02 · *limitation: no quantified freshness/staleness*
3. **Evaluation: how you would know which works** (H2) — F-03, F-04
   - 3.1 Practitioner evaluation patterns and their limits (H3) — F-04 · *limitation: sizes/metrics unjustified*
   - 3.2 The one controlled academic comparison (H3) — F-03 · *limitation: abstract only; S-15 duplicates S-16*
4. **Latency: direction of the trade-off and the numbers problem** (H2) — F-05, F-06 · *limitation: no shared-workload benchmark*
5. **Cost: upfront versus ongoing** (H2) — F-07, F-08 · *limitation: no complete TCO model*
   - 5.1 Published figures and what they actually cover (H3) — F-08 · *limitation: self-reported, non-comparable*
6. **Security and data governance** (H2) — F-09, F-10, F-11
   - 6.1 Where the sources disagree on data control (H3) — F-09, F-10 · *limitation: unreconciled*
   - 6.2 RAG-specific attack surface (H3) — F-11 · *limitation: RAG-skewed, thin sourcing*
7. **Where fine-tuning is the tool of choice** (H2) — F-14 · *limitation: benefit unmeasured*
8. **Hybrid approaches: what the corpus actually recommends** (H2) — F-12, F-13 · *limitation: 70/20/10 is one anecdote*
9. **A decision path for an enterprise assistant** (H2) — F-01, F-02, F-09, F-12, F-14
10. **Evidence gaps, assumptions, and what to verify before committing** (H2) — F-15, F-16 · *limitation: grounded mainly in gaps*

## Diagrams

- **decision-flow** (flowchart) in section `decision-path` — findings F-01, F-02, F-09, F-12, F-14.
  Caption: Decision path for choosing RAG, fine-tuning, or a hybrid. If the feature depends on current, changing, or citable knowledge, retrieval is indicated; if it needs consistent style, a strict output format, or steady behaviour on a narrow repeated task, fine-tuning is indicated; when both are needed, the corpus recommends combining them, starting with prompting plus RAG and adding fine-tuning for the behaviour gaps that remain ([S-05], [S-09], [S-06], [S-25]). Because the corpus offers no universal ranking and no shared-workload measurements, this diagram is a routing aid for scoping, not a claim about which approach is better.

## Gaps

- No controlled, head-to-head, end-to-end comparison of RAG vs a fine-tuned model on the same enterprise assistant workload.
- No shared-workload latency benchmark; only directional statements and one vendor's token-generation times (S-24).
- No complete enterprise TCO model; cost evidence is vendor estimates with differing scopes and units.
- Fine-tuning-specific security risks (e.g. data extraction from weights) are not covered; security evidence is RAG-skewed.
- The one academic study (S-15/S-16) is abstract-only, so per-technique results cannot be cited.
- No evidence on multi-tenant scale behaviour or fine-tuned behaviour drift after base-model weight updates (beyond a passing mention in S-05).
- No survey or independent data on how often teams choose each option; the only ratio (S-05) is a single-vendor anecdote.
- No worked example comparing the approaches against explicit enterprise success metrics.

## Limitations

- Corpus is dominated by vendor blogs, whitepapers, and product/marketing pages that sell RAG and/or fine-tuning services.
- Quantitative claims are self-reported, use different scopes/units, and are not independently verified.
- S-15 and S-16 are the same paper (arXiv abstract + ACL Anthology landing page for 2024.inlg-main.15) — one evidence thread, not two.
- Latency, cost, and security evidence is largely qualitative or directional; no numeric rankings are supported.
- Publication dates span 2024-04 to 2026-06; some claims are forward-dated or tied to unverifiable model versions.
- Only one peer-reviewed source, available only at abstract length.
- No source reports measurements from a real enterprise assistant deployment.

## Closing rationale

An axis-by-axis decision brief fits this topic and goal because the corpus addresses each axis the team asked about and does so in comparable form: freshness ([S-09], [S-06], [S-01]), evaluation ([S-05], [S-25], [S-27], [S-28], [S-15]/[S-16]), latency ([S-01], [S-06], [S-10], [S-24]), cost ([S-05], [S-06], [S-09], [S-03], [S-24]), and security ([S-28], [S-25], [S-09]) appear as recurring, structured comparisons, several already in table form ([S-06], [S-09], [S-13]). The corpus also explicitly argues against the framing the goal warns about: [S-09] states the pair is "two tools for two jobs, not a contest with a single winner", and [S-15]/[S-16] report there is "no universal best-technique". A decision brief can honor that by routing rather than ranking. The evidence base is thin and commercially skewed — most sources are vendor blogs or sales pages ([S-05], [S-06], [S-09], [S-10], [S-27]), the only peer-reviewed study is available solely as an abstract ([S-15], [S-16], which are the same paper), and the single concrete latency figure is one vendor's own model timings ([S-24]) — so the outline deliberately foregrounds evaluation practice, the governance disagreement between [S-09]/[S-10] and [S-01], and an explicit gaps section instead of manufacturing criteria, benchmarks, or a winner. The single flowchart in `decision-path` turns the supported conditions into a scoping aid while its caption states the limits. Formats that fit less well are a research paper (too few, too shallow sources), a build tutorial (no generalizable procedure), and a ranked scorecard (the corpus supplies no comparable measurements and rejects rankings).
