# Research synthesis: AI agent evaluation

Build a working evaluation setup for tool-using agents: choose task datasets, define success criteria, analyze failures, instrument observability, bound retries, and gate releases — while knowing which parts of the advice are documented in research or measured practice, and which are only vendor or single-team examples.

Format: Staged implementation guide with provenance labels on each practice. The goal asks readers to build and run an evaluation setup, and the corpus is dominated by practitioner walkthroughs plus benchmark papers that repeatedly converge on the same sequence — define success, build cases, grade, repeat runs, trace, analyse failures, bound budgets, gate releases ([S-24], [S-26], [S-29]). A staged guide lets each stage carry the evidence it actually has: research-grade numbers where they exist ([S-08], [S-09], [S-28]) and clearly labelled vendor or single-team examples where they do not ([S-01], [S-22], [S-25]). It also gives bounded retries and cost budgets a natural home as explicit stop conditions rather than an aside.

## What you are actually evaluating

Set the unit under test as a system (model, prompt, tools, retrieval, orchestration) rather than a model, and warn that public benchmark scores do not transfer to a reader's stack.

Evaluation targets a system — model plus prompt, tools, retrieval, memory, and orchestration — because the same base model scores very differently under different agent scaffolds and tool descriptions. [S-09] [S-30] [S-25] [S-09]

Public benchmarks and leaderboards are treated as orientation only: their scores do not transfer to a specific stack, and contamination, weak test suites, and idealised tasks inflate published results. [S-06] [S-24] [S-04] [S-09]

## Step 1 — Write success down as an evidence contract

Turn "the agent worked" into a checkable specification covering observable outcomes, allowed and prohibited actions, constraints, and failure behaviour.

