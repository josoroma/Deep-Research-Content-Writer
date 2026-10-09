# Synthesis summary — RAG vs fine-tuning

- **Run ID:** rag-vs-fine-tuning-20261009T204551Z
- **Topic:** RAG vs fine-tuning
- **Input fingerprint:** `369db3966788b9fa78b752a94b3863062e149d39894dc10cbb6ce6fcb533ae41`
- **Contract version:** 2
- **Objective origin:** explicit
- **Sources considered:** 17 (S-01, S-03, S-05, S-06, S-09, S-10, S-13, S-15, S-16, S-17, S-18, S-19, S-20, S-23, S-24, S-26, S-27)
- **Findings:** 19 · **Outline sections:** 21 · **Diagrams:** 2

## Reader objective

Help an engineering team decide, feature by feature, whether to use RAG, fine-tuning, or a hybrid for an enterprise AI assistant, by comparing the five dimensions the goal names and stating the conditions and evidence limits behind each claim.

## Format decision

- **Label:** decision-oriented comparison with explicit conditional guidance
- **Confidence:** moderate
- **Why:** The goal is a choice among three options across five named dimensions, and the corpus supports conditional trade-offs far better than a verdict. A dimension-by-dimension comparison lets each dimension carry its own conditional guidance and evidence weight, and lets contradictory cost and threshold claims sit side by side instead of being averaged into a ranking. Several sources already present comparison tables, but their thresholds conflict (F-05), so the format treats those tables as inputs to be qualified rather than settled criteria.
- **Alternatives considered:** literature review of RAG systems research; step-by-step hybrid build tutorial; narrative explainer of what RAG and fine-tuning are; ranked recommendation brief.

## Evidence types

- vendor engineering blog (large platform vendor)
- vendor and consultancy comparison blog
- vendor whitepaper / marketing page
- peer-reviewed venue paper, accepted to IEEE CAI 2026 (S-23)
- arXiv preprint reporting original systems characterization experiments (S-18)
- arXiv preprint reporting original applied security-incident experiments (S-26)
- data-labeling vendor article on RAG evaluation
- paid course / product landing page

## Findings

| ID | Statement (abridged) | Evidence |
| --- | --- | --- |
| F-01 | RAG and fine-tuning are complementary, not mutually exclusive: RAG supplies knowledge at query time, fine-tuning changes behaviour. | S-15, S-09 |
| F-02 | For changing knowledge, RAG updates answers by re-indexing; a fine-tuned model stays frozen at its training snapshot. | S-15, S-19, S-09, S-05 |
| F-03 | Documented failure mode: fine-tuning for facts yields confident staleness once knowledge changes. | S-09, S-15, S-24 |
| F-04 | Cost structures differ in shape: RAG pays recurring per-query context/infra; fine-tuning concentrates cost at training and can lower per-query tokens. | S-15, S-16, S-20, S-13 (qualifies), S-19 (contradicts) |
| F-05 | Published break-even points differ by one to three orders of magnitude; any single threshold is an assumption. | S-05, S-20 (qualifies), S-16 (contradicts) |
| F-06 | Retrieval adds pipeline stages before the first token, so RAG tends to show higher TTFT than a direct fine-tuned call. | S-18, S-15, S-20, S-06 |
| F-07 | Retrieval integration dominates latency: stride and index choices can move end-to-end latency by nearly two orders of magnitude. | S-18, S-16 (qualifies) |
| F-08 | The retrieval step itself need not be the bottleneck: sub-30 ms P95 retrieval latency reported in a peer-reviewed study. | S-23 |
| F-09 | For access control and deletion, RAG is the easier governance story; weights make per-user restriction require separate models. | S-20, S-15, S-19, S-09 (qualifies) |
| F-10 | Locally deployed models retained near-cloud accuracy in a security-incident study, at a speed cost. | S-26 |
| F-11 | Within a RAG deployment, model/provider selection can dominate cost at equal measured accuracy. | S-26 |
| F-12 | RAG and fine-tuning need different evaluation metrics (retrieval/faithfulness vs task metrics). | S-17, S-19 |
| F-13 | Treat cost and latency as first-class evaluation dimensions; freeze golden sets to keep comparisons valid. | S-17, S-05, S-15 |
| F-14 | Inside RAG, chunking/embedding/metadata choices change outcomes as much as the architecture choice; no single configuration wins on every metric. | S-23, S-05 |
| F-15 | The recurring production pattern is hybrid — fine-tune for behaviour, retrieve for knowledge — sequenced RAG-first. | S-15, S-09, S-24 |
| F-16 | Combining is not automatically better: naive layering can fail and hybrid inherits both systems' complexity. | S-16, S-19 (qualifies) |
| F-17 | PEFT methods (LoRA/QLoRA) lower fine-tuning upfront cost, though headline savings figures are vendor claims. | S-15, S-05, S-19 (qualifies) |
| F-18 | Self-reported adoption leans RAG-first, but the supporting statistics are secondhand and dated. | S-16, S-15 |
| F-19 | Several sources sell the architecture they recommend, so their comparisons are not independent assessments. | S-24, S-10, S-27 |

## Outline

