# Research synthesis: RAG vs fine-tuning

Give an engineering team a dimension-by-dimension comparison of RAG, fine-tuning, and hybrid architectures for enterprise AI assistants — covering data freshness, evaluation, latency, cost, and security — with the strength and disagreements of the underlying evidence made explicit so the team can run its own decision rather than adopt a vendor's ranking.

Format: evidence-graded decision brief with a dimension-by-dimension trade-off comparison. The reader's task is a choice among three architectures judged against five named dimensions, so the document should be organized by those dimensions (freshness, evaluation, latency, cost, security) rather than as a narrative or a procedure. The corpus supplies comparative guidance, quantitative estimates, and one independent systems study — enough to compare dimensions and show where sources agree or conflict, but not enough for a ranked recommendation, a reproducible how-to, or a research paper with original results. An explicit evidence-strength section and per-dimension 'what this does not settle' notes let the brief respect the goal's instruction to preserve evidence limits and avoid unsupported rankings.

## Reading this comparison: what the evidence can and cannot settle

Set expectations before any recommendation: state that most sources are vendor guidance, that one independent study exists and is RAG-only, that adoption numbers are survey-based, and that the cost crossover is contested — so the reader knows no ranking follows.

The corpus contains no controlled head-to-head comparison of RAG and fine-tuning on the same enterprise task; comparative conclusions rest on vendor guidance, second-hand benchmark citations, and one independent RAG-only systems study, and sources explicitly caution against extrapolating benchmark results. [S-18] [S-24] [S-24] [S-15] [S-19]

- qualifies: RAG is generally better for most enterprise use cases because it is more secure, scalable, and cost-efficient. [S-19]

Sources report that RAG dominates enterprise production adoption relative to fine-tuning, but the supporting numbers are survey-based or openly estimated rather than measured across a defined population. [S-16] [S-23] [S-03]

- Qualification: S-23's statistics are attributed to bracketed secondary citations without accessible methodology in the corpus.

- Qualification: Adoption share is not evidence of superiority; S-16 itself notes hybrid outperforms but adoption favors RAG because few teams have both skill sets.

- qualifies: Currently, RAG is one of the most used methods in the domain of large language models; one can even assume that 90% of LLM-powered applications make use of RAG in one way or another. [S-03]

Sources disagree about where fine-tuning becomes cheaper than RAG: published crossover thresholds span roughly 100k queries per month to more than 100M, and one source asserts RAG is generally more cost-efficient, so no single crossover should be treated as settled. [S-05] [S-16] [S-19] [S-16]

- Qualification: Each threshold is tied to a specific provider price list and assumed prompt length, so the disagreement may reflect assumptions as much as genuine disagreement.

- Qualification: S-05's figure is an operational rule of thumb; S-16's is a modeled break-even; S-19's is an unqualified preference.

- contradicts: RAG is generally more cost-efficient than fine-tuning because it limits resource costs by leveraging existing data and eliminating the need for extensive training stages. [S-19]

## The core distinction: changing knowledge vs. changing behavior

Give the reader the one framing that most sources share, so the five dimensions that follow have a consistent vocabulary; also note prompt engineering as the cheaper baseline that keeps the choice from looking falsely binary.

Sources broadly converge that fine-tuning is the tool for changing model behavior — tone, style, and output format — while RAG is the tool for supplying changing knowledge. [S-15] [S-05] [S-09] [S-12]

Prompt engineering, supervised fine-tuning, RLHF, and distillation sit alongside RAG as ways to bring data to a model, and prompt engineering is the cheapest baseline for simple or small-data cases. [S-12] [S-15] [S-12]

- Qualification: The goal scopes the decision to RAG, fine-tuning, and hybrid; prompt engineering is included only to prevent a false three-way binary.

## Data freshness and knowledge updates

Answer the first comparison dimension: where knowledge lives and how quickly it can change.

RAG can refresh what a model knows at query time without retraining, whereas a fine-tuned model's knowledge is fixed to the data snapshot used in training and changing it requires another training cycle. [S-15] [S-15] [S-19] [S-10]

- Qualification: The freshness advantage is about where knowledge lives, not about answer quality; several sources note RAG answers are only as current and correct as the indexed corpus.

- qualifies: All successful models require continuous fine-tuning to introduce new information and stay relevant. It’s a repeated process, not just a one-and-done. [S-10]

