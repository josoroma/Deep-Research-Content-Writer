# Research synthesis: RAG vs fine-tuning

Help an engineering team choose between RAG, fine-tuning, and a hybrid approach for enterprise AI assistants by comparing data freshness, evaluation, latency, cost, and security while preserving evidence limits and avoiding unsupported rankings.

Format: Comparative decision brief: dimension-by-dimension tradeoff analysis with an explicit evidence-strength column and a staged decision guide. The reader has to make one architecture call across five named dimensions, and the corpus supports exactly that shape: every dimension has directional claims, several dimensions have internal disagreement, and none has measurement. A dimension-by-dimension brief lets each dimension carry its own confidence, states where sources conflict (for example retrieval cost at scale, or whether fine-tuning is always faster), and ends with the staged path the sources actually converge on instead of a winner. The matrix keeps the reader's five criteria visible so no dimension is silently dropped, and the evidence-strength column is the mechanism that preserves the corpus's limits rather than hiding them.

## How to read this brief: what the corpus can and cannot settle

Give the reader the provenance of the evidence up front — eighteen extracted pages, almost all vendor-authored, dated between January 2024 and October 2026 — and set the rule that no overall winner will be declared, only per-dimension judgments with stated confidence.

Most of the corpus is vendor-authored — company blogs, a whitepaper, GPU-cloud and retrieval-platform marketing — and its quantitative claims are presented as vendor experience (deal ratios, client outcomes, pilot ranges) rather than as measurement. [S-20] [S-11] [S-30] [S-04]

- Qualification: S-30's 20% figure is attached to the vendor's product deployment, so it does not isolate the effect of retrieval versus fine-tuning.

- Qualification: Several sources close with calls to book a call, start an assessment, or contact sales, which is context for how their comparisons are framed.

Some numbers in the corpus are unsourced and should not be carried into a decision, including a '30% of customers' outdated-answer anecdote, a '20–30%' tone-and-satisfaction effect, and an analyst-firm adoption forecast. [S-15] [S-15] [S-06]

- Qualification: None of these claims carries a citation, dataset, or method, and the anecdotes are unattributed, so they cannot be verified or bounded.

- Qualification: They are plausible marketing motivators, not inputs to an architecture decision.

The guidance spans January 2024 to October 2026, and the newest sources explicitly re-date older advice — 2023-era retrieval thresholds, RLHF as the default alignment method, and the 'stuff versus retrieve' rule are declared obsolete — so any recommendation must carry its publication date. [S-20] [S-20] [S-20]

- Qualification: The claim that the landscape shifted is itself made by a vendor blog, and its five 'developments' are asserted without references or measurements.

- Qualification: The corpus contains only one source dated after mid-2026 (S-11, October 2026), so the newest picture rests on a thin, single-vendor base.

- qualifies: | **Knowledge is dynamic, proprietary, or larger than the context window** | **RAG** (start with hybrid retrieval + re-ranker) | Updates in minutes, citable sources, no retraining cost. | [S-20]

Limitation: This section's own basis is corpus metadata rather than content: twelve of the thirty ranked URLs were never extracted, so the sample cannot be characterised as representative of available guidance.

## The reframing the sources agree on: knowledge versus behaviour

Establish the shared framing that retrieval changes what the assistant knows and fine-tuning changes how it behaves, so the rest of the brief compares capabilities instead of crowning a technique.

The sources converge on a reframing rather than a contest: retrieval governs what an assistant knows and how current that knowledge is, while fine-tuning governs how it behaves (style, format, task shape), so the two are complementary capabilities instead of interchangeable substitutes. [S-20] [S-17] [S-09] [S-15]

- Qualification: The framing is asserted by the same vendor-authored sources that sell implementation services; none of them tests it empirically or against a controlled task set.

- Qualification: S-20 itself presents the framing as the answer to 'is RAG better than fine-tuning', which is an editorial position rather than an experimental result.

The corpus converges on a staged path rather than a single choice: start with retrieval because it is faster and cheaper to iterate and because it exposes which behaviour gaps remain, measure under real traffic, then fine-tune only the residual voice, format, or narrow-reasoning gaps, with hybrid described as the usual production endpoint. [S-17] [S-17] [S-04] [S-20] [S-11] [S-09] [S-06]

- Qualification: The sequencing advice comes from development agencies and platform vendors who sell the staged work; no source reports a deployment where the sequence was followed and measured.

- Qualification: The ordering also assumes the reader can afford two rounds of investment, which the corpus does not test against budget-constrained teams.

Hybrid is described consistently at the architecture level — fine-tuning for tone, format, or domain reasoning plus retrieval for facts, sometimes named RAFT — with an explicit warning that it adds routing decisions and synchronisation between model checkpoints and retrieval indexes. [S-17] [S-01] [S-15] [S-08]

- Qualification: RAFT is described by reference to papers and vendor practice; no source in the corpus reports implementing or measuring a hybrid assistant.

- Qualification: The complexity warning is qualitative; no source estimates the engineering or evaluation overhead of the coordination layer.

- qualifies: - **Synchronization of Model and Knowledge Base:** As your domain evolves, you must ensure that updates to the fine-tuned model remain aligned with updates to the retrieval database. [S-08]

## Data freshness and knowledge updates

Show the dimension with the strongest and most convergent support, and give the reader the operational consequence: update an index versus run a retraining cadence.

Freshness is the best-supported differentiator in the corpus: retrieval-based systems absorb new or corrected information by updating a document store or index, whereas a fine-tuned model is a snapshot of its training data whose currency depends on a retraining cadence. [S-01] [S-15] [S-06] [S-10] [S-17] [S-13] [S-20]

- Qualification: Every source making this claim is a vendor or consultancy blog; none measures how quickly an update propagates or whether accuracy holds after an update.

- Qualification: The magnitude of the freshness advantage is never quantified (no update-latency or drift measurements appear anywhere in the corpus).

