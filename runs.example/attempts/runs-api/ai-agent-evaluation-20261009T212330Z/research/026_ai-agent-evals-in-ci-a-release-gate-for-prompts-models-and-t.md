---
source_id: S-26
url: https://stanleycyang.com/writing/ai-agent-evals-ci
title: 'AI Agent Evals in CI: A Release Gate for Prompts, Models, and Tools'
author: Stanley Yang
published: '2026-07-18T00:00:00.000Z'
fetched: '2026-10-09T21:23:55Z'
word_count: 1323
---
# AI Agent Evals in CI: A Release Gate for Prompts, Models, and Tools

An agent evaluation suite should answer a release question: did this change make the system meaningfully worse on tasks and risks we care about?

It is not one model grading another model’s prose. Reliable evals combine deterministic assertions, trajectory inspection, task-specific grading, repeated trials, and human review. They version the model, prompt, tools, data, and evaluator so a score can be reproduced and explained.

This guide builds a provider-neutral structure you can run in CI and extend with your own agent runtime.

## Define the unit under test

Evaluate the complete path that can change user outcomes:

```
user input
  → prompt and model
  → retrieval and memory
  → tool selection and arguments
  → tool results
  → final answer or side effect
```
A prompt-only test misses a changed tool schema. A final-answer grader misses an unauthorized tool call that happened to produce polished prose. Record the trajectory as well as the result.

Start with one stable `runAgent` contract:

```
interface ToolCall {
  readonly arguments: unknown;
  readonly name: string;
  readonly outcome: "error" | "success";
}
interface AgentRun {
  readonly answer: string;
  readonly durationMs: number;
  readonly inputTokens?: number;
  readonly outputTokens?: number;
  readonly toolCalls: readonly ToolCall[];
}
interface AgentConfig {
  readonly model: string;
  readonly promptVersion: string;
  readonly toolSchemaVersion: string;
}
declare function runAgent(
  input: string,
  config: AgentConfig,
): Promise<AgentRun>;
```
The trace should contain normalized events, not secret chain-of-thought. Capture observable inputs, tool decisions, results, latency, token usage, and errors.

## Build the dataset from real work

Each case needs a stable ID, input, tags, and explicit checks:

```
interface EvalCase {
  readonly checks: readonly Check[];
  readonly id: string;
  readonly input: string;
  readonly tags: readonly string[];
}
interface CheckResult {
  readonly message: string;
  readonly passed: boolean;
}
type Check = (run: AgentRun) => CheckResult | Promise<CheckResult>;
```
Seed the suite from:

- representative user tasks across common segments;
- difficult edge cases found during development;
- every confirmed production failure;
- tool timeouts, empty results, and malformed responses;
- permission and tenant-boundary tests;
- indirect prompt injection and data-exfiltration attempts;
- poisoned or conflicting memory; and
- tasks where the correct behavior is to ask, refuse, or stop.

Keep confidential data out of the repository. Synthesize or redact cases while preserving the behavior being tested. Version the dataset and make changes reviewable.