Long context is presented as a complement to retrieval — used to reason over an already-narrowed, authorized evidence set — not as a replacement for retrieval over a changing corpus. [S-24] [S-24] [S-12]

- Qualification: The long-context option is argued mostly by a single vendor source (S-24), which simultaneously states that its own model's specifications do not prove retrieval recall or production readiness.

### RAG: freshness at query time

Explain that retrieval decouples knowledge from weights, and note what that implies for update effort and citations.

RAG can refresh what a model knows at query time without retraining, whereas a fine-tuned model's knowledge is fixed to the data snapshot used in training and changing it requires another training cycle. [S-15] [S-15] [S-19] [S-10]

- Qualification: The freshness advantage is about where knowledge lives, not about answer quality; several sources note RAG answers are only as current and correct as the indexed corpus.

- qualifies: All successful models require continuous fine-tuning to introduce new information and stay relevant. It’s a repeated process, not just a one-and-done. [S-10]

Because RAG keeps sensitive content in an external store, sources say it supports retrieval-time access control, easier deletion, and source attribution, while fine-tuning embeds data in weights where granular access control and removal are difficult. [S-20] [S-19] [S-15] [S-15] [S-12]

- Qualification: The governance advantage assumes the retrieval layer itself is correctly access-controlled; S-24 and S-27 show that misconfigured retrieval is a primary failure mode.

### Fine-tuning: a knowledge snapshot baked into weights

Explain the training-snapshot limitation and the retraining cycle it implies, without implying fine-tuning is unusable for stable domains.

RAG can refresh what a model knows at query time without retraining, whereas a fine-tuned model's knowledge is fixed to the data snapshot used in training and changing it requires another training cycle. [S-15] [S-15] [S-19] [S-10]

- Qualification: The freshness advantage is about where knowledge lives, not about answer quality; several sources note RAG answers are only as current and correct as the indexed corpus.

- qualifies: All successful models require continuous fine-tuning to introduce new information and stay relevant. It’s a repeated process, not just a one-and-done. [S-10]

Sources broadly converge that fine-tuning is the tool for changing model behavior — tone, style, and output format — while RAG is the tool for supplying changing knowledge. [S-15] [S-05] [S-09] [S-12]

### Long context is not a substitute for a changing corpus

Close off a common false third option: large context windows help reason over an already-narrowed evidence set but do not solve currency or permission scoping.

Long context is presented as a complement to retrieval — used to reason over an already-narrowed, authorized evidence set — not as a replacement for retrieval over a changing corpus. [S-24] [S-24] [S-12]

- Qualification: The long-context option is argued mostly by a single vendor source (S-24), which simultaneously states that its own model's specifications do not prove retrieval recall or production readiness.

## Latency and serving characteristics

Present the retrieval-hop overhead with measured figures where they exist, and immediately flag that fine-tuned models are not guaranteed to be faster.

RAG adds retrieval stages that increase time-to-first-token, tail latency, and end-to-end latency, while a fine-tuned model can answer without a retrieval hop — but the corpus cautions that the fine-tuning latency advantage is not guaranteed. [S-18] [S-18] [S-20] [S-15] [S-07]

- Qualification: S-18 measures RAG pipelines against a baseline LLM, not against a fine-tuned model on the same task and hardware.

- Qualification: Latency depends on retrieval index choice, batching, reranking, and context length, so published millisecond figures are configuration-specific.

- qualifies: A fine-tuned model may be larger or more complex than a retrieval-based alternative, which can impact**inference speed** , especially in production environments with latency constraints. [S-07]

## Cost structure and the scale crossover

Separate the two cost shapes (upfront training vs recurring retrieval) before addressing the disputed crossover point.

Fine-tuning concentrates cost at the start — data preparation, training compute, and experimentation — and can lower per-query input-token cost, which sources say pays off at high, stable volume. [S-16] [S-15] [S-20] [S-16]

- Qualification: Upfront figures range from under $20 of GPU time for one QLoRA run (S-20) to $1,000-$20,000 for a LoRA program (S-05), reflecting different model sizes and data-prep scope.

- Qualification: Costs assume the domain is stable enough that the training investment is amortized over many queries.

RAG has low setup cost but incurs recurring per-query retrieval and context-token costs that scale linearly with traffic. [S-16] [S-05] [S-16] [S-20]

- Qualification: Recurring cost depends on retrieved token volume, reranking, caching, and vector-database pricing, all of which vary by design.