The newest sources argue that long-context prompting with prefix caching can replace retrieval for corpora that fit the window and change slowly, which reshapes the cost and freshness calculus while leaving the knowledge/behaviour split intact. [S-20] [S-20] [S-20] [S-20] [S-17]

- Qualification: Both sources are 2026-dated vendor blog posts; the cache-discount percentages and the cost reversal are asserted without measurements, and their corpus-size thresholds differ (200k versus up to 1M tokens).

- Qualification: Long context does not address citation-per-answer or per-document access control, which those same sources still credit to retrieval.

The guidance spans January 2024 to October 2026, and the newest sources explicitly re-date older advice — 2023-era retrieval thresholds, RLHF as the default alignment method, and the 'stuff versus retrieve' rule are declared obsolete — so any recommendation must carry its publication date. [S-20] [S-20] [S-20]

- Qualification: The claim that the landscape shifted is itself made by a vendor blog, and its five 'developments' are asserted without references or measurements.

- Qualification: The corpus contains only one source dated after mid-2026 (S-11, October 2026), so the newest picture rests on a thin, single-vendor base.

- qualifies: | **Knowledge is dynamic, proprietary, or larger than the context window** | **RAG** (start with hybrid retrieval + re-ranker) | Updates in minutes, citable sources, no retraining cost. | [S-20]

### Why the update cadence, not the technique, is the first filter

Turn the freshness finding into a concrete question for the reader's assistant: how often do the underlying facts or policies change, and who owns the update path in each architecture.

Freshness is the best-supported differentiator in the corpus: retrieval-based systems absorb new or corrected information by updating a document store or index, whereas a fine-tuned model is a snapshot of its training data whose currency depends on a retraining cadence. [S-01] [S-15] [S-06] [S-10] [S-17] [S-13] [S-20]

- Qualification: Every source making this claim is a vendor or consultancy blog; none measures how quickly an update propagates or whether accuracy holds after an update.

- Qualification: The magnitude of the freshness advantage is never quantified (no update-latency or drift measurements appear anywhere in the corpus).

The corpus converges on a staged path rather than a single choice: start with retrieval because it is faster and cheaper to iterate and because it exposes which behaviour gaps remain, measure under real traffic, then fine-tune only the residual voice, format, or narrow-reasoning gaps, with hybrid described as the usual production endpoint. [S-17] [S-17] [S-04] [S-20] [S-11] [S-09] [S-06]

- Qualification: The sequencing advice comes from development agencies and platform vendors who sell the staged work; no source reports a deployment where the sequence was followed and measured.

- Qualification: The ordering also assumes the reader can afford two rounds of investment, which the corpus does not test against budget-constrained teams.

## Evaluation and measurement

Present the corpus's most actionable material as practice while flagging that no source reports results, so the team knows what to build and that it cannot borrow anyone's numbers.

Evaluation practice is the corpus's most concrete operational material: build a small eval set with expected answers before changing anything, re-run it after every change to chunking, embedding, retrieval, or prompt, use task-specific evals rather than training loss, and compare against a strong retrieval baseline — but no source reports the results of any such evaluation. [S-04] [S-04] [S-17] [S-20] [S-20] [S-08]

- Qualification: The prescribed eval-set sizes (100 queries, 30 prompts) are vendor heuristics; no source shares the eval sets, metric definitions, or pass thresholds.

- Qualification: No source reports a before/after score for a real deployment, so the guidance can be adopted but its sufficiency cannot be judged from this corpus.

Only one research-grade comparison is discussed in the corpus, and it reaches the reader second-hand: a GPU-cloud vendor post summarises a 2024 Microsoft Research MMLU study and a Berkeley RAFT paper, then cautions that the accuracy advantage applies to informational questions rather than all tasks. [S-21] [S-21] [S-21]

- Qualification: The underlying papers (arXiv 2312.05934 and 2403.10131) are not part of the extracted corpus, and no scores, sample sizes, or confidence intervals are reproduced.

- Qualification: The summarising source is a GPU-cloud vendor whose post also promotes running these workloads on its platform.

- qualifies: While this study shows RAG often outperforms on informational accuracy, this is only one of many use cases. Fine-tuning could perform better than RAG at other tasks like sentiment analysis, NSFW content detection, and tone of voice curation. [S-21]

Limitation: No source in this corpus reports an eval set, metric definition, or measured score for either approach; the guidance is prescriptive only.

### The measurement practices the corpus prescribes

Collect the recurring prescriptions — a small labelled eval set before any change, re-runs after every pipeline change, task-specific evals rather than loss, comparison against a retrieval baseline — into a checklist a team can adopt.

Evaluation practice is the corpus's most concrete operational material: build a small eval set with expected answers before changing anything, re-run it after every change to chunking, embedding, retrieval, or prompt, use task-specific evals rather than training loss, and compare against a strong retrieval baseline — but no source reports the results of any such evaluation. [S-04] [S-04] [S-17] [S-20] [S-20] [S-08]

- Qualification: The prescribed eval-set sizes (100 queries, 30 prompts) are vendor heuristics; no source shares the eval sets, metric definitions, or pass thresholds.

- Qualification: No source reports a before/after score for a real deployment, so the guidance can be adopted but its sufficiency cannot be judged from this corpus.

The corpus converges on a staged path rather than a single choice: start with retrieval because it is faster and cheaper to iterate and because it exposes which behaviour gaps remain, measure under real traffic, then fine-tune only the residual voice, format, or narrow-reasoning gaps, with hybrid described as the usual production endpoint. [S-17] [S-17] [S-04] [S-20] [S-11] [S-09] [S-06]

- Qualification: The sequencing advice comes from development agencies and platform vendors who sell the staged work; no source reports a deployment where the sequence was followed and measured.

- Qualification: The ordering also assumes the reader can afford two rounds of investment, which the corpus does not test against budget-constrained teams.

### The only research-grade comparison reaches the reader second-hand

Explain precisely what the MMLU and RAFT references do and do not establish, so the team does not cite them as proof that retrieval wins on accuracy.

