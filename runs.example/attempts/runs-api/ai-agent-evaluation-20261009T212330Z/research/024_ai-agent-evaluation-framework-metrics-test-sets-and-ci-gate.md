---
source_id: S-24
url: https://www.codiste.com/ai-agent-evaluation-framework
title: 'AI Agent Evaluation Framework: Metrics, Test Sets and CI Gate'
author: Nishant Bijani
published: '2026-10-05T13:45:59.477908+00:00'
fetched: '2026-10-09T21:23:53Z'
word_count: 1857
---
# AI Agent Evaluation Framework: Metrics, Test Sets and CI Gate

Someone edits one line in a support agent's prompt to make it sound friendlier. Every demo conversation still looks fine, so the change ships. Two days later the agent quietly stopped asking for an order number before it issues refunds.

Nothing crashed, no error fired, and no single answer looked wrong. That is what makes agents hard to test. A chatbot gives you one reply to grade. An agent takes a dozen steps, calls tools and changes records, and it can fail in any of them while the final message reads perfectly.

This guide lays out a practical [AI agent evaluation](https://www.codiste.com/ai-agent-evaluation) framework in three parts: the metrics to measure, the test sets to build, and the CI gates that stop a bad change from reaching production.

An AI agent evaluation framework is a repeatable system for testing whether an agent completes its tasks correctly, consistently and within budget. It defines what to measure, which test cases to run, how each result is graded, and which scores must pass before a change can be deployed.

Every framework, whatever the tooling, is built from the same six parts. Anthropic's engineering guide to agent evals uses this vocabulary, and it is worth adopting because it makes conversations between engineers precise:

Most LLM evaluation grades a single response: did the model answer the question accurately and well? Agent evaluation has to grade a process, and that changes almost everything about how the test works.

The practical consequence: an agent can produce a polished, accurate-sounding final message while having called the wrong tool, updated the wrong record or skipped a required check. If your evaluation only reads the last message, it will pass that agent.

Most LLM evaluation metrics score a single response for accuracy or relevance. Agentic AI evaluation metrics have to cover more: correctness, reliability, efficiency and safety across many steps. These eight cover most production agents:

Task success is the headline number: did the agent finish what the user asked? Grade it on the outcome, not the wording. For a booking agent, the test is whether the reservation exists with the right date and guests, not whether the agent said “your booking is confirmed”. AWS's published framework for its own agents separates this into goal success, whether every user goal was met, and goal accuracy, whether the result matches the ground truth.

These two metrics catch most agent bugs before they reach a customer. Tool selection asks whether the agent chose the right function: fetching quarterly revenue instead of general market data. Parameter accuracy asks whether it filled that function correctly: the right region, the right quarter, in the right format.

Both are easy to grade with code, because the expected call is known. That makes them ideal CI gates. AWS's production blueprint blocks a deploy when tool selection accuracy falls below 95%.

Agents give different results on different runs of the same task, so a single pass tells you little. Two metrics handle this, and they answer different questions:

The gap between them is large. An agent with 75% success per attempt scores about 98% on pass@3 but only about 42% on pass^3. Sierra introduced pass^k with τ-bench (tau bench), its tool-agent-user benchmark, in June 2024, after finding that agents with respectable single-run scores degraded sharply across repeated runs. If your agent talks to customers, pass^k is the reliability number to report.

A grounded agent only states what its sources or tools returned. Check groundedness by comparing each claim in the final answer against the retrieved documents or tool outputs. This is one of the few places an LLM judge earns its cost, because matching a claim to a source is hard to do with exact string rules.

Measure both per completed task, not per model call. An agent that makes eleven tool calls to finish a job can be slow and expensive even when each call is fast and cheap. Track p95 latency, the slowest 5% of tasks, because that is what a frustrated user experiences. A model swap often trades one against the other: AWS's own example shows a smaller model cutting median latency from 3.2 to 1.8 seconds while tool selection accuracy fell from 92% to 87%. Your eval suite is what makes that trade visible before customers find it.

Handoff rate is how often the agent escalates to a person. Too high, and the agent saves little. Too low, and it is probably guessing when it should stop. Grade the quality of each handoff as well as the rate: did it escalate the cases your rules say it must, and did it pass enough context that the person did not start again?

Use three kinds of graders, in this order of preference:

LLM judges carry known biases. The MT-Bench research that established the method in 2023 found three: a preference for whichever answer appears first, a preference for longer answers, and a preference for output written by the judge's own model family. Shuffle answer order, cap response length in the rubric, and use a different model as judge than the one being tested.

Two rules from Anthropic's guide apply across every grader. Grade the outcome rather than the exact path, because an agent may find a valid route you did not anticipate. And read transcripts regularly: you will not know whether your graders are fair until you look at what they passed and failed.

A good test set is small, real and growing. Build it in three layers.

Start with 20 to 50 tasks, which is the starting range Anthropic recommends. Take them from real user requests and real failures, not from scenarios your team imagines. For each, record the input, the starting state, and the expected outcome and tool calls. This golden dataset is the core of everything that follows, so spend time making each success definition unambiguous.

Add the cases that break agents: missing information, contradictory instructions, a tool that returns an error, a user who changes their mind halfway, a request the agent should refuse. Each edge case should have a defined correct behavior, which is often a clean handoff rather than an answer.

Every time the agent fails in production, turn the failure into a test case. This is how the suite grows to match the real world, and it guarantees the same bug cannot ship twice. AWS describes the same practice: let real user behavior grow the evaluation suite.

Keep two separate suites. A capability suite holds hard tasks the agent cannot yet do reliably; its pass rate starts low and shows whether changes improve the agent. A regression suite holds tasks the agent already handles; its pass rate should sit near 100%, and any drop signals a break. When a capability task passes consistently, move it into the regression suite.

One warning: a suite at 100% catches regressions but tells you nothing about improvement. If every score is perfect, add harder tasks.

Most agent failures we see come from evaluation gaps, not model limits: no golden set, no consistency check, no gate before deploy. Codiste builds the test set, graders and CI gates alongside the agent, so the team that takes it over can change it safely.

A CI gate turns your evaluation into a release rule: the suite runs automatically, and the deploy is blocked if a metric falls below its threshold. Set gates for each layer of the framework:

Set thresholds relative to your current production numbers rather than ideal targets. A gate that blocks every release gets switched off.

Run the suite on every change that can alter agent behavior, not only on code changes: a prompt edit, a model or model version swap, a new or changed tool, a change to retrieval data or the knowledge base, and an update to any connected API. Prompt and model changes are the ones teams most often ship without testing, and they are the most likely to cause quiet regressions like the refund example at the top of this guide.

CI gates protect releases. Agent observability and [AI agent monitoring](https://www.codiste.com/ai-agents-aml-transaction-monitoring) protect everything after release. Trace production runs, sample a share of live interactions, and score them with the same graders you use in CI. Some teams also run a new version in shadow mode first: it processes real traffic in parallel, without affecting users, so you can compare its scores against production before switching over. When monitoring finds a new failure, it goes into the regression suite, which closes the loop.

Tools do not build the framework for you. They run it. Choose by which part of the framework you need covered:

Two notes on choosing. Pick tools that keep your test cases in your own repository or export them cleanly, because the test set is the asset you are building. And treat public benchmarks as orientation only: a model's τ-bench score says little about how it handles your tools, your data and your rules. For context on where agents are already in production, see our guide to [AI agents for business](https://codiste.com/blog/ai-agents-for-business).

Most problems in AI agent testing come from a handful of habits:

An agent that works in a demo and an agent that works on Monday morning are different products, and the difference is evaluation. Agents fail quietly. They call the wrong tool, skip a step or drift after a prompt edit, and the final message still reads as if nothing went wrong.

The framework that catches this is not complicated. Measure the outcome and the steps, not only the reply. Run each task more than once and report pass^k for anything customers touch, because single-run scores flatter every agent. Grade with code wherever a right answer exists, use an LLM judge only where it does not, and check that judge against people.

The test set matters more than any tool. Twenty to fifty real tasks, a set of edge cases, and a regression case for every production failure will tell you more than a public benchmark ever will. That set grows with the agent, and after a year it becomes the most valuable thing your team owns about it.

Then put it in the release path. Every prompt edit, model swap and tool change runs the suite, and a drop below the threshold blocks the deploy. Teams that do this ship agent changes with confidence. Teams that skip it find their regressions in customer complaints, usually days after the change that caused them, and spend the next week working out which change it was.

If your agent is in production without a test set or a release gate, Codiste can build both around the agent you already have, starting from the failures your users have already found.

Nishant builds where ambitious ideas meet production reality. As CTO & Co-Founder at Codiste, he has helped ship 150+ AI systems. Through The CTO Story, he gets technical leaders talking about what rarely makes the slide deck: the trade-offs, failures, and decisions behind what actually ships.

Every great partnership begins with a conversation. Whether you're exploring possibilities or ready to scale, our team of specialists will help you navigate the journey.