Sources disagree about where fine-tuning becomes cheaper than RAG: published crossover thresholds span roughly 100k queries per month to more than 100M, and one source asserts RAG is generally more cost-efficient, so no single crossover should be treated as settled. [S-05] [S-16] [S-19] [S-16]

- Qualification: Each threshold is tied to a specific provider price list and assumed prompt length, so the disagreement may reflect assumptions as much as genuine disagreement.

- Qualification: S-05's figure is an operational rule of thumb; S-16's is a modeled break-even; S-19's is an unqualified preference.

- contradicts: RAG is generally more cost-efficient than fine-tuning because it limits resource costs by leveraging existing data and eliminating the need for extensive training stages. [S-19]

### RAG: low setup, recurring retrieval and context cost

Show how retrieval cost grows linearly with traffic and which design choices change it.

RAG has low setup cost but incurs recurring per-query retrieval and context-token costs that scale linearly with traffic. [S-16] [S-05] [S-16] [S-20]

- Qualification: Recurring cost depends on retrieved token volume, reranking, caching, and vector-database pricing, all of which vary by design.

### Fine-tuning: upfront training, cheaper inference

Show where fine-tuning spend concentrates and why data preparation dominates it.

Fine-tuning concentrates cost at the start — data preparation, training compute, and experimentation — and can lower per-query input-token cost, which sources say pays off at high, stable volume. [S-16] [S-15] [S-20] [S-16]

- Qualification: Upfront figures range from under $20 of GPU time for one QLoRA run (S-20) to $1,000-$20,000 for a LoRA program (S-05), reflecting different model sizes and data-prep scope.

- Qualification: Costs assume the domain is stable enough that the training investment is amortized over many queries.

### Where the crossover is — and why the sources disagree

Present the conflicting thresholds side by side and explain that the right comparison is the reader's own token volume and knowledge volatility, not a published number.

Sources disagree about where fine-tuning becomes cheaper than RAG: published crossover thresholds span roughly 100k queries per month to more than 100M, and one source asserts RAG is generally more cost-efficient, so no single crossover should be treated as settled. [S-05] [S-16] [S-19] [S-16]

- Qualification: Each threshold is tied to a specific provider price list and assumed prompt length, so the disagreement may reflect assumptions as much as genuine disagreement.

- Qualification: S-05's figure is an operational rule of thumb; S-16's is a modeled break-even; S-19's is an unqualified preference.

- contradicts: RAG is generally more cost-efficient than fine-tuning because it limits resource costs by leveraging existing data and eliminating the need for extensive training stages. [S-19]

Sources converge on a small set of decision variables — how often knowledge changes, query volume, need for citations, output-format strictness, access-control needs, and team capability — even though the thresholds and weights attached to them differ. [S-16] [S-05] [S-15] [S-14]

- Qualification: The variables agree; the numeric triggers do not (see F-06), so the brief should present the variables as questions rather than as a scoring rubric.

## Evaluation

Give the team an evaluation plan per layer and be explicit that the corpus's fine-tuning evaluation material is thin.

Evaluation is layered: retrieval metrics (precision@k, recall@k, MRR, nDCG), generation metrics (faithfulness, answer relevance, citation coverage, hallucination rate), and end-to-end checks for correctness, latency, cost, and safety. [S-17] [S-17] [S-17] [S-20]

- Qualification: Metric definitions are consistent across sources, but no source supplies enterprise-specific acceptance thresholds for an assistant, only examples such as a faithfulness floor above 0.85 (S-26).

Evaluation guidance in the corpus is RAG-centric; fine-tuning evaluation appears only as general guidance about task-specific metrics on held-out data, with no comparable benchmark set or acceptance thresholds for fine-tuned assistants. [S-19] [S-17] [S-15]

- Qualification: This is a corpus gap rather than a claim that fine-tuning evaluation methods do not exist elsewhere.

### Measure retrieval, generation, and end-to-end separately

List the concrete metric families and named tooling so the team can stand up a harness before choosing architecture.

Evaluation is layered: retrieval metrics (precision@k, recall@k, MRR, nDCG), generation metrics (faithfulness, answer relevance, citation coverage, hallucination rate), and end-to-end checks for correctness, latency, cost, and safety. [S-17] [S-17] [S-17] [S-20]

- Qualification: Metric definitions are consistent across sources, but no source supplies enterprise-specific acceptance thresholds for an assistant, only examples such as a faithfulness floor above 0.85 (S-26).