Only one research-grade comparison is discussed in the corpus, and it reaches the reader second-hand: a GPU-cloud vendor post summarises a 2024 Microsoft Research MMLU study and a Berkeley RAFT paper, then cautions that the accuracy advantage applies to informational questions rather than all tasks. [S-21] [S-21] [S-21]

- Qualification: The underlying papers (arXiv 2312.05934 and 2403.10131) are not part of the extracted corpus, and no scores, sample sizes, or confidence intervals are reproduced.

- Qualification: The summarising source is a GPU-cloud vendor whose post also promotes running these workloads on its platform.

- qualifies: While this study shows RAG often outperforms on informational accuracy, this is only one of many use cases. Fine-tuning could perform better than RAG at other tasks like sentiment analysis, NSFW content detection, and tone of voice curation. [S-21]

Limitation: The referenced papers are not in the corpus, and the summarising source is a vendor blog.

## Latency

Lay out the retrieval-hop cost, the agentic multiplier, and the contested claim that fine-tuning is always faster, so the team can size a latency budget rather than rely on a slogan.

Latency evidence is directional and partly contested: retrieval adds a hop quoted at 100–400 ms (and 3–10x for agentic multi-step retrieval), several sources say fine-tuning answers faster because knowledge is internalized, and one source warns that a fine-tuned model may be larger or more complex and therefore slower at inference. [S-17] [S-20] [S-06] [S-01] [S-15] [S-21] [S-08] [S-08]

- Qualification: No controlled latency benchmark appears in the corpus; the 100–400 ms hop and the 3–10x agentic multiplier are practitioner estimates from vendor or consultancy posts.

- Qualification: Latency is not decomposed by pipeline configuration (embedding, reranking, cache hit rate, model size), so the numbers cannot be applied directly to a given architecture.

- contradicts: - **Tradeoffs in Inference Speed:** A fine-tuned model may be larger or more complex than a retrieval-based alternative, which can impact**inference speed** , especially in production environments with latency constraints. [S-08]

- qualifies: - **Internalized Knowledge:** The model doesn’t need to retrieve information externally; instead, it can generate contextually aware, fluent answers based on what it has learned, resulting in faster**response generation** and consistent tone. [S-08]

The newest sources argue that long-context prompting with prefix caching can replace retrieval for corpora that fit the window and change slowly, which reshapes the cost and freshness calculus while leaving the knowledge/behaviour split intact. [S-20] [S-20] [S-20] [S-20] [S-17]

- Qualification: Both sources are 2026-dated vendor blog posts; the cache-discount percentages and the cost reversal are asserted without measurements, and their corpus-size thresholds differ (200k versus up to 1M tokens).

- Qualification: Long context does not address citation-per-answer or per-document access control, which those same sources still credit to retrieval.

Some numbers in the corpus are unsourced and should not be carried into a decision, including a '30% of customers' outdated-answer anecdote, a '20–30%' tone-and-satisfaction effect, and an analyst-firm adoption forecast. [S-15] [S-15] [S-06]

- Qualification: None of these claims carries a citation, dataset, or method, and the anecdotes are unattributed, so they cannot be verified or bounded.

- Qualification: They are plausible marketing motivators, not inputs to an architecture decision.

Limitation: There are no controlled latency benchmarks in the corpus, and the quoted figures are unattributed practitioner estimates.

### The retrieval hop: what the numbers claim and what they omit

Give the reader the 100–400 ms and 3–10x figures with their provenance and the configuration detail they leave out, plus the long-context branch where no retrieval hop exists.

Latency evidence is directional and partly contested: retrieval adds a hop quoted at 100–400 ms (and 3–10x for agentic multi-step retrieval), several sources say fine-tuning answers faster because knowledge is internalized, and one source warns that a fine-tuned model may be larger or more complex and therefore slower at inference. [S-17] [S-20] [S-06] [S-01] [S-15] [S-21] [S-08] [S-08]

- Qualification: No controlled latency benchmark appears in the corpus; the 100–400 ms hop and the 3–10x agentic multiplier are practitioner estimates from vendor or consultancy posts.

- Qualification: Latency is not decomposed by pipeline configuration (embedding, reranking, cache hit rate, model size), so the numbers cannot be applied directly to a given architecture.

- contradicts: - **Tradeoffs in Inference Speed:** A fine-tuned model may be larger or more complex than a retrieval-based alternative, which can impact**inference speed** , especially in production environments with latency constraints. [S-08]

- qualifies: - **Internalized Knowledge:** The model doesn’t need to retrieve information externally; instead, it can generate contextually aware, fluent answers based on what it has learned, resulting in faster**response generation** and consistent tone. [S-08]

The newest sources argue that long-context prompting with prefix caching can replace retrieval for corpora that fit the window and change slowly, which reshapes the cost and freshness calculus while leaving the knowledge/behaviour split intact. [S-20] [S-20] [S-20] [S-20] [S-17]

- Qualification: Both sources are 2026-dated vendor blog posts; the cache-discount percentages and the cost reversal are asserted without measurements, and their corpus-size thresholds differ (200k versus up to 1M tokens).

- Qualification: Long context does not address citation-per-answer or per-document access control, which those same sources still credit to retrieval.

### The contested claim that fine-tuning always answers faster

Show the conflict between the sources that treat internalized knowledge as faster and the source warning that a fine-tuned model may be larger or more complex, so latency is treated as an empirical question for the team's own stack.

Latency evidence is directional and partly contested: retrieval adds a hop quoted at 100–400 ms (and 3–10x for agentic multi-step retrieval), several sources say fine-tuning answers faster because knowledge is internalized, and one source warns that a fine-tuned model may be larger or more complex and therefore slower at inference. [S-17] [S-20] [S-06] [S-01] [S-15] [S-21] [S-08] [S-08]

- Qualification: No controlled latency benchmark appears in the corpus; the 100–400 ms hop and the 3–10x agentic multiplier are practitioner estimates from vendor or consultancy posts.

- Qualification: Latency is not decomposed by pipeline configuration (embedding, reranking, cache hit rate, model size), so the numbers cannot be applied directly to a given architecture.