The practical starting point is to define success before choosing evaluators: the observable result, the evidence that proves it (often system state rather than the agent's message), permitted and prohibited actions, constraints, and how the agent should behave when the task cannot be completed. [S-29] [S-24] [S-23]

- Qualification: Success definitions are use-case specific; the corpus offers no shared rubric beyond the goal-success and goal-accuracy pair attributed to AWS in S-24.

Across research and practitioner sources, tool-using agents are evaluated on the execution path as well as the final answer, because a correct or polished response can hide wrong tool selection, skipped prerequisites, and broken reasoning. [S-05] [S-24] [S-06] [S-23] [S-04]

- Qualification: No source in the corpus measures how much trajectory scoring improves outcomes compared with output-only scoring.

- Qualification: S-05 also notes that trajectory evaluation adds overhead and is not always worth it for single-turn or deterministic pipelines.

### Cover four scopes: outcome, trajectory, decisions, reliability

Give readers a spine for the specification so they do not stop at final-answer scoring, and connect the reliability scope to later repeated-run metrics.

Across research and practitioner sources, tool-using agents are evaluated on the execution path as well as the final answer, because a correct or polished response can hide wrong tool selection, skipped prerequisites, and broken reasoning. [S-05] [S-24] [S-06] [S-23] [S-04]

- Qualification: No source in the corpus measures how much trajectory scoring improves outcomes compared with output-only scoring.

- Qualification: S-05 also notes that trajectory evaluation adds overhead and is not always worth it for single-turn or deterministic pipelines.

Because agent behaviour is stochastic, sources recommend running each important case several times and reporting consistency metrics such as pass@1, pass@k, and pass^k instead of a single success or failure. [S-24] [S-29] [S-26] [S-04] [S-06]

- Qualification: Trial counts are only loosely specified ("several" in S-26); S-26 also notes that confidence intervals express sampling uncertainty and do not fix a biased dataset.

### Define tool- and state-level success criteria

Show how to express success as evidence from systems and traces — expected tool calls, arguments, and resulting state — rather than as message wording.

For agent datasets, ground truth is documented as including expected tool calls and intermediate steps, not only expected final answers. [S-05] [S-12] [S-26] [S-23]

- Qualification: S-23 concedes this annotation work is hard and slow; S-29 similarly warns against enforcing one exact sequence when several paths are valid.

Inefficient and repeated tool use is a measurable evaluated failure mode, captured through repeated-call error rates, retry and recovery metrics, tool-call failure rate, and path-convergence scores. [S-08] [S-29] [S-20] [S-23] [S-08]

- Qualification: S-29's convergence score is a described formula whose shortest observed run is only a proxy for efficiency; S-08's percentages come from one benchmark harness with human-annotated ground truth.

## Step 2 — Build the task dataset

Describe how to assemble a first suite that reflects real workloads instead of imagined ones, and how large it needs to be to start.

Practitioner sources converge on seeding the evaluation set from real user requests and confirmed production failures, starting small (roughly 5–50 cases) and adding ambiguous, adversarial, and failure-inducing cases rather than only happy paths. [S-24] [S-22] [S-26] [S-05] [S-29] [S-10]

- Qualification: The 5–50 case ranges are recommendations from a small-team roadmap (S-22) and a vendor-authored guide (S-24); no source reports how suite size relates to escaped defects.

- qualifies: I am looking for a benchmark dataset which would allow me to evaluate how well GPT matches uesr intent with those functions (as a baseline). [S-10]

For agent datasets, ground truth is documented as including expected tool calls and intermediate steps, not only expected final answers. [S-05] [S-12] [S-26] [S-23]

- Qualification: S-23 concedes this annotation work is hard and slow; S-29 similarly warns against enforcing one exact sequence when several paths are valid.

### Where cases come from

List the documented sources of cases: real user requests, confirmed production failures, ambiguous inputs, tool failures, permission boundaries, and injection attempts.

Practitioner sources converge on seeding the evaluation set from real user requests and confirmed production failures, starting small (roughly 5–50 cases) and adding ambiguous, adversarial, and failure-inducing cases rather than only happy paths. [S-24] [S-22] [S-26] [S-05] [S-29] [S-10]

- Qualification: The 5–50 case ranges are recommendations from a small-team roadmap (S-22) and a vendor-authored guide (S-24); no source reports how suite size relates to escaped defects.

- qualifies: I am looking for a benchmark dataset which would allow me to evaluate how well GPT matches uesr intent with those functions (as a baseline). [S-10]

The documented failure workflow is a loop: confirm a production failure, capture the trace, turn it into a regression case with agreed expected behaviour, run it against candidate changes, and keep it in the suite. [S-29] [S-05] [S-24] [S-05] [S-30]

- Qualification: The loop is described consistently across sources, but none quantifies its effect on escaped defects or regression frequency.

### When you have no dataset yet

Present synthetic generation honestly as a documented cold-start recipe from vendors, one published Amazon practice, and benchmark construction, with its verification burden stated.

When no dataset exists, sources describe generating one synthetically — LLM-generated tasks, expert or golden solutions, and human verification — and this is presented as benchmark-construction practice and single-team recipes rather than as validated guidance. [S-04] [S-30] [S-12]

- Qualification: The recipes come from a vendor podcast recap (S-04), a benchmark paper (S-12), and one published Amazon practice (S-30); none reports measured similarity between synthetic and production case distributions.

One corpus item is a concrete worked example rather than a technique: a single-agent, bounded 5-step document agent scoring 63.3% across 30 cases, with failures dominated by missing citations and missed escalation. [S-28] [S-28] [S-28]

- Qualification: This is one team's published example on a 30-case dataset with a fixed rubric and a 0.7 pass threshold; it demonstrates a report format and failure analysis, not a generalisable benchmark result.

Limitation: No source measures how closely synthetic cases match production distributions, so treat generated cases as a starting point that must be validated against real traffic.

## Step 3 — Choose graders from the least subjective method upward

Give readers a decision rule for grading: deterministic checks first, narrow judge rubrics next, human judgement at the boundary of uncertainty and consequence.

The recommended grading order is deterministic code checks first, narrowly scoped LLM judges only where language judgment is required, and human review where automated verdicts cannot be trusted. [S-26] [S-29] [S-24] [S-26]

- Qualification: S-24 warns that deterministic string matching must not stand in for semantic properties ("Contains refund" does not prove policy compliance).

LLM-as-a-judge is widely used for semantic checks, but every source that documents it also documents bias and instability and recommends rubric constraints, multiple judge passes, and calibration against human-labelled examples before judge scores drive decisions. [S-05] [S-24] [S-09] [S-04] [S-29]

- Qualification: No source reports a reliability figure for a calibrated judge on agent trajectories, so the mitigation list is advice rather than a measured result.

### Deterministic checks first

Show which agent properties code can judge — tool names and argument ranges, budget ceilings, approval ordering, expected sandbox state — and warn against string matching for semantic claims.

The recommended grading order is deterministic code checks first, narrowly scoped LLM judges only where language judgment is required, and human review where automated verdicts cannot be trusted. [S-26] [S-29] [S-24] [S-26]

- Qualification: S-24 warns that deterministic string matching must not stand in for semantic properties ("Contains refund" does not prove policy compliance).

Sources agree on explicit stop conditions for tool-using agents: caps on tool calls, retries per tool, tokens and cost, approval before state-changing writes, and escalation instead of unbounded retrying or looping. [S-22] [S-22] [S-26] [S-26] [S-29] [S-22] [S-25]

- Qualification: The numeric caps (8 tool calls, 2 retries per tool, specific SLO percentages) come from one small-team roadmap (S-22) and vendor playbooks (S-25, S-26); no source reports how those values were derived or how they generalise.

- Qualification: S-27 adds a separate bound that evaluation cannot enforce: infrastructure failures mid-run can force a full restart, so retry budgets interact with platform state durability.

### Narrow judge rubrics and their documented biases

Explain when a judge earns its cost, and enumerate the documented position, verbosity, and self-enhancement biases the rubric must defend against.

LLM-as-a-judge is widely used for semantic checks, but every source that documents it also documents bias and instability and recommends rubric constraints, multiple judge passes, and calibration against human-labelled examples before judge scores drive decisions. [S-05] [S-24] [S-09] [S-04] [S-29]

- Qualification: No source reports a reliability figure for a calibrated judge on agent trajectories, so the mitigation list is advice rather than a measured result.

### Calibrate before you trust, and review what you cannot calibrate

Describe judge calibration against human labels, adjudication of disagreements, and periodic transcript review, with sampling to control cost.

LLM-as-a-judge is widely used for semantic checks, but every source that documents it also documents bias and instability and recommends rubric constraints, multiple judge passes, and calibration against human-labelled examples before judge scores drive decisions. [S-05] [S-24] [S-09] [S-04] [S-29]

- Qualification: No source reports a reliability figure for a calibrated judge on agent trajectories, so the mitigation list is advice rather than a measured result.

Human review is positioned where uncertainty and consequence are highest — calibration labels, adjudication of disagreements, periodic audits, and any verdict that could permit a high-consequence action — with sampling used to contain evaluation cost. [S-29] [S-29] [S-24] [S-22] [S-06]

- Qualification: No source gives a review-volume or cost model for choosing sample sizes; the split between automated and human review remains a judgement call.

## Step 4 — Run cases more than once and report consistency

Make the case for repeated trials and consistency metrics, and show how pass@k and pass^k answer different questions about an agent that talks to users.

Because agent behaviour is stochastic, sources recommend running each important case several times and reporting consistency metrics such as pass@1, pass@k, and pass^k instead of a single success or failure. [S-24] [S-29] [S-26] [S-04] [S-06]

- Qualification: Trial counts are only loosely specified ("several" in S-26); S-26 also notes that confidence intervals express sampling uncertainty and do not fix a biased dataset.

Limitation: The corpus gives consistency metrics but no guidance on trial counts or how to trade trial volume against evaluation cost.

## Step 5 — Trace the run and keep the trace usable

Turn tracing into a concrete capture list and a storage decision, since every later evaluation step depends on what the trace preserved.

Documented trace requirements cover inputs and outputs, every tool call with arguments and results, retrieved context, intermediate reasoning, token counts and costs, and timing — and runs should be stored hierarchically because agents branch, backtrack, and delegate. [S-06] [S-06] [S-05] [S-18] [S-20]

- Qualification: S-15 and S-16 give a further reason to record state after every side effect: a successful HTTP response does not prove the intended external state change occurred.

OpenTelemetry's GenAI semantic conventions are the emerging vendor-neutral schema for agent telemetry — spans and attributes such as gen_ai.tool.name and gen_ai.usage.* — but sources describe the conventions as still experimental. [S-06] [S-16] [S-16] [S-20]

- Qualification: Vendor documentation (S-16, S-20) describes support for these conventions; no source reports an independent interoperability or overhead test.

- qualifies: [GenAI semantic conventions remain experimental](https://opentelemetry.io/blog/2025/ai-agent-observability/) but are rapidly stabilizing. [S-16]

### What every trace needs

Give a per-layer capture list (request, retrieval, reasoning, tool calls with arguments and results, state after side effects, tokens, cost, timing) and explain why hierarchical storage matters.

Documented trace requirements cover inputs and outputs, every tool call with arguments and results, retrieved context, intermediate reasoning, token counts and costs, and timing — and runs should be stored hierarchically because agents branch, backtrack, and delegate. [S-06] [S-06] [S-05] [S-18] [S-20]

- Qualification: S-15 and S-16 give a further reason to record state after every side effect: a successful HTTP response does not prove the intended external state change occurred.

### Standardising on OpenTelemetry GenAI conventions

Explain the emerging convention names for tool and usage attributes, and flag that the conventions are still experimental so instrumentation should not be the only source of truth.

OpenTelemetry's GenAI semantic conventions are the emerging vendor-neutral schema for agent telemetry — spans and attributes such as gen_ai.tool.name and gen_ai.usage.* — but sources describe the conventions as still experimental. [S-06] [S-16] [S-16] [S-20]

- Qualification: Vendor documentation (S-16, S-20) describes support for these conventions; no source reports an independent interoperability or overhead test.

- qualifies: [GenAI semantic conventions remain experimental](https://opentelemetry.io/blog/2025/ai-agent-observability/) but are rapidly stabilizing. [S-16]

## Step 6 — Sort failures into categories and feed them back

Move readers from a pass rate to a diagnosed failure distribution, then into the loop that turns each confirmed failure into a permanent regression case.

Sources supply concrete failure categories to sort results into: wrong tool or missing information, redundant calls, refusal and escalation errors, missing citations or grounding, parameter errors, and poor uncertainty calibration. [S-28] [S-08] [S-28] [S-12] [S-14]

- Qualification: S-08's error percentages and S-28's category counts each come from a single harness or team; the taxonomies overlap but are not standardised.

- Qualification: S-14's framing is from a vendor blog post about its own observability product.

The documented failure workflow is a loop: confirm a production failure, capture the trace, turn it into a regression case with agreed expected behaviour, run it against candidate changes, and keep it in the suite. [S-29] [S-05] [S-24] [S-05] [S-30]

- Qualification: The loop is described consistently across sources, but none quantifies its effect on escaped defects or regression frequency.

### Categories that show up in practice

Give readers a starting taxonomy — wrong tool or missing information, redundant calls, refusal and escalation errors, missing citations, parameter errors, poor uncertainty calibration — drawn from benchmark and worked-example evidence.

Sources supply concrete failure categories to sort results into: wrong tool or missing information, redundant calls, refusal and escalation errors, missing citations or grounding, parameter errors, and poor uncertainty calibration. [S-28] [S-08] [S-28] [S-12] [S-14]

- Qualification: S-08's error percentages and S-28's category counts each come from a single harness or team; the taxonomies overlap but are not standardised.

- Qualification: S-14's framing is from a vendor blog post about its own observability product.

One corpus item is a concrete worked example rather than a technique: a single-agent, bounded 5-step document agent scoring 63.3% across 30 cases, with failures dominated by missing citations and missed escalation. [S-28] [S-28] [S-28]

- Qualification: This is one team's published example on a 30-case dataset with a fixed rubric and a 0.7 pass threshold; it demonstrates a report format and failure analysis, not a generalisable benchmark result.

### From trace to regression case

Describe the loop step by step: confirm the failure, keep the smallest reproducing state, record expected behaviour, and run it against every candidate change.

The documented failure workflow is a loop: confirm a production failure, capture the trace, turn it into a regression case with agreed expected behaviour, run it against candidate changes, and keep it in the suite. [S-29] [S-05] [S-24] [S-05] [S-30]

- Qualification: The loop is described consistently across sources, but none quantifies its effect on escaped defects or regression frequency.

Practitioner sources converge on seeding the evaluation set from real user requests and confirmed production failures, starting small (roughly 5–50 cases) and adding ambiguous, adversarial, and failure-inducing cases rather than only happy paths. [S-24] [S-22] [S-26] [S-05] [S-29] [S-10]

- Qualification: The 5–50 case ranges are recommendations from a small-team roadmap (S-22) and a vendor-authored guide (S-24); no source reports how suite size relates to escaped defects.

- qualifies: I am looking for a benchmark dataset which would allow me to evaluate how well GPT matches uesr intent with those functions (as a baseline). [S-10]

## Step 7 — Bound retries, tool calls, and spend, and wire them to autonomy

Give every stop condition a home: service-level indicators, retry and loop caps, approval gates, and cost or latency ceilings treated as correctness criteria.

Sources agree on explicit stop conditions for tool-using agents: caps on tool calls, retries per tool, tokens and cost, approval before state-changing writes, and escalation instead of unbounded retrying or looping. [S-22] [S-22] [S-26] [S-26] [S-29] [S-22] [S-25]

- Qualification: The numeric caps (8 tool calls, 2 retries per tool, specific SLO percentages) come from one small-team roadmap (S-22) and vendor playbooks (S-25, S-26); no source reports how those values were derived or how they generalise.

- Qualification: S-27 adds a separate bound that evaluation cannot enforce: infrastructure failures mid-run can force a full restart, so retry budgets interact with platform state durability.

Uptime, latency, and error rate are documented as insufficient for agents; sources propose agent-specific indicators such as task success rate, tool-call accuracy, hallucination rate, cost per task, and end-to-end latency measured per completed task. [S-25] [S-18] [S-25] [S-16] [S-18]

- Qualification: The supporting texts are vendor and vendor-adjacent blogs; the Datadog figure in S-25 is cited secondhand without sample detail.

Cost and latency are presented as parts of correctness rather than pure operations metrics — cost is measured per successful task and latency at the tail of the whole run, including tool calls. [S-25] [S-23] [S-06] [S-09]

- Qualification: The specific dollar and latency budgets in S-22 and S-25 are example values from single teams rather than derived targets.

### Pick agent-level indicators, then set thresholds from impact

Replace availability and error rate with task success, tool-call accuracy, hallucination rate, cost per task, and tail latency, and show how published thresholds are starting points only.

Uptime, latency, and error rate are documented as insufficient for agents; sources propose agent-specific indicators such as task success rate, tool-call accuracy, hallucination rate, cost per task, and end-to-end latency measured per completed task. [S-25] [S-18] [S-25] [S-16] [S-18]

- Qualification: The supporting texts are vendor and vendor-adjacent blogs; the Datadog figure in S-25 is cited secondhand without sample detail.

Published gate and SLO numbers exist, but they come from single teams or vendors — for example a 95% tool-selection gate attributed to an AWS blueprint and a vendor guidance to set first SLOs slightly above the observed baseline. [S-24] [S-25] [S-25]

- Qualification: These figures are not field consensus: S-24 and S-25 are vendor-authored guides, so the numbers are illustrative starting points that must be re-derived for each deployment.

- Qualification: S-25 also notes that different agent types need different targets, which undercuts any single published threshold.

### Stop conditions, retry caps, and approval gates

Specify the bounds and explain the escalation path when a bound is hit, including approval before state-changing writes and autonomy reduction when quality drops.

Sources agree on explicit stop conditions for tool-using agents: caps on tool calls, retries per tool, tokens and cost, approval before state-changing writes, and escalation instead of unbounded retrying or looping. [S-22] [S-22] [S-26] [S-26] [S-29] [S-22] [S-25]

- Qualification: The numeric caps (8 tool calls, 2 retries per tool, specific SLO percentages) come from one small-team roadmap (S-22) and vendor playbooks (S-25, S-26); no source reports how those values were derived or how they generalise.

- Qualification: S-27 adds a separate bound that evaluation cannot enforce: infrastructure failures mid-run can force a full restart, so retry budgets interact with platform state durability.

### Measuring loops, waste, and cost

Show how to detect redundant calls, retry storms, and long tails with path-convergence, retry and recovery rates, tool-call failure rate, and cost per successful task.

Inefficient and repeated tool use is a measurable evaluated failure mode, captured through repeated-call error rates, retry and recovery metrics, tool-call failure rate, and path-convergence scores. [S-08] [S-29] [S-20] [S-23] [S-08]

- Qualification: S-29's convergence score is a described formula whose shortest observed run is only a proxy for efficiency; S-08's percentages come from one benchmark harness with human-annotated ground truth.

Cost and latency are presented as parts of correctness rather than pure operations metrics — cost is measured per successful task and latency at the tail of the whole run, including tool calls. [S-25] [S-23] [S-06] [S-09]

- Qualification: The specific dollar and latency budgets in S-22 and S-25 are example values from single teams rather than derived targets.

## Step 8 — Make the suite a release gate

Turn the suite into a deploy decision: what triggers a full run, what conditions block a release, and why gates must be declared before results are seen.

Sources position the suite as a CI release gate that runs on every change capable of altering behaviour — prompt edits, model swaps, tool changes, retrieval changes — and blocks deploys on failed safety or quality conditions. [S-24] [S-26] [S-22] [S-24] [S-26] [S-26]

- Qualification: All gate designs in the corpus are practitioner proposals; none reports measured reduction in production regressions after adoption.

Published gate and SLO numbers exist, but they come from single teams or vendors — for example a 95% tool-selection gate attributed to an AWS blueprint and a vendor guidance to set first SLOs slightly above the observed baseline. [S-24] [S-25] [S-25]

- Qualification: These figures are not field consensus: S-24 and S-25 are vendor-authored guides, so the numbers are illustrative starting points that must be re-derived for each deployment.

- Qualification: S-25 also notes that different agent types need different targets, which undercuts any single published threshold.

### What triggers a full run

List the changes that alter behaviour even when application code does not: prompt edits, model swaps, tool schema changes, retrieval or knowledge-base updates, and connected API changes.

Sources position the suite as a CI release gate that runs on every change capable of altering behaviour — prompt edits, model swaps, tool changes, retrieval changes — and blocks deploys on failed safety or quality conditions. [S-24] [S-26] [S-22] [S-24] [S-26] [S-26]

- Qualification: All gate designs in the corpus are practitioner proposals; none reports measured reduction in production regressions after adoption.

### Writing the gate policy and choosing thresholds

Give a defensible policy structure — hard safety failures block, tagged regressions block, operational budgets block — plus the rule that thresholds come from observed variance, not ambition.

Sources position the suite as a CI release gate that runs on every change capable of altering behaviour — prompt edits, model swaps, tool changes, retrieval changes — and blocks deploys on failed safety or quality conditions. [S-24] [S-26] [S-22] [S-24] [S-26] [S-26]

- Qualification: All gate designs in the corpus are practitioner proposals; none reports measured reduction in production regressions after adoption.

Because agent behaviour is stochastic, sources recommend running each important case several times and reporting consistency metrics such as pass@1, pass@k, and pass^k instead of a single success or failure. [S-24] [S-29] [S-26] [S-04] [S-06]

- Qualification: Trial counts are only loosely specified ("several" in S-26); S-26 also notes that confidence intervals express sampling uncertainty and do not fix a biased dataset.

Published gate and SLO numbers exist, but they come from single teams or vendors — for example a 95% tool-selection gate attributed to an AWS blueprint and a vendor guidance to set first SLOs slightly above the observed baseline. [S-24] [S-25] [S-25]

- Qualification: These figures are not field consensus: S-24 and S-25 are vendor-authored guides, so the numbers are illustrative starting points that must be re-derived for each deployment.

- Qualification: S-25 also notes that different agent types need different targets, which undercuts any single published threshold.

## Multi-agent and long-horizon cases

Explain why per-agent scoring breaks down in multi-agent systems, what to measure instead, and why the same reasoning extends to long-running tasks where context decays.

For multi-agent systems, per-agent scores mislead; sources recommend end-to-end evaluation plus explicit handoff, communication, and coordination measurements. [S-04] [S-30] [S-01] [S-17]

- Qualification: The multi-agent metrics named in S-30 (planning score, communication score, collaboration success rate) are described without published baselines or thresholds.

Evaluation targets a system — model plus prompt, tools, retrieval, memory, and orchestration — because the same base model scores very differently under different agent scaffolds and tool descriptions. [S-09] [S-30] [S-25] [S-09]

Limitation: Multi-agent metrics in the corpus come from vendor and vendor-adjacent posts without published baselines.

## What public benchmarks can and cannot tell you

Help readers read leaderboards correctly: use them to locate capability gaps and known failure modes, not to predict their own agent's production reliability.

Public benchmarks and leaderboards are treated as orientation only: their scores do not transfer to a specific stack, and contamination, weak test suites, and idealised tasks inflate published results. [S-06] [S-24] [S-04] [S-09]

Benchmark evidence documents where tool use breaks down: session-level accuracy below 15% on in-the-wild multi-turn tool use, task accuracy collapsing from strong function-calling scores to 7.2% on a multi-step agentic benchmark, and frontier agents failing about one in five realistic terminal tasks. [S-08] [S-09] [S-06] [S-13] [S-07]

- Qualification: All figures are point-in-time results tied to specific model versions and harnesses; none measures a reader's own deployment.

- Qualification: S-10 shows that practitioners looking for a ready-made tool-selection benchmark dataset historically found the landscape hard to navigate.

## Limits of this evidence base

State plainly which parts of the guide rest on research or measured practice and which rest on vendor documentation, single-team examples, or unanswered community questions — so readers know where to validate locally.

Several corpus sources are vendor or vendor-sponsored documents, so their platform capability, reliability, and interview-derived statistics are marketing claims rather than independently measured results. [S-01] [S-16] [S-27] [S-15]

- Qualification: Where a claim carries no method, sample, or reproduction detail (for example the 3–15% tool-failure rate in S-15), treat it as an unverified figure rather than a finding.

- qualifies: Tool calls fail between 3 and 15% [S-15]

One corpus item is a concrete worked example rather than a technique: a single-agent, bounded 5-step document agent scoring 63.3% across 30 cases, with failures dominated by missing citations and missed escalation. [S-28] [S-28] [S-28]

- Qualification: This is one team's published example on a 30-case dataset with a fixed rubric and a 0.7 pass threshold; it demonstrates a report format and failure analysis, not a generalisable benchmark result.

Limitation: No controlled comparisons of the recommended evaluation designs exist in the corpus, and numeric caps and thresholds are illustrative rather than derived.

Gap: No source reports a controlled comparison of evaluation designs — trajectory versus output scoring, deterministic versus judge grading — on the same agent.

Gap: Retry, tool-call, and budget caps are recommended constants without any derivation or reported effect on task success or customer outcomes.

Gap: No shared public task set for tool selection appears in the corpus: the only community request found (S-10) is unanswered, and S-09 documents the benchmark landscape as fragmented.

Gap: Observability and trace-completeness comparisons are vendor-authored; no independent measurement of telemetry overhead, sampling loss, or cross-framework interoperability is present.

Gap: Multi-agent evaluation metrics (handoff, communication, collaboration) are described without published baselines or reference datasets.

Gap: Human-review effort and sampling economics are asserted rather than modelled: no source gives a cost or coverage calculation for review queues.

Corpus limitation: About half the corpus is vendor or vendor-sponsored content (S-01, S-06, S-14, S-16, S-17, S-20, S-24, S-25, S-27, S-29); it is cited for described practice and for its own numbers, not as independent verification.

Corpus limitation: S-10 is an unanswered community forum thread and S-15 is a secondary editorial summarising another vendor's guide; neither is used as primary evidence for a technique.

Corpus limitation: Numeric results are point-in-time and tied to specific model versions and harnesses (BFCL September 2024 data in S-09, terminal-bench 2.0 in S-06, 2024–2026 paper and leaderboard snapshots), so they indicate difficulty rather than current rankings.

Corpus limitation: No source in the corpus reports an experiment isolating the effect of trajectory scoring, bounded retries, or CI gating on production outcomes.

Corpus limitation: Two research papers assume conditions (a bounded 5-step agent budget in S-28, preregistration in S-07) that readers may not be able to replicate.

This plan takes the shape of a staged implementation guide because the corpus is dominated by practitioner walkthroughs and benchmark documentation that converge on the same sequence — define success, build cases, grade, repeat runs, trace, analyse failures, bound budgets, gate releases — across independent authors [S-24] [S-26] [S-29] [S-22], and because the reader's goal is to build and run an evaluation setup rather than to survey a field. The strongest and most consistent evidence concerns what to capture and measure: process evaluation over final answers [S-05] [S-24], ground truth that includes expected tool calls [S-05] [S-12], hierarchical traces with tool arguments and costs [S-06] [S-18], agent-level indicators instead of uptime and error rate [S-25] [S-18], explicit stop conditions and retry caps [S-22] [S-26], and CI gates that run on prompt, model, tool, and retrieval changes [S-24] [S-26]. The guide therefore spends most of its structure on those stages. The weaker evidence is handled by labelling rather than by strengthening: numeric caps and thresholds such as 8 tool calls, 2 retries per tool, a 95% tool-selection gate, and first SLOs 10-15% above baseline come from one small-team roadmap and vendor-authored playbooks [S-22] [S-24] [S-25], the observability and management-platform descriptions are vendor documents [S-01] [S-16] [S-20] [S-27], the multi-agent metrics come from vendor and vendor-adjacent posts [S-30] [S-17], the 3–15% tool-failure figure is quoted third-hand [S-15], and the 63.3% pass rate comes from a single published 30-case example [S-28]. Those items appear as examples with their provenance stated, never as findings. The quantitative claims that are strongest are point-in-time measurements from publicly documented harnesses — session accuracy below 15% on in-the-wild multi-turn tool use [S-08], a drop from 83.59% on function calling to 7.2% on a multi-step agentic benchmark [S-09], and one in five realistic terminal tasks failing even for top agents [S-06] — and they are used to justify the practices, not to predict any reader's results. Two formats fit less well and are noted in the plan: an annotated literature review would showcase the research sources but leave the implementation goal unserved and imply consensus that the vendor-heavy half of the corpus does not support, and a hands-on tutorial would claim reproducibility the sources never demonstrate, since the corpus contains snippets and recipes rather than a validated harness. The closing bias is toward honest scope: the final section keeps the vendor claims, the single-team exemplar, and the empty spaces — no controlled comparison of evaluation designs, no published baseline for multi-agent metrics, no answer to the community request for an off-the-shelf tool-selection dataset [S-10] — visible instead of rounding them up into confident advice.