NIST’s [AI test, evaluation, validation, and verification program](https://www.nist.gov/ai-test-evaluation-validation-and-verification-tevv) emphasizes that trustworthy measurement requires context and multiple methods. The [NIST Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) recommends documented test data and content flows, known ground truth where possible, and both human and automated evaluation.

## Put deterministic checks first

Use code for anything code can judge. Deterministic checks are cheaper, more reproducible, and easier to debug than an LLM grader.

```
function didNotCall(...forbiddenNames: string[]): Check {
  return (run) => {
    const used = run.toolCalls
      .map((call) => call.name)
      .filter((name) => forbiddenNames.includes(name));
    return {
      passed: used.length === 0,
      message: used.length === 0
        ? "No forbidden tool was called."
        : `Forbidden tools called: ${used.join(", ")}`,
    };
  };
}
function answerIncludes(expected: string): Check {
  return (run) => ({
    passed: run.answer.includes(expected),
    message: `Answer must include ${JSON.stringify(expected)}.`,
  });
}
```
Other deterministic assertions include:

- JSON or domain-schema validation;
- exact calculations;
- required citations resolving to retrieved sources;
- maximum tool-call and token budgets;
- allowed tool names and argument ranges;
- no write before an approval event;
- tenant IDs never crossing the test fixture boundary; and
- expected state in a sandbox after a side effect.

Do not use string matching for semantic properties it cannot represent. “Contains refund” does not prove the answer followed refund policy.

## Grade semantics with a narrow rubric

Use a model grader only for properties that need language judgment. Give it:

- the original task;
- the observable run, including relevant tool calls;
- reference facts or sources;
- one property to judge;
- an anchored ordinal scale; and
- a required evidence field.

For example:

```
Judge only factual support.
2 = every consequential claim is supported by the supplied sources.
1 = the answer is mostly supported but contains a minor unsupported claim.
0 = a consequential claim is unsupported or contradicts a source.
Return JSON: {"score": 0|1|2, "evidence": ["..."]}
```
Validate the grader’s JSON. Calibrate it against a human-labeled set and measure disagreement. Freeze its model and rubric inside a release comparison. If the evaluator changes at the same time as the agent, you cannot tell whether the system moved or the ruler moved.

Never let a semantic grader override a hard safety failure. An eloquent answer does not excuse an unauthorized write.

## Repeat stochastic cases

One successful run says little when sampling and external tools vary. Run important cases several times and record the distribution.

```
async function evaluateCase(
  testCase: EvalCase,
  config: AgentConfig,
  trials: number,
): Promise<readonly (readonly CheckResult[])[]> {
  const results: CheckResult[][] = [];
  for (let trial = 0; trial < trials; trial += 1) {
    const run = await runAgent(testCase.input, config);
    results.push(await Promise.all(
      testCase.checks.map((check) => check(run)),
    ));
  }
  return results;
}
```
Use serial execution first for reproducibility and rate-limit safety. Add bounded parallelism after the harness is correct.

Report counts, not only percentages: 9/10 is more informative than 90%. For binomial pass/fail metrics, a Wilson lower confidence bound gives a conservative view of small samples:

```
function wilsonLowerBound(
  successes: number,
  total: number,
  z = 1.96,
): number {
  if (total === 0) return 0;
  const probability = successes / total;
  const zSquared = z * z;
  const denominator = 1 + zSquared / total;
  const center = probability + zSquared / (2 * total);
  const margin = z * Math.sqrt(
    (probability * (1 - probability) + zSquared / (4 * total)) / total,
  );
  return (center - margin) / denominator;
}
```
Confidence intervals do not fix a biased dataset. They only express sampling uncertainty for the cases you chose.

## Compare candidate and baseline on the same cases

A CI run should execute both configurations when cost permits:

```
baseline = current production model + prompt + tools
candidate = proposed model + prompt + tools
```
Use the same dataset snapshot, sandbox fixtures, grader, sampling settings, and trial count. Pair results by case so the report can say which tasks improved or regressed.

Track at least:

| Metric | Why it matters | 
|---|---|
| Task pass rate by tag | Averages can hide a broken segment | 
| Hard safety failures | Must usually be zero | 
| Tool error and retry rate | Reveals fragile trajectories | 
| p50 and p95 latency | Agents often have long tails | 
| Input/output tokens | Cost and context growth | 
| Human escalation rate | Can be correct behavior, but must be planned | 
| Grader-human agreement | Detects an unreliable evaluator | 

Do not claim a win because the mean score rises while a critical workflow falls.

## Write a release policy before seeing results

A defensible gate might be:

```
Block the release if any condition is true:
- any tenant isolation, unauthorized write, or secret-exfiltration test fails;
- a critical task tag regresses by more than the predeclared tolerance;
- the overall paired pass rate falls outside the accepted margin;
- p95 latency or mean token use exceeds its budget without an approved tradeoff;
- the candidate introduces a new unexplained production-error class.
```
Set thresholds from product risk and observed variance. Do not tune them after results appear just to make a desired release pass.

For a small fast suite, run every pull request. Put slower repeated and adversarial suites on merge, nightly, and pre-deployment gates. Store the report and normalized traces as artifacts with access controls and retention limits.

## Debug failures without grading the grader

For each failing case, show:

- dataset ID and version;
- baseline and candidate configuration fingerprints;
- trial number and random/sampling configuration;
- check name and evidence;
- tool trajectory with sensitive fields redacted;
- retrieved source IDs;
- latency and token counts; and
- links to the relevant trace.

Then classify the cause: dataset error, harness error, evaluator error, model behavior, retrieval, tool, or orchestration. Fixing a mislabeled case is legitimate; silently deleting a hard case is not.

Instrument the runtime with [OpenTelemetry traces](https://stanleycyang.com/writing/trace-ai-agents-opentelemetry) so an eval failure can be inspected using the same signals as production.

## Avoid the common eval traps

- **Only happy paths:** the suite becomes a demo, not a risk control.
- **One trial:** intermittent regressions appear fixed.
- **One aggregate score:** critical failures disappear in the mean.
- **Model grader as ground truth:** evaluator bias becomes product policy.
- **Leaking expected answers:** the test measures prompt recognition.
- **Changing agent and grader together:** the comparison loses its reference.
- **No production feedback loop:** the suite stops representing actual failures.
- **CI without artifacts:** a red build cannot be diagnosed.

The goal is not a magical universal score. It is a repeatable body of evidence that lets an accountable person decide whether this specific system change is safe and useful.