- contradicts: - **Tradeoffs in Inference Speed:** A fine-tuned model may be larger or more complex than a retrieval-based alternative, which can impact**inference speed** , especially in production environments with latency constraints. [S-08]

- qualifies: - **Internalized Knowledge:** The model doesn’t need to retrieve information externally; instead, it can generate contextually aware, fluent answers based on what it has learned, resulting in faster**response generation** and consistent tone. [S-08]

## Cost

Separate setup cost from per-query cost, present the quoted ranges with their sources, and make the disagreement about retrieval cost at scale explicit instead of averaging it away.

Cost evidence is directional rather than measured: retrieval is described as cheap to set up with ongoing per-query and storage costs, fine-tuning as a large one-time training investment with cheaper per-query inference, with quoted ranges such as low-five-figures for a retrieval pilot and $1,000–$20,000 for a LoRA training run. [S-04] [S-04] [S-11] [S-15] [S-03]

- Qualification: Figures come from vendor blogs and a GPU-cloud vendor's scenario lists; scopes differ (embedding spend, per-query token cost, GPU-hour hosting, one-time training spend) and none is audited or reproducible.

- Qualification: The $0.53–$7.34 per hour figure is a second-hand citation of another site about hosting a 70B model, not a measured cost of either technique.

Sources disagree about retrieval's cost trajectory: one enterprise whitepaper presents RAG as cost-efficient with minimal overhead, while other sources stress that per-query retrieval and larger prompts make retrieval more expensive at scale. [S-06] [S-15] [S-20]

- Qualification: The disagreement is about framing rather than measurements: no source in the corpus provides a cost model, token accounting, or a worked total-cost comparison.

- Qualification: S-06 is a service-provider whitepaper whose summary section also markets the provider's own AI strategy services.

The economic crossover between the two approaches is asserted rather than derived: one source states that below roughly 100,000 queries per month the economics favour retrieval, and another says fine-tuning becomes cheaper per answer once deployed. [S-04] [S-15]

- Qualification: Neither source shows the arithmetic, token counts, or price assumptions behind the crossover, and both are vendor-authored.

- Qualification: The threshold is stated in queries per month while the other cost figures in the corpus are per-query or one-time, so the two cannot be reconciled from this evidence.

Limitation: All figures are vendor estimates in incompatible units; no total-cost model exists in the corpus.

### Two cost shapes: paying to index versus paying to train

Contrast the retrieval cost profile (fast, cheap setup; per-query and storage ongoing) with the fine-tuning profile (large one-time training; cheaper inference), using the corpus's own ranges.

Cost evidence is directional rather than measured: retrieval is described as cheap to set up with ongoing per-query and storage costs, fine-tuning as a large one-time training investment with cheaper per-query inference, with quoted ranges such as low-five-figures for a retrieval pilot and $1,000–$20,000 for a LoRA training run. [S-04] [S-04] [S-11] [S-15] [S-03]

- Qualification: Figures come from vendor blogs and a GPU-cloud vendor's scenario lists; scopes differ (embedding spend, per-query token cost, GPU-hour hosting, one-time training spend) and none is audited or reproducible.

- Qualification: The $0.53–$7.34 per hour figure is a second-hand citation of another site about hosting a 70B model, not a measured cost of either technique.

How much labelled data justifies fine-tuning is not settled in the corpus: quoted thresholds range from 'at least 1,000 clean labeled examples' through 'a few hundred to a few thousand' to '>10,000' examples, depending on the source and the fine-tuning method. [S-17] [S-20] [S-04]

- Qualification: None of the thresholds is tied to a measured fine-tuning result or to a stated task difficulty; they are heuristics from vendor playbooks.

- Qualification: The sources also disagree on weighting quality versus quantity, so the numbers cannot be treated as a data-readiness gate with a single answer.

- qualifies: Do you have >10,000 labelled examples of the behaviour you want? Fine-tune. [S-04]

### Where the cost claims conflict and where the crossover is asserted

Show the reader that one whitepaper calls retrieval cost-efficient while other sources describe rising retrieval cost at scale, and present the ~100k-queries-per-month crossover as an unverified assertion.

Sources disagree about retrieval's cost trajectory: one enterprise whitepaper presents RAG as cost-efficient with minimal overhead, while other sources stress that per-query retrieval and larger prompts make retrieval more expensive at scale. [S-06] [S-15] [S-20]

- Qualification: The disagreement is about framing rather than measurements: no source in the corpus provides a cost model, token accounting, or a worked total-cost comparison.

- Qualification: S-06 is a service-provider whitepaper whose summary section also markets the provider's own AI strategy services.

The economic crossover between the two approaches is asserted rather than derived: one source states that below roughly 100,000 queries per month the economics favour retrieval, and another says fine-tuning becomes cheaper per answer once deployed. [S-04] [S-15]

- Qualification: Neither source shows the arithmetic, token counts, or price assumptions behind the crossover, and both are vendor-authored.

- Qualification: The threshold is stated in queries per month while the other cost figures in the corpus are per-query or one-time, so the two cannot be reconciled from this evidence.

## Security, access control, and compliance

Compare the two options on authorization, exposure surface, training-data obligations, and auditability, while stating that the security sources are mostly generic rather than tradeoff-specific.

Retrieval is the layer that can enforce authorization per document and per caller and that can return inspectable, citable evidence; a fine-tuned model stores learned content in weights that cannot be inspected or filtered per user. [S-13] [S-20] [S-17] [S-15]

- Qualification: The per-document filtering claim is architectural reasoning from three vendor sources; none reports implementing or testing an access-control scheme.

- Qualification: 'fine-tuning without RAG rarely survives a compliance review' is an unsourced assertion from a development agency's blog.

Retrieval also expands the exposure surface: connectors, index copies, cached context, and prompt/response logs create additional places where sensitive data is stored or reused, so retrieval security depends on scoping, classification, and least privilege rather than on the technique itself. [S-26] [S-26] [S-26] [S-26] [S-08] [S-30]