1. **One decision, three options, five dimensions** (H2, `sec_frame`) — F-01, F-19
2. **Data freshness: what changes, and how fast** (H2, `sec_freshness`) — F-02, F-03
3. **Cost: two different shapes, and why the break-even numbers disagree** (H2, `sec_cost`) — F-04, F-05, F-17
   - Where RAG's recurring bill comes from (H3, `sec_cost_recurring`) — F-04, F-11
   - Where fine-tuning's cost concentrates, and the PEFT discount (H3, `sec_cost_training`) — F-17, F-04
4. **Latency: two questions, not one slogan** (H2, `sec_latency`) — F-06, F-07, F-08
   - Where the time goes in a RAG request (H3, `sec_latency_stages`) — F-06, F-07 *(limitation: figures from one configuration in S-18 and one modelled breakdown in S-20)*
   - Retrieval is not automatically the bottleneck (H3, `sec_latency_retrieval`) — F-08
5. **Security, privacy and governance** (H2, `sec_security`) — F-09, F-10
   - Per-user access and the deletion problem (H3, `sec_security_access`) — F-09 *(limitation: architectural argument and vendor assertion only; no audit/incident evidence)*
   - Local deployment as a privacy option, and its price (H3, `sec_security_local`) — F-10
6. **Evaluation: two metric sets and one discipline** (H2, `sec_evaluation`) — F-12, F-13, F-14
   - Two metric sets, not one (H3, `sec_eval_metrics`) — F-12
   - Frozen sets, cost and latency in the loop (H3, `sec_eval_discipline`) — F-13 *(limitation: cadences are single-source practitioner advice)*
   - A caution: retrieval quality moves outcomes on its own (H3, `sec_eval_retrieval_quality`) — F-14
7. **When to combine: the hybrid pattern and its sequence** (H2, `sec_hybrid`) — F-15, F-16
   - Fine-tune for behaviour, retrieve for knowledge (H3, `sec_hybrid_pattern`) — F-15
   - Sequence: RAG first, then fine-tune the failure modes (H3, `sec_hybrid_sequence`) — F-15, F-18
   - What hybrid costs you (H3, `sec_hybrid_cost`) — F-16
8. **Conditional guidance by scenario** (H2, `sec_guidance`) — F-02, F-04, F-06, F-09, F-12, F-15
9. **Evidence limits: what this corpus cannot settle** (H2, `sec_limits`) — F-05, F-19, F-11 *(limitation: vendor-dominated evidence; no head-to-head measurement; thresholds disagree by orders of magnitude)*

## Diagrams

- `d1_decision_flow` (flowchart, in `sec_guidance`) — per-feature decision conditions with "both" as a common outcome. Findings: F-01, F-02, F-09, F-15.
- `d2_rag_request_path` (sequenceDiagram, in `sec_latency_stages`) — RAG request stages vs a direct fine-tuned call; no invented timings. Findings: F-06, F-07, F-08.

## Limitations

- Most sources are vendor, consultancy, data-labeling or course-marketing pages; only S-18, S-23 and S-26 report original experiments, and S-15 is a large vendor engineering blog rather than a study.
- Only S-23 is described as accepted to a peer-reviewed venue; S-18 and S-26 are preprints. All three test narrow questions, not the full RAG-vs-fine-tuning-vs-hybrid decision.
- Quantitative cost and latency comparisons are modelled from stated assumptions and differ across sources; they are not measurements of a comparable deployment.
- Several numeric claims are secondhand citations whose primary sources are not in this corpus (Snorkel AI in S-10/S-19, Menlo Ventures in S-16, RAFT in S-16).
- Some sources have a direct commercial interest in the recommendation they make, so repeated claims are not independent corroboration.
- Publication dates span 2024-08 to 2026-08 and cite different price lists, model versions and adoption surveys; no source reconciles those assumptions.
- Source IDs identify files that were read, not that they semantically support a claim.

## Gaps

- No head-to-head, measured comparison of RAG, fine-tuning and hybrid on the same enterprise assistant workload.
- No cost, latency or accuracy figure is reproducible from the corpus.
- Hybrid systems are described conceptually; no hybrid-specific evaluation design or measured hybrid result.
- Security/privacy conclusions rest on architecture and vendor assertion; no audit, incident or penetration-test evidence.
- The corpus cannot support a universal ranking or settle the conflicting break-even thresholds (F-05).
- Coverage is skewed by retrieval: ten numbered URLs (files 002, 004, 007, 008, 011, 012, 014, 021, 022, 025) are failed or thin fetches; no sources were invented for them.
- Timeframe drift is unresolved across 2024-08 to 2026-08 sources.

## Closing rationale

The corpus answers the team's five dimensions unevenly, and a comparison-with-conditions format follows that shape instead of forcing a winner. Freshness, access control and metric selection are described consistently across sources, so those sections can give relatively firm conditional guidance. Cost and latency are where the corpus fragments: the structural split is agreed, but break-even thresholds differ by one to three orders of magnitude and a flat "RAG is cheaper" claim sits against volume-dependent framing elsewhere, while latency is an orders-of-magnitude design variable in one systems study and a sub-30 ms retrieval step in another. A ranked brief would have to suppress those conflicts, which contradicts the goal's instruction to preserve evidence limits. The outline therefore gives freshness, cost, latency, security and evaluation separate sections with conditional statements, adds a hybrid section because hybrid is the only option every comparative source endorses in some form, and closes with the limits. Confidence is moderate rather than strong because the decision-relevant comparisons are argued or modelled, not measured.