Both approaches depend on data quality and continuous monitoring: irrelevant or stale documents degrade RAG, while mislabeled or biased training data degrade fine-tuned models, and both need drift detection. [S-19] [S-15] [S-17] [S-27]

### What is missing for fine-tuned assistants

State plainly that fine-tuning evaluation guidance in the corpus is generic, so teams must define their own task metrics and acceptance thresholds.

Evaluation guidance in the corpus is RAG-centric; fine-tuning evaluation appears only as general guidance about task-specific metrics on held-out data, with no comparable benchmark set or acceptance thresholds for fine-tuned assistants. [S-19] [S-17] [S-15]

- Qualification: This is a corpus gap rather than a claim that fine-tuning evaluation methods do not exist elsewhere.

Limitation: The corpus provides no benchmark set, metric definitions, or acceptance thresholds for evaluating a fine-tuned assistant comparable to the RAG metric stack; this section must present the absence rather than invent a protocol.

## Security, access control, and governance

Frame security as a two-sided trade-off: retrieval keeps data external and governable but adds attack surface, while fine-tuning hides data in weights but makes control and deletion hard.

Because RAG keeps sensitive content in an external store, sources say it supports retrieval-time access control, easier deletion, and source attribution, while fine-tuning embeds data in weights where granular access control and removal are difficult. [S-20] [S-19] [S-15] [S-15] [S-12]

- Qualification: The governance advantage assumes the retrieval layer itself is correctly access-controlled; S-24 and S-27 show that misconfigured retrieval is a primary failure mode.

RAG is not automatically more secure: it introduces indirect prompt injection, knowledge-base poisoning, and vector or embedding exposure, and the corpus documents reported incidents of each. [S-27] [S-27] [S-24] [S-07]

- Qualification: S-27 reports incidents with links to external sources that cannot be verified inside this corpus.

- Qualification: No source in the corpus offers a matching threat analysis for fine-tuned deployments, so the two sides are not symmetrically evidenced.

Access control must be enforced before retrieval: post-filtering a global top-k is unsafe and can leak through titles, snippets, counts, or timing, and the same rules must cover caches, summaries, logs, and citations. [S-24] [S-24] [S-27] [S-24]

- Qualification: S-24 is vendor material, but it explicitly separates its own model claims from proven capability and cites NIST ABAC and OWASP rather than its own benchmarks.

### Retrieval-time authorization and deletion

Explain the mechanics of permission-aware retrieval and deletion across derived artifacts, including the failure mode of post-filtering a global top-k.

Access control must be enforced before retrieval: post-filtering a global top-k is unsafe and can leak through titles, snippets, counts, or timing, and the same rules must cover caches, summaries, logs, and citations. [S-24] [S-24] [S-27] [S-24]

- Qualification: S-24 is vendor material, but it explicitly separates its own model claims from proven capability and cites NIST ABAC and OWASP rather than its own benchmarks.

Because RAG keeps sensitive content in an external store, sources say it supports retrieval-time access control, easier deletion, and source attribution, while fine-tuning embeds data in weights where granular access control and removal are difficult. [S-20] [S-19] [S-15] [S-15] [S-12]

- Qualification: The governance advantage assumes the retrieval layer itself is correctly access-controlled; S-24 and S-27 show that misconfigured retrieval is a primary failure mode.

### RAG's own attack surface

Counter the intuition that external storage is simply safer by describing indirect prompt injection, knowledge-base poisoning, and embedding exposure, with the incident evidence available.

RAG is not automatically more secure: it introduces indirect prompt injection, knowledge-base poisoning, and vector or embedding exposure, and the corpus documents reported incidents of each. [S-27] [S-27] [S-24] [S-07]

- Qualification: S-27 reports incidents with links to external sources that cannot be verified inside this corpus.

- Qualification: No source in the corpus offers a matching threat analysis for fine-tuned deployments, so the two sides are not symmetrically evidenced.

## Hybrid approaches: what the evidence supports

Explain the recommended hybrid pattern, what it requires to work (training the model to reason over retrieved context), and its honest cost and skill penalties.

Hybrid architectures — fine-tune for behavior and format, retrieve for current facts — are widely recommended, but they inherit the complexity, cost, and skill requirements of both systems. [S-15] [S-16] [S-12] [S-19] [S-16]

- qualifies: Using both approaches means inheriting the complexity of both systems. [S-19]