- Qualification: S-26 is anonymous FAQ-style content from a non-human-identity vendor, and S-30 is retrieval-platform marketing that uses the same Copilot incident to introduce its own product.

- Qualification: No source quantifies how much extra exposure a retrieval stack adds, and none examines a specific enterprise access-control implementation.

Fine-tuning relocates security obligations rather than removing them: training data must respect consent and bias audits, and one study summarised in the corpus claims fine-tuning can degrade safety alignment and jailbreak resistance, while another source asserts the opposite direction of leakage risk without evidence. [S-15] [S-28] [S-25] [S-15]

- Qualification: The alignment claim arrives as a one-paragraph digest summary of someone else's study; neither the study nor any measurement is in the corpus.

- Qualification: S-15's 'less likely to leak private files' statement sits beside its own table row requiring consent and bias audits for training data, so the corpus is internally inconsistent on this point.

- qualifies: Does it always work? Probably not. Does it generally work? Yes, because you are providing guard rails for the LLM from which they shouldn’t deviate. [S-25]

- qualifies: Fine-Tuning keeps all data inside the model, so it’s less likely to leak private files. [S-15]

Security coverage in the corpus is mostly generic LLM-security material — prompt injection, jailbreaks, rate limiting, EU AI Act scope, and attack-surface framing — rather than evidence about which customization approach is safer in a RAG-versus-fine-tuning decision. [S-25] [S-28] [S-28] [S-26]

- Qualification: S-25 dates from January 2024 and S-28 from June 2024; both predate the agentic-retrieval and long-context patterns the newest sources discuss.

- Qualification: S-28 is a curated link digest rather than original analysis, so its claims are at least one step removed from primary sources.

- qualifies: That tradeoff is especially visible in retrieval-augmented generation, enterprise copilots, and agentic tools, where the system must be trusted to fetch relevant context on behalf of the user. [S-26]

Audit and compliance requirements pull designs toward retrieval: citations let a reviewer trace an answer to a specific source, regulated-domain guidance in the corpus points to retrieval or hybrid, and the corpus frames regulatory exposure under the EU AI Act as context for that choice. [S-17] [S-13] [S-15] [S-28]

- Qualification: No source in the corpus cites a specific regulatory requirement that mandates citation or forbids weight-embedded knowledge for assistants.

- Qualification: The strongest compliance phrasing ('rarely survives a compliance review') is an unsourced assertion in a development agency's blog post.

Limitation: Only a minority of the security sources (S-13, S-15, S-20, S-26) address retrieval or weight-embedded knowledge directly; the rest are general LLM-security guidance, partly predating current architectures.

### Access control is enforced at retrieval time, not at generation time

Explain why per-document and per-caller filtering plus citable evidence makes retrieval the natural control point for assistants that must respect entitlements.

Retrieval is the layer that can enforce authorization per document and per caller and that can return inspectable, citable evidence; a fine-tuned model stores learned content in weights that cannot be inspected or filtered per user. [S-13] [S-20] [S-17] [S-15]

- Qualification: The per-document filtering claim is architectural reasoning from three vendor sources; none reports implementing or testing an access-control scheme.

- Qualification: 'fine-tuning without RAG rarely survives a compliance review' is an unsourced assertion from a development agency's blog.

Audit and compliance requirements pull designs toward retrieval: citations let a reviewer trace an answer to a specific source, regulated-domain guidance in the corpus points to retrieval or hybrid, and the corpus frames regulatory exposure under the EU AI Act as context for that choice. [S-17] [S-13] [S-15] [S-28]

- Qualification: No source in the corpus cites a specific regulatory requirement that mandates citation or forbids weight-embedded knowledge for assistants.

- Qualification: The strongest compliance phrasing ('rarely survives a compliance review') is an unsourced assertion in a development agency's blog post.

### Retrieval widens the exposure surface as well as controlling it

Balance the previous section with connectors, index copies, cache, and logging paths, and with the least-privilege and scoping tests the corpus recommends.

Retrieval also expands the exposure surface: connectors, index copies, cached context, and prompt/response logs create additional places where sensitive data is stored or reused, so retrieval security depends on scoping, classification, and least privilege rather than on the technique itself. [S-26] [S-26] [S-26] [S-26] [S-08] [S-30]

- Qualification: S-26 is anonymous FAQ-style content from a non-human-identity vendor, and S-30 is retrieval-platform marketing that uses the same Copilot incident to introduce its own product.

- Qualification: No source quantifies how much extra exposure a retrieval stack adds, and none examines a specific enterprise access-control implementation.

Security coverage in the corpus is mostly generic LLM-security material — prompt injection, jailbreaks, rate limiting, EU AI Act scope, and attack-surface framing — rather than evidence about which customization approach is safer in a RAG-versus-fine-tuning decision. [S-25] [S-28] [S-28] [S-26]

- Qualification: S-25 dates from January 2024 and S-28 from June 2024; both predate the agentic-retrieval and long-context patterns the newest sources discuss.

- Qualification: S-28 is a curated link digest rather than original analysis, so its claims are at least one step removed from primary sources.

- qualifies: That tradeoff is especially visible in retrieval-augmented generation, enterprise copilots, and agentic tools, where the system must be trusted to fetch relevant context on behalf of the user. [S-26]

### Fine-tuning's security trade is not free

Cover training-data consent and audit obligations plus the cited claim that fine-tuning can degrade safety alignment, and note the corpus's internal inconsistency about leakage risk.

Fine-tuning relocates security obligations rather than removing them: training data must respect consent and bias audits, and one study summarised in the corpus claims fine-tuning can degrade safety alignment and jailbreak resistance, while another source asserts the opposite direction of leakage risk without evidence. [S-15] [S-28] [S-25] [S-15]

- Qualification: The alignment claim arrives as a one-paragraph digest summary of someone else's study; neither the study nor any measurement is in the corpus.

