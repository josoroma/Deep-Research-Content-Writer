# Research synthesis: AI agent evaluation

Create a practical implementation guide for evaluating tool-using AI agents, covering task datasets, success criteria, failure analysis, observability, and bounded retries, while distinguishing documented techniques from untested examples.

Format: Evidence-graded implementation guide (practitioner playbook with documented-vs-untested labeling). The goal asks for a practical implementation guide covering datasets, success criteria, failure analysis, observability, and bounded retries. The corpus supplies concrete procedural material for each of those areas (Arize's six-step loop in S-30, Google Cloud's five-step ADK loop and synthetic-data recipe in S-04, LangChain's trajectory-evaluation and dataset workflow in S-05, and OpenTelemetry instrumentation in S-23/S-29), while the benchmark papers (S-08, S-09, S-12, S-13) supply measured limits on how well agents actually perform. A guide format lets the plan sequence those procedures in the order a team would implement them and attach an explicit documented-versus-untested label to each step, which is exactly the distinction the goal requests.

## Why tool-using agents break output-only evaluation

Establish the reader's mental model: agents are non-deterministic and their correct answers can hide broken reasoning, so evaluation must cover the run, not just the response.

Agent evaluation must score the execution path, not only the final answer, because a correct or fluent output can hide broken reasoning, unsafe actions, or an inefficient run. [S-05] [S-30] [S-06]

- Qualification: All three sources are vendor engineering blogs, so this is documented practitioner consensus rather than an independently measured result.

Because agent behavior is non-deterministic, evaluation must be repeated and statistical rather than a single deterministic pass/fail check. [S-04] [S-16] [S-30] [S-06]

- Qualification: The pass@k / pass^k framing is attributed to Anthropic's guide by S-30; the corpus does not include that primary source.

## Define success criteria and a metric contract before you build

Give the reader a starting discipline: pick the production decision first, then define outcome, action, constraint and failure-handling criteria and record what each metric cannot prove.

Success criteria should be defined before building, tied to a specific production decision, and recorded as a metric contract that states what each number cannot prove. [S-17] [S-30] [S-17] [S-17]

- Qualification: The metric-contract format is one practitioner's proposal (S-17); no source tests whether it improves outcomes.

- qualifies: The right threshold depends on the workflow, impact and review model. A suggested number in a workshop is a hypothesis, not evidence. [S-17]

Metrics should be layered across technical operation, task completion, and value/risk, and aggregate scores can hide regressions in specific tools or high-risk tasks. [S-17] [S-06] [S-30]

- Qualification: The two layering schemes (S-17 and S-06) are similar but not identical; neither is validated against outcomes.

## Build a task dataset that reflects production

Show how to assemble the evaluation set, including ground truth for tool calls and reasoning steps, and how to seed it from real traffic.

Task datasets for agents need ground truth that includes expected tool calls and reasoning steps, organized into happy-path, edge-case, and adversarial categories and seeded from real production requests. [S-05] [S-05] [S-30]

- Qualification: The three-category split and the production-seeded approach are practitioner conventions; no source measures how much coverage they achieve.

Evaluation cost is a first-order constraint, so teams sample traffic and reserve expensive methods for high-value or high-risk cases. [S-06] [S-05] [S-05]

- Qualification: No source quantifies the cost of specific evaluation configurations beyond noting that some exceed the baseline agent workload.

- qualifies: Trajectory evaluation adds real overhead [S-05]

### Cold start: generating synthetic tasks and ground truth

Present the documented synthetic-data recipe for teams with no dataset, and flag that it is a single vendor demo rather than a validated method.

When no dataset exists, a documented cold-start recipe generates synthetic tasks, expert solutions, imperfect attempts, and automatic scoring. [S-04] [S-04]

- Qualification: This recipe is presented in a single vendor demo (Google Cloud ADK/Vertex AI) and is not independently validated in the corpus.

## Choose evaluators: deterministic checks, LLM judges, and human review

Lay out the evaluator-selection rule (use the least subjective method that can decide the case) and the three review patterns.

Outcome evaluation should inspect the resulting system state rather than trusting the agent's own confirmation message. [S-30] [S-30]

- Qualification: Illustrated with a worked refund scenario rather than measured across deployments.

Tool selection and parameter extraction should be evaluated separately from downstream response quality, because routing failures otherwise masquerade as quality failures. [S-30] [S-18] [S-18]

- Qualification: S-18 is product documentation for a metrics library, so the metric list reflects that vendor's design choices.

LLM-as-a-judge is the practical default for trajectory scoring, but judges are biased and inconsistent, so they require structured rubrics, multiple passes, and calibration against human labels. [S-05] [S-09] [S-04]

- Qualification: The bias taxonomy in S-09 is a literature synthesis; the corpus does not include the underlying bias studies.

Human review should be reserved for boundaries of uncertainty and consequence, typically through sampled review queues rather than exhaustive scoring. [S-30] [S-22]

- Qualification: The 1-5% sampling figure is one team's starting heuristic, not a validated threshold.

### Score outcomes against system state, not the agent's message

Explain why the confirmation message is not evidence and how to check persisted state and partial completion.

Outcome evaluation should inspect the resulting system state rather than trusting the agent's own confirmation message. [S-30] [S-30]

- Qualification: Illustrated with a worked refund scenario rather than measured across deployments.

### Evaluate routing and tool arguments separately

Give the reader the two router axes (tool selection and parameter extraction) and the dataset cases that expose routing errors.

Tool selection and parameter extraction should be evaluated separately from downstream response quality, because routing failures otherwise masquerade as quality failures. [S-30] [S-18] [S-18]

- Qualification: S-18 is product documentation for a metrics library, so the metric list reflects that vendor's design choices.

### Calibrate LLM judges and place human review at the boundary

Cover judge bias, rubric design, multiple passes, and where human review is mandatory.

LLM-as-a-judge is the practical default for trajectory scoring, but judges are biased and inconsistent, so they require structured rubrics, multiple passes, and calibration against human labels. [S-05] [S-09] [S-04]

- Qualification: The bias taxonomy in S-09 is a literature synthesis; the corpus does not include the underlying bias studies.

Human review should be reserved for boundaries of uncertainty and consequence, typically through sampled review queues rather than exhaustive scoring. [S-30] [S-22]

- Qualification: The 1-5% sampling figure is one team's starting heuristic, not a validated threshold.

## Instrument observability: complete traces and OpenTelemetry conventions

Specify the minimum trace contents, the hierarchical structure requirement, and the versioning caveat for GenAI semantic conventions.

Observability requires complete per-run traces that preserve hierarchical structure across tool calls, retrieval, prompt versions, cost and latency, because flat logs and uptime metrics cannot explain agent failures. [S-22] [S-06] [S-05] [S-22]

- Qualification: Trace-element checklists differ slightly across S-06, S-22 and S-23; no source reconciles them into one schema.

OpenTelemetry GenAI semantic conventions are the emerging standard for agent tracing, but they remain in Development status, so emitted versions and field mappings must be pinned as versioned infrastructure. [S-23] [S-06] [S-29] [S-23]

- Qualification: S-23 is a practitioner blog reporting on the OpenTelemetry project; the corpus does not include the specification itself.

## Analyze failures with taxonomies and diagnostic probes

Show how to classify failures consistently and how probe tools can isolate tool-selection weaknesses that capability rankings miss.

Failure analysis benefits from a predefined failure taxonomy, and benchmark error analysis shows wrong-tool and redundant-call errors dominate over parameter-level errors. [S-25] [S-22] [S-08]

- Qualification: The WildToolBench error distribution is specific to its 1,024-task dataset and may not transfer to other domains.

Diagnostic probe tools (canaries) can surface tool-selection weaknesses, and a model's capability tier does not predict its safety under such probes. [S-15] [S-15]

- Qualification: This is secondhand reporting of a preprint (arXiv 2608.04719) by a practitioner news site; the paper itself is not in the corpus and the result is not peer-reviewed here.

## Bound retries, loops, and evaluation cost

Turn retry limits, escalation, iteration counts and cost-per-success into explicit evaluation targets, and explain sampling to control evaluation spend.

Bounded retries and loop control should be explicit evaluation targets: retry limits, required escalations, iteration counts, and cost per successful outcome. [S-30] [S-23] [S-22]

- Qualification: No source specifies concrete retry limits or backoff parameters; the guidance is to make limits explicit and measurable, not what the limits should be.

Evaluation cost is a first-order constraint, so teams sample traffic and reserve expensive methods for high-value or high-risk cases. [S-06] [S-05] [S-05]

- Qualification: No source quantifies the cost of specific evaluation configurations beyond noting that some exceed the baseline agent workload.

- qualifies: Trajectory evaluation adds real overhead [S-05]

## Close the loop: from production failures to regression tests

Describe the trace-to-regression pipeline and the curation rules that keep the regression suite useful.

Production failures should be converted into regression tests, closing a loop from monitoring through human review back into the evaluation dataset. [S-05] [S-30] [S-06] [S-30]

- Qualification: The loop is described consistently across vendors but no source measures its effect on defect rates.

- qualifies: Do not copy every failed [trace](https://arize.com/glossary/trace/) into the dataset. [S-30]

## Evaluate multi-agent and end-to-end behavior

Explain why per-agent scores mislead in handoff systems and what end-to-end evaluation must cover.

In multi-agent systems, per-agent scores mislead; evaluation must be end-to-end because failures propagate across handoffs and shared state. [S-04] [S-01] [S-06]

- Qualification: The multi-agent guidance is illustrated with hypothetical scenarios; S-13's REALM-Bench is the only multi-agent benchmark in the corpus and reports no comparative results in the fetched text.

## Use benchmarks as one signal, not a guarantee

Help the reader interpret leaderboards: what benchmark results show about current agent limits, and why they do not transfer to production.

Benchmarks are useful for capability assessment but do not guarantee production success, and contamination plus idealized scenarios limit how much their scores mean. [S-06] [S-04] [S-09]

- Qualification: The BFCL/MCP-Atlas contrast is drawn from leaderboard snapshots cited by S-09, not from a controlled study in the corpus.

Benchmark evidence shows tool-using agents still fail a large share of realistic tasks, with session-level success far below task-level success. [S-08] [S-06] [S-21]

- Qualification: These figures come from different benchmarks with different task distributions and cannot be compared directly; S-21 is secondhand news reporting.

Benchmark design involves explicit trade-offs between realism and reproducibility, and a reliability paradox in which more realistic benchmarks require less reliable LLM-judge scoring. [S-09] [S-09] [S-12] [S-13]

- Qualification: S-12 and S-13 are benchmark design documents; they describe intended evaluation dimensions rather than reporting comparative outcomes.

## Governance and trust metrics for production agents

Extend the metric set beyond accuracy to tool-use safety, injection resilience, escalation, and telemetry classification.

Trustworthiness and governance metrics extend beyond accuracy to tool-use safety, prompt-injection resilience, escalation rates, and classification of telemetry as sensitive data. [S-14] [S-14] [S-26] [S-26]

- Qualification: S-14 and S-26 are security-governance publications that reference NIST, OWASP and MITRE frameworks; the corpus does not include those primary standards.

## Documented techniques vs. untested examples: reading this guide critically

Give the reader an explicit evidence key so they can tell vendor-documented practice from benchmark-measured results and from single-source demos.

When no dataset exists, a documented cold-start recipe generates synthetic tasks, expert solutions, imperfect attempts, and automatic scoring. [S-04] [S-04]

- Qualification: This recipe is presented in a single vendor demo (Google Cloud ADK/Vertex AI) and is not independently validated in the corpus.

Diagnostic probe tools (canaries) can surface tool-selection weaknesses, and a model's capability tier does not predict its safety under such probes. [S-15] [S-15]

- Qualification: This is secondhand reporting of a preprint (arXiv 2608.04719) by a practitioner news site; the paper itself is not in the corpus and the result is not peer-reviewed here.

The evaluation ecosystem remains fragmented: practitioners still ask for basic tool-selection benchmarks, and observability tooling is stitched together from many overlapping platforms. [S-10] [S-28] [S-25]

- Qualification: S-10 is a single forum post from 2024 and may not represent the current state of available benchmarks.

Limitation: Most procedural guidance in this corpus is vendor-documented and product-adjacent; only S-08, S-09, S-12 and S-13 report measured results, and no source provides an independent, controlled comparison of the recommended practices.

Gap: No source reports a controlled experiment comparing evaluation strategies (for example, trajectory scoring versus output-only scoring) on the same agent and task set.

Gap: Concrete retry limits, backoff parameters, and loop-termination thresholds are not specified anywhere in the corpus; only the need to make them explicit and measurable is documented.

Gap: Cost figures for evaluation are asserted qualitatively (S-06) but no source provides measured cost-per-evaluation or sampling-budget guidance beyond a 1-5% human-review heuristic (S-22).

Gap: The corpus contains no primary OpenTelemetry specification, no primary Anthropic evaluation guide, and no primary canary-tool paper; those are referenced secondhand.

Gap: Multi-agent evaluation is discussed conceptually (S-01, S-04, S-13) but no source reports measured end-to-end multi-agent results.

Gap: There is no evidence on how to set release thresholds or guardrail values; S-17 explicitly says a proposed number is a hypothesis, not evidence.

Corpus limitation: Most procedural guidance in this corpus comes from vendor engineering blogs that also market an evaluation or observability product (S-01, S-04, S-05, S-06, S-18, S-22, S-23, S-26, S-28, S-29, S-30); their recommended workflows are documented practice, not independently validated results.

Corpus limitation: Only S-08, S-09, S-12 and S-13 report measured benchmark results; the remaining sources assert failure rates, cost figures and incident statistics without exposing methodology in the fetched text.

Corpus limitation: Several headline statistics are secondhand: S-16 attributes an 84% production-failure figure to Gartner/MIT/Stanford without a primary citation, and S-15 reports a canary-tool preprint through a practitioner news site rather than the paper itself.

Corpus limitation: No source in the corpus reports a controlled, head-to-head comparison of the evaluation practices it recommends, so relative effectiveness of the techniques cannot be established from this evidence.

Corpus limitation: Version and timeframe assumptions differ: S-23 documents OpenTelemetry GenAI conventions moving repositories in mid-2026, while S-09 cites 2024 leaderboard numbers, so tool and benchmark details are time-sensitive.

This corpus supports an implementation guide better than a literature review or a platform comparison because it contains step-by-step procedures for exactly the areas the goal names: dataset construction and ground-truth annotation [S-05], a synthetic cold-start recipe [S-04], outcome-versus-trajectory scoring and evaluator selection [S-30], trace instrumentation with OpenTelemetry [S-23][S-29], failure taxonomies [S-22][S-25], and retry/loop and cost controls [S-12][S-22]. The benchmark papers supply the counterweight the goal also asks for: measured evidence that agents still fail large shares of realistic tasks, with session accuracy below 15% on WildToolBench [S-08] and top agents succeeding on only 81.8% of terminal tasks [S-06], plus the warning that benchmark scores do not transfer to production [S-09]. Because most procedural sources are vendor engineering blogs that also sell evaluation or observability products [S-01][S-06][S-22][S-30], the outline ends with an explicit documented-versus-untested section and the plan records limitations and gaps rather than presenting vendor practice as validated method. The two proposed diagrams are limited to relationships the sources actually describe: the evaluation loop [S-30][S-05] and the span structure of a traced run [S-23][S-29].