- qualifies: Hybrid requires both ML and data engineering capabilities simultaneously, a combination few organizations have. [S-16]

Sources citing retrieval-aware fine-tuning research (RAFT) claim that hybrids trained to reason over retrieved context outperform either approach alone, and warn that simply layering RAG on a fine-tuned model often fails. [S-16] [S-16] [S-16] [S-01]

- Qualification: The outperform claim is attributed to external benchmark papers; the corpus does not reproduce the experiments or the benchmark conditions.

Sources report that RAG dominates enterprise production adoption relative to fine-tuning, but the supporting numbers are survey-based or openly estimated rather than measured across a defined population. [S-16] [S-23] [S-03]

- Qualification: S-23's statistics are attributed to bracketed secondary citations without accessible methodology in the corpus.

- Qualification: Adoption share is not evidence of superiority; S-16 itself notes hybrid outperforms but adoption favors RAG because few teams have both skill sets.

- qualifies: Currently, RAG is one of the most used methods in the domain of large language models; one can even assume that 90% of LLM-powered applications make use of RAG in one way or another. [S-03]

## Keeping either approach healthy: data quality and monitoring

Show that the choice does not remove the operational burden; both paths fail on data quality and need drift detection.

Both approaches depend on data quality and continuous monitoring: irrelevant or stale documents degrade RAG, while mislabeled or biased training data degrade fine-tuned models, and both need drift detection. [S-19] [S-15] [S-17] [S-27]

## Deciding for your team

Convert the comparison into a set of questions the team can answer with its own numbers — volatility, volume, citation needs, format strictness, access-control scope, and available skills — without issuing a ranking.

Sources converge on a small set of decision variables — how often knowledge changes, query volume, need for citations, output-format strictness, access-control needs, and team capability — even though the thresholds and weights attached to them differ. [S-16] [S-05] [S-15] [S-14]

- Qualification: The variables agree; the numeric triggers do not (see F-06), so the brief should present the variables as questions rather than as a scoring rubric.

Sources disagree about where fine-tuning becomes cheaper than RAG: published crossover thresholds span roughly 100k queries per month to more than 100M, and one source asserts RAG is generally more cost-efficient, so no single crossover should be treated as settled. [S-05] [S-16] [S-19] [S-16]

- Qualification: Each threshold is tied to a specific provider price list and assumed prompt length, so the disagreement may reflect assumptions as much as genuine disagreement.

- Qualification: S-05's figure is an operational rule of thumb; S-16's is a modeled break-even; S-19's is an unqualified preference.

- contradicts: RAG is generally more cost-efficient than fine-tuning because it limits resource costs by leveraging existing data and eliminating the need for extensive training stages. [S-19]

Sources broadly converge that fine-tuning is the tool for changing model behavior — tone, style, and output format — while RAG is the tool for supplying changing knowledge. [S-15] [S-05] [S-09] [S-12]

Because RAG keeps sensitive content in an external store, sources say it supports retrieval-time access control, easier deletion, and source attribution, while fine-tuning embeds data in weights where granular access control and removal are difficult. [S-20] [S-19] [S-15] [S-15] [S-12]

- Qualification: The governance advantage assumes the retrieval layer itself is correctly access-controlled; S-24 and S-27 show that misconfigured retrieval is a primary failure mode.

## Open questions and evidence gaps

List what the team would need to measure for itself, and name the corpus limits that prevent a stronger conclusion.

The corpus contains no controlled head-to-head comparison of RAG and fine-tuning on the same enterprise task; comparative conclusions rest on vendor guidance, second-hand benchmark citations, and one independent RAG-only systems study, and sources explicitly caution against extrapolating benchmark results. [S-18] [S-24] [S-24] [S-15] [S-19]

- qualifies: RAG is generally better for most enterprise use cases because it is more secure, scalable, and cost-efficient. [S-19]

Evaluation guidance in the corpus is RAG-centric; fine-tuning evaluation appears only as general guidance about task-specific metrics on held-out data, with no comparable benchmark set or acceptance thresholds for fine-tuned assistants. [S-19] [S-17] [S-15]

- Qualification: This is a corpus gap rather than a claim that fine-tuning evaluation methods do not exist elsewhere.

Limitation: No source provides a controlled head-to-head RAG-vs-fine-tuning comparison on a shared enterprise workload, so this section cannot cite a definitive study; it should state the gap and suggest the team's own benchmark instead.