- Qualification: S-15's 'less likely to leak private files' statement sits beside its own table row requiring consent and bias audits for training data, so the corpus is internally inconsistent on this point.

- qualifies: Does it always work? Probably not. Does it generally work? Yes, because you are providing guard rails for the LLM from which they shouldn’t deviate. [S-25]

- qualifies: Fine-Tuning keeps all data inside the model, so it’s less likely to leak private files. [S-15]

Retrieval is the layer that can enforce authorization per document and per caller and that can return inspectable, citable evidence; a fine-tuned model stores learned content in weights that cannot be inspected or filtered per user. [S-13] [S-20] [S-17] [S-15]

- Qualification: The per-document filtering claim is architectural reasoning from three vendor sources; none reports implementing or testing an access-control scheme.

- Qualification: 'fine-tuning without RAG rarely survives a compliance review' is an unsourced assertion from a development agency's blog.

## A staged path the evidence supports

Convert the dimensions into a sequence the team can execute: retrieval first for changing or citable knowledge, a measurement period, then targeted fine-tuning for residual gaps, with hybrid as the likely endpoint.

The corpus converges on a staged path rather than a single choice: start with retrieval because it is faster and cheaper to iterate and because it exposes which behaviour gaps remain, measure under real traffic, then fine-tune only the residual voice, format, or narrow-reasoning gaps, with hybrid described as the usual production endpoint. [S-17] [S-17] [S-04] [S-20] [S-11] [S-09] [S-06]

- Qualification: The sequencing advice comes from development agencies and platform vendors who sell the staged work; no source reports a deployment where the sequence was followed and measured.

- Qualification: The ordering also assumes the reader can afford two rounds of investment, which the corpus does not test against budget-constrained teams.

Hybrid is described consistently at the architecture level — fine-tuning for tone, format, or domain reasoning plus retrieval for facts, sometimes named RAFT — with an explicit warning that it adds routing decisions and synchronisation between model checkpoints and retrieval indexes. [S-17] [S-01] [S-15] [S-08]

- Qualification: RAFT is described by reference to papers and vendor practice; no source in the corpus reports implementing or measuring a hybrid assistant.

- Qualification: The complexity warning is qualitative; no source estimates the engineering or evaluation overhead of the coordination layer.

- qualifies: - **Synchronization of Model and Knowledge Base:** As your domain evolves, you must ensure that updates to the fine-tuned model remain aligned with updates to the retrieval database. [S-08]

How much labelled data justifies fine-tuning is not settled in the corpus: quoted thresholds range from 'at least 1,000 clean labeled examples' through 'a few hundred to a few thousand' to '>10,000' examples, depending on the source and the fine-tuning method. [S-17] [S-20] [S-04]

- Qualification: None of the thresholds is tied to a measured fine-tuning result or to a stated task difficulty; they are heuristics from vendor playbooks.

- Qualification: The sources also disagree on weighting quality versus quantity, so the numbers cannot be treated as a data-readiness gate with a single answer.

- qualifies: Do you have >10,000 labelled examples of the behaviour you want? Fine-tune. [S-04]

Freshness is the best-supported differentiator in the corpus: retrieval-based systems absorb new or corrected information by updating a document store or index, whereas a fine-tuned model is a snapshot of its training data whose currency depends on a retraining cadence. [S-01] [S-15] [S-06] [S-10] [S-17] [S-13] [S-20]

- Qualification: Every source making this claim is a vendor or consultancy blog; none measures how quickly an update propagates or whether accuracy holds after an update.

- Qualification: The magnitude of the freshness advantage is never quantified (no update-latency or drift measurements appear anywhere in the corpus).

Retrieval also expands the exposure surface: connectors, index copies, cached context, and prompt/response logs create additional places where sensitive data is stored or reused, so retrieval security depends on scoping, classification, and least privilege rather than on the technique itself. [S-26] [S-26] [S-26] [S-26] [S-08] [S-30]

- Qualification: S-26 is anonymous FAQ-style content from a non-human-identity vendor, and S-30 is retrieval-platform marketing that uses the same Copilot incident to introduce its own product.

- Qualification: No source quantifies how much extra exposure a retrieval stack adds, and none examines a specific enterprise access-control implementation.

Limitation: The sequencing is recommended by vendor and agency playbooks; no source reports a deployment that followed it and was measured.

### Start with retrieval, then measure, then fine-tune the gaps

Justify the ordering from the sources' reasoning — cheaper iteration, faster learning under real traffic, and observable failure modes — and attach the measurement requirement from the evaluation section.

The corpus converges on a staged path rather than a single choice: start with retrieval because it is faster and cheaper to iterate and because it exposes which behaviour gaps remain, measure under real traffic, then fine-tune only the residual voice, format, or narrow-reasoning gaps, with hybrid described as the usual production endpoint. [S-17] [S-17] [S-04] [S-20] [S-11] [S-09] [S-06]

- Qualification: The sequencing advice comes from development agencies and platform vendors who sell the staged work; no source reports a deployment where the sequence was followed and measured.

- Qualification: The ordering also assumes the reader can afford two rounds of investment, which the corpus does not test against budget-constrained teams.

Evaluation practice is the corpus's most concrete operational material: build a small eval set with expected answers before changing anything, re-run it after every change to chunking, embedding, retrieval, or prompt, use task-specific evals rather than training loss, and compare against a strong retrieval baseline — but no source reports the results of any such evaluation. [S-04] [S-04] [S-17] [S-20] [S-20] [S-08]

- Qualification: The prescribed eval-set sizes (100 queries, 30 prompts) are vendor heuristics; no source shares the eval sets, metric definitions, or pass thresholds.

- Qualification: No source reports a before/after score for a real deployment, so the guidance can be adopted but its sufficiency cannot be judged from this corpus.

### Hybrid patterns: what they buy and what they cost in complexity

Describe the fine-tune-for-behaviour plus retrieve-for-facts architecture, name RAFT, and state the routing and synchronisation burden it adds.

Hybrid is described consistently at the architecture level — fine-tuning for tone, format, or domain reasoning plus retrieval for facts, sometimes named RAFT — with an explicit warning that it adds routing decisions and synchronisation between model checkpoints and retrieval indexes. [S-17] [S-01] [S-15] [S-08]

- Qualification: RAFT is described by reference to papers and vendor practice; no source in the corpus reports implementing or measuring a hybrid assistant.

- Qualification: The complexity warning is qualitative; no source estimates the engineering or evaluation overhead of the coordination layer.

- qualifies: - **Synchronization of Model and Knowledge Base:** As your domain evolves, you must ensure that updates to the fine-tuned model remain aligned with updates to the retrieval database. [S-08]

The sources converge on a reframing rather than a contest: retrieval governs what an assistant knows and how current that knowledge is, while fine-tuning governs how it behaves (style, format, task shape), so the two are complementary capabilities instead of interchangeable substitutes. [S-20] [S-17] [S-09] [S-15]

- Qualification: The framing is asserted by the same vendor-authored sources that sell implementation services; none of them tests it empirically or against a controlled task set.

- Qualification: S-20 itself presents the framing as the answer to 'is RAG better than fine-tuning', which is an editorial position rather than an experimental result.

### Data-readiness gates before committing to fine-tuning

Show that the corpus's example-count thresholds diverge, so the team must pick its own gate based on the task and count its genuinely labelled examples.

How much labelled data justifies fine-tuning is not settled in the corpus: quoted thresholds range from 'at least 1,000 clean labeled examples' through 'a few hundred to a few thousand' to '>10,000' examples, depending on the source and the fine-tuning method. [S-17] [S-20] [S-04]

- Qualification: None of the thresholds is tied to a measured fine-tuning result or to a stated task difficulty; they are heuristics from vendor playbooks.

- Qualification: The sources also disagree on weighting quality versus quantity, so the numbers cannot be treated as a data-readiness gate with a single answer.

- qualifies: Do you have >10,000 labelled examples of the behaviour you want? Fine-tune. [S-04]

Evaluation practice is the corpus's most concrete operational material: build a small eval set with expected answers before changing anything, re-run it after every change to chunking, embedding, retrieval, or prompt, use task-specific evals rather than training loss, and compare against a strong retrieval baseline — but no source reports the results of any such evaluation. [S-04] [S-04] [S-17] [S-20] [S-20] [S-08]

- Qualification: The prescribed eval-set sizes (100 queries, 30 prompts) are vendor heuristics; no source shares the eval sets, metric definitions, or pass thresholds.

- Qualification: No source reports a before/after score for a real deployment, so the guidance can be adopted but its sufficiency cannot be judged from this corpus.

## Third options that bypass the retrieval-versus-fine-tuning choice

Give the reader the alternatives the newest sources raise — long-context prompting with caching and distillation into small task-specific models — so the decision space is complete, with their limits stated.

The newest sources argue that long-context prompting with prefix caching can replace retrieval for corpora that fit the window and change slowly, which reshapes the cost and freshness calculus while leaving the knowledge/behaviour split intact. [S-20] [S-20] [S-20] [S-20] [S-17]

- Qualification: Both sources are 2026-dated vendor blog posts; the cache-discount percentages and the cost reversal are asserted without measurements, and their corpus-size thresholds differ (200k versus up to 1M tokens).

- Qualification: Long context does not address citation-per-answer or per-document access control, which those same sources still credit to retrieval.

Distillation and small task-specific models appear as a third lever, justified on cost and latency grounds for narrow, high-volume work rather than as a fix for factual grounding. [S-29] [S-13] [S-20]

- Qualification: S-29 is a sponsored practitioner column about distillation that does not compare distillation with RAG or fine-tuning on any measured task.

- Qualification: The 'often beats a frontier API' claim is a vendor assertion with no benchmark, dataset, or evaluation detail attached.

The guidance spans January 2024 to October 2026, and the newest sources explicitly re-date older advice — 2023-era retrieval thresholds, RLHF as the default alignment method, and the 'stuff versus retrieve' rule are declared obsolete — so any recommendation must carry its publication date. [S-20] [S-20] [S-20]

- Qualification: The claim that the landscape shifted is itself made by a vendor blog, and its five 'developments' are asserted without references or measurements.

- Qualification: The corpus contains only one source dated after mid-2026 (S-11, October 2026), so the newest picture rests on a thin, single-vendor base.

- qualifies: | **Knowledge is dynamic, proprietary, or larger than the context window** | **RAG** (start with hybrid retrieval + re-ranker) | Updates in minutes, citable sources, no retraining cost. | [S-20]

### Long context plus prefix caching for small, slow-moving corpora

Explain when a static corpus that fits the window makes retrieval unnecessary, and why citation and per-document access control still argue for retrieval.

The newest sources argue that long-context prompting with prefix caching can replace retrieval for corpora that fit the window and change slowly, which reshapes the cost and freshness calculus while leaving the knowledge/behaviour split intact. [S-20] [S-20] [S-20] [S-20] [S-17]

- Qualification: Both sources are 2026-dated vendor blog posts; the cache-discount percentages and the cost reversal are asserted without measurements, and their corpus-size thresholds differ (200k versus up to 1M tokens).

- Qualification: Long context does not address citation-per-answer or per-document access control, which those same sources still credit to retrieval.

Retrieval is the layer that can enforce authorization per document and per caller and that can return inspectable, citable evidence; a fine-tuned model stores learned content in weights that cannot be inspected or filtered per user. [S-13] [S-20] [S-17] [S-15]

- Qualification: The per-document filtering claim is architectural reasoning from three vendor sources; none reports implementing or testing an access-control scheme.

- Qualification: 'fine-tuning without RAG rarely survives a compliance review' is an unsourced assertion from a development agency's blog.

### Distillation and small task-specific models for narrow, high-volume work

Position distillation as a cost and latency lever that does not solve grounding, so it complements rather than replaces the main decision.

Distillation and small task-specific models appear as a third lever, justified on cost and latency grounds for narrow, high-volume work rather than as a fix for factual grounding. [S-29] [S-13] [S-20]