Gap: No measured comparison of answer quality, hallucination rate, or task accuracy between RAG, fine-tuning, and hybrid on an identical enterprise assistant workload.

Gap: No published, reproducible evaluation protocol for fine-tuned assistants comparable to the RAG metric stack (precision@k, recall@k, MRR, nDCG, faithfulness, citation coverage).

Gap: No agreed cost crossover point: thresholds in the corpus range from roughly 100k queries/month to more than 100M queries/month, with different underlying assumptions.

Gap: Little evidence on hybrid operational cost in practice, and none on the failure modes of hybrid orchestration beyond qualitative warnings about synchronization and routing complexity.

Gap: No corpus evidence on latency of a fine-tuned model versus RAG measured under the same traffic and hardware, so the latency comparison rests on architecture reasoning plus one RAG-only measurement study.

Gap: No treatment of fine-tuning-specific security threats (training-data extraction, memorization of PII) beyond brief mentions of leak risk and deletion difficulty.

Gap: No human-factors or team-skills data beyond assertions that hybrid requires both ML and data-engineering capabilities.

Corpus limitation: Almost all sources are vendor or product content (superannotate, vectorize, codelamda, v2solutions, orq.ai, upstash, coreweave, Google Cloud, agicent, Databricks, actian, labelyourdata, montecarlo, nextgencoding, ai-de.net, Tencent, c3.unu.edu) with commercial incentives and self-referential 'best practice' framing.

Corpus limitation: Only one source is independent research (S-18, arXiv), and it characterizes RAG inference systems in isolation rather than comparing RAG against a fine-tuned baseline on a shared task; it also states its study 'is not exhaustive'.

Corpus limitation: No source reports a controlled head-to-head RAG-vs-fine-tuning experiment on the same enterprise workload; benchmark numbers cited (SWE-bench, BIRD-SQL, an agriculture benchmark, RAFT) come second-hand through vendor posts.

Corpus limitation: Cost and latency figures depend on specific model pricing and hardware rates (GPT-5.2, Claude 3.5 Sonnet, GPT-4.1, Pinecone, A10G/H100 rates) and on assumed token volumes, so they date quickly and are not directly comparable across sources.

Corpus limitation: Publication dates span 2024-04 to 2026-10; the older pieces (S-01, S-03, S-09, S-12) predate several referenced pricing and model changes, and S-23 is a forward-looking 2026-2030 projection with claims attributed to secondary citations rather than primary data.

Corpus limitation: Several sources assert a general winner (for example S-19's FAQ preference for RAG, S-06's preference for fine-tuning on coherence and latency), which conflicts with the goal's instruction to avoid unsupported rankings; these are recorded as source claims, not adopted.

Corpus limitation: Security evidence is split between RAG-side threat reporting (S-27) and access-control architecture (S-24); there is no comparable security analysis of fine-tuned model deployment beyond ACL and deletion limitations.

Corpus limitation: Evaluation evidence is heavily RAG-centric; fine-tuning evaluation appears only as short general guidance.

Corpus limitation: Some sources (S-26, S-23) are promotional or AI-generated-looking syntheses with dense unattributed statistics ('15-40% gains', '86% of organizations') that cannot be verified within the corpus.

A dimension-by-dimension decision brief fits because the corpus is comparative guidance rather than procedure or experiment: nineteen of the twenty sources are vendor or trade publications, and the single independent study characterizes RAG inference in isolation and states that its work 'is not exhaustive' [S-18]. Organizing by the goal's own axes lets each dimension be argued from the sources that actually address it — freshness from the Databricks, Monte Carlo, and IBM guides [S-15][S-19][S-08]; latency from the arXiv measurement study plus two vendor profiles [S-18][S-20][S-15]; cost from three sources whose thresholds disagree by three orders of magnitude [S-05][S-16][S-20]; evaluation from the one dedicated metrics article and the RAGAS-based builds [S-17][S-26]; and security from the threat reporting and access-control architecture pieces [S-27][S-24]. The brief also needs its evidence-frame and gaps sections because several sources do assert general winners — 'RAG is generally better for most enterprise use cases' [S-19] — and adopting those would violate the goal's instruction to avoid unsupported rankings; recording them as claims while presenting the disagreement openly is the honest alternative. The hybrid section is warranted rather than optional because the recommendation is near-unanimous [S-15][S-16][S-12], and the caution that hybrid inherits both systems' complexity [S-19] keeps it from becoming a fourth unsupported ranking.