- Qualification: S-29 is a sponsored practitioner column about distillation that does not compare distillation with RAG or fine-tuning on any measured task.

- Qualification: The 'often beats a frontier API' claim is a vendor assertion with no benchmark, dataset, or evaluation detail attached.

Cost evidence is directional rather than measured: retrieval is described as cheap to set up with ongoing per-query and storage costs, fine-tuning as a large one-time training investment with cheaper per-query inference, with quoted ranges such as low-five-figures for a retrieval pilot and $1,000–$20,000 for a LoRA training run. [S-04] [S-04] [S-11] [S-15] [S-03]

- Qualification: Figures come from vendor blogs and a GPU-cloud vendor's scenario lists; scopes differ (embedding spend, per-query token cost, GPU-hour hosting, one-time training spend) and none is audited or reproducible.

- Qualification: The $0.53–$7.34 per hour figure is a second-hand citation of another site about hosting a 70B model, not a measured cost of either technique.

## What would change this recommendation, and what the corpus cannot answer

List the missing measurements and the conditions that would flip the staged path — measured cost at the team's volume, a latency budget under a real pipeline, evidence that retrieval quality cannot be repaired, or a compliance requirement — so the team knows which pilot result to look for.

Limitation: This section rests entirely on corpus absences: no measured cost, latency, or evaluation data exists in the eighteen extracted sources, so its questions cannot be answered from this research.

Gap: No cost model: nothing in the corpus pairs token counts, retrieval volume, model prices, and evaluation labour into a comparable total cost of ownership for the two options.

Gap: No latency measurements: the 100–400 ms retrieval hop and the 3–10x agentic multiplier are unattributed practitioner estimates, not measurements for any named stack.

Gap: No evaluation artifacts: no source shares an eval set, metric definition, groundedness or retrieval-precision score, or before/after result for a RAG, fine-tuned, or hybrid assistant.

Gap: No primary benchmark: the MMLU and RAFT studies are cited second-hand and are absent from the corpus, so their magnitudes, conditions, and limits cannot be checked.

Gap: No evidence on hybrid orchestration failure modes: the routing rules and the risk of a fine-tuned model contradicting a fresher retrieval layer are named but never measured.

Gap: No data on the cost or latency of enforcing per-document access control inside a retrieval pipeline, which is exactly the control the corpus recommends.

Gap: No independent or third-party assessment of any vendor claim in the corpus, and no coverage of the twelve URLs that failed extraction (S-02, S-05, S-07, S-12, S-14, S-16, S-18, S-19, S-22, S-23, S-24, S-27).

Corpus limitation: Only 18 of 30 ranked URLs were extracted (S-02, S-05, S-07, S-12, S-14, S-16, S-18, S-19, S-22, S-23, S-24, S-27 are absent), so the corpus is a partial sample of the search results and nothing can be said about the missing pages.

Corpus limitation: Nearly every source is vendor-authored: company blogs, a whitepaper, GPU-cloud marketing, retrieval-platform marketing, and security-vendor posts, several ending in calls to contact sales or start an assessment.

Corpus limitation: No source reports its own controlled measurement of latency, cost, accuracy, or retrieval quality for RAG versus fine-tuning; the only benchmark discussion is a vendor post summarising external papers, which are not themselves in the corpus.

Corpus limitation: Figures are quoted in incompatible units and years (per-hour GPU hosting, per-query token cost, one-time training spend, percentage case-volume reductions) and cannot be combined into a total cost of ownership.

Corpus limitation: Security sources (S-25, S-26, S-28, S-30) address LLM security in general — prompt injection, jailbreaks, rate limiting, EU AI Act scope, attack-surface framing — rather than the RAG-versus-fine-tuning tradeoff; only S-13, S-15 and S-20 discuss per-document access control in a way that bears on the choice.

Corpus limitation: Publication dates range from January 2024 to October 2026, so the corpus mixes advice written before and after long-context prompting, prompt caching, agentic retrieval, and preference-optimization shifts; older and newer sources disagree partly because they describe different capability baselines.

Corpus limitation: Several headline numbers are unsourced or single-source (outdated-answer anecdotes, tone-satisfaction effects, adoption forecasts, vendor deal ratios, one claim that fine-tuning makes leakage less likely).

This is a decision brief rather than a tutorial or a ranked verdict because the reader's goal names five criteria and the corpus supplies directional claims for each without a single measurement. The framing that survives every source is that retrieval governs knowledge and freshness while fine-tuning governs behaviour [S-20][S-17][S-09], which makes the five dimensions the natural organising structure instead of a winner's podium. Freshness is the one dimension supported by many independent pages [S-01][S-06][S-10][S-13][S-15][S-17][S-20], so it carries the confidence and does most of the work in a staged path of retrieval first, measurement, then targeted fine-tuning [S-17][S-04][S-20]. Cost, latency, and evaluation are presented with their conflicts intact: retrieval is called both cost-efficient [S-06] and costlier at scale [S-15][S-20]; fine-tuning is called the faster option [S-01][S-06][S-15] while another same-source passage warns a fine-tuned model may be slower to serve [S-08]; and the only benchmark discussion arrives second-hand with an explicit scope limit [S-21]. Security is where the corpus is thinnest in the sense that matters: retrieval clearly owns per-document enforcement and citation [S-13][S-20][S-17], retrieval also widens the exposure surface through connectors and logs [S-26][S-08], fine-tuning shifts obligations to training-data consent and audit [S-15] and is claimed to weaken safety alignment [S-28] — but most security pages are generic LLM-security material about jailbreaks, prompt injection, and regulation rather than tradeoff analysis [S-25][S-28]. Confidence is therefore limited: vendor-authored sources, twelve unextracted URLs, no controlled benchmarks, and at least three unsourced statistics that a reader should discard [S-15][S-06]. The brief ends with the questions whose answers would actually move the decision, so the team can run the pilot that is missing from the literature rather than choosing on rhetoric.
