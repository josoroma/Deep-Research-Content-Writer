---
source_id: S-23
url: https://www.buildmvpfast.com/blog/tracing-ai-agent-workflows-opentelemetry-multi-step-2026
title: 'OpenTelemetry for AI Agents: Tracing Multi-Step Workflows'
author: BuildMVPFast
published: '2026-03-29'
fetched: '2026-10-09T21:41:50Z'
word_count: 2845
---
# OpenTelemetry for AI Agents: Tracing Multi-Step Workflows

Picture shipping an AI agent that handles customer refund requests. It works in staging. Five steps: classify intent, pull order history, check refund eligibility, draft the response, send it. Clean and linear.

In production, it starts approving refunds for orders that don’t exist. You spend two days staring at logs that tell you nothing useful. The agent logged its final output and the initial input. Everything in between is a black box.

Turns out the retrieval step was pulling the wrong order because of a stale embedding index, and the eligibility check was passing because it received an empty response (which it interpreted as “no restrictions found”). Two bugs, zero visibility.


That’s the moment you stop treating AI agent observability as a “nice-to-have” and start instrumenting every step. A survey of 1,300+ developers found that 89% say they have “some form of observability” for their AI systems, but only 62% can actually inspect individual steps. That gap is where the bugs hide.

## Update: April 2026

A couple of details changed quickly after this post went live. [Anthropic](https://www.buildmvpfast.com/alternatives/anthropic) moved Claude Cowork to [general availability](https://support.claude.com/en/articles/12138966-release-notes) on April 9 and added [OpenTelemetry support for Cowork activity](https://support.claude.com/en/articles/14477985-monitor-claude-cowork-activity-with-opentelemetry) on Team and Enterprise plans, which matters if you want the same observability discipline outside terminal-only agent workflows. Anthropic’s [Claude Code monitoring docs](https://code.claude.com/docs/en/monitoring-usage) also now spell out concrete span fields such as `gen_ai.system`, `gen_ai.request.model`, request IDs, token counts, and error status.

One caveat is still easy to miss: OpenTelemetry’s [GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) remain in Development status and still use the `OTEL_SEMCONV_STABILITY_OPT_IN` transition path. In practice, that means your dashboards, collectors, and field mappings should be treated as versioned infrastructure, not as a schema that is done forever.

## Update: July 2026 (the conventions moved repos)

Since April, the biggest change is structural, and it will break the link above if you rely on it. In [release v1.42.0](https://github.com/open-telemetry/semantic-conventions/releases) (June 12, 2026), the OpenTelemetry project deprecated every `gen_ai.*` attribute, metric, event, and span in the main semantic-conventions repo and moved them to a dedicated [semantic-conventions-genai repository](https://github.com/open-telemetry/semantic-conventions-genai). The old `opentelemetry.io/docs/specs/semconv/gen-ai/` page is now a redirect notice, so update any bookmarks and docs links your team pinned earlier in the year.

Two span-level changes landed just before that, in v1.41.0 (April 28). The `invoke_agent` span was split into a CLIENT variant for remote agent calls and an INTERNAL variant for local framework execution, so a self-hosted LangGraph run and a call out to a remote agent service no longer look identical in the waterfall. And `execute_tool` now requires the tool name in the span name itself, which makes tool failures easier to scan without opening each span. MCP tool tracing, added back in v1.39, propagates context between your agent and the MCP server so those calls join one trace instead of splitting into two.

The status has not changed: the GenAI and MCP conventions are still Development, with no public stabilization date. As the maintainers put it, attribute names may still shift, but the core concepts have settled. The practical takeaway is the same as before, pin your emitted version and treat the schema as living infrastructure.

## Your agent is a distributed system. Trace it like one.

Here’s something that took me embarrassingly long to realize: a multi-step AI agent is a distributed system. Each step (LLM call, tool execution, retrieval, validation) is a service boundary with its own failure modes and latency profile. Each one costs money too.

Traditional application logging gives you timestamps and messages. That’s fine when your code is deterministic. But LLM calls are non-deterministic, tool calls can fail silently, and agent orchestration frameworks like [LangGraph and CrewAI](https://www.buildmvpfast.com/blog/langgraph-vs-crewai-vs-autogen-vs-swarms-agent-framework-2026) add branching logic that makes a linear log stream borderline useless.

What you actually need is distributed tracing. The same concept that SREs have used for microservices since Google published the Dagger paper in 2010, and the same primitive that [autonomous SRE agents like NeuBird Falcon](https://www.buildmvpfast.com/blog/neubird-autonomous-sre-ai-agent-production-incident-2026) consume to triage production incidents. Every agent run gets a trace ID. Every step within that run gets a span. Spans have parent-child relationships, timestamps, durations, and attributes (metadata). When something breaks, you don’t grep through logs. You pull up the trace, see the waterfall view, and pinpoint exactly which span failed and why.

A developer on r/LocalLLaMA put it well: “I tried to hand-roll observability for local LLM inference… then realized OpenTelemetry solves the ‘parent span / timestamps / threads’ mess.” That’s the pattern I keep seeing. Teams build custom logging, realize it doesn’t scale past three agent steps, and migrate to proper tracing.

## OpenTelemetry’s GenAI semantic conventions

OpenTelemetry is the CNCF standard for observability. Traces, metrics, and logs with a vendor-neutral API. If you’ve used Jaeger, [Datadog](https://www.buildmvpfast.com/alternatives/datadog), or Grafana Tempo for backend tracing, you already know the primitives.

What’s newer is the **GenAI semantic conventions**. The OpenTelemetry project has been building a standardized set of attribute names specifically for LLM and AI agent workloads. These conventions define how to record things like `gen_ai.system` (which provider: openai, anthropic, cohere), `gen_ai.request.model` (which model), `gen_ai.usage.input_tokens` and `gen_ai.usage.output_tokens` (token counts), and `gen_ai.request.temperature`.

Why does this matter? Because without standard attribute names, every observability tool invents its own schema. Langfuse calls it `model`, LangSmith calls it `llm`, your custom logging calls it `model_name`. Then you try to query across tools and nothing lines up. The GenAI conventions solve this the same way HTTP semantic conventions solved it for web requests years ago.

The conventions also cover **tool calls** (`gen_ai.tool.name`, `gen_ai.tool.description`) and **agent events**, which means you can trace an entire multi-step workflow with standardized attributes that any OTel-compatible backend can understand. As of April 2026, though, the spec is still marked Development, so pin the emitted version instead of assuming every backend is already aligned.

## OpenLLMetry and the $70M acquisition that nobody expected

OK so I need to talk about **Traceloop** and their open-source project **OpenLLMetry**, because the story here is wild.

OpenLLMetry is a set of OpenTelemetry-native instrumentations for LLM providers. You initialize it with a single line of code, and it auto-instruments calls to [OpenAI](https://www.buildmvpfast.com/alternatives/openai), Anthropic, Cohere, Bedrock, and 20+ other providers. No manual span creation needed. It captures prompts, completions, token counts, latency, model parameters, and cost estimates automatically.

The project has been steadily growing since 2024. Auto-instrumentation for LangChain, LlamaIndex, Haystack, and the [Vercel](https://www.buildmvpfast.com/alternatives/vercel) AI SDK. Support for vector databases (Pinecone, Chroma, Weaviate) so your RAG pipeline traces include the retrieval step too.

Then in March 2026, ServiceNow acquired Traceloop for a reported $60-80 million. This was their third acquisition in three months (after Armis and Pyramid Analytics). One investor on Twitter framed it as ServiceNow building an “AI Control Tower” stack: “Moveworks = orchestration, Veza = identity, Armis = visibility, Traceloop = evaluation. You can’t govern agents you can’t observe.”

That acquisition tells you something about where the industry is heading. Prompt evaluation (Promptfoo, [acquired by OpenAI for $86M](https://www.buildmvpfast.com/blog/prompt-engineering-product-development-versioning-testing-2026)) and agent tracing (OpenLLMetry, acquired by ServiceNow) are no longer nice-to-haves. They’re infrastructure.

The open-source project still works. You can still use it. But if you’re evaluating observability tools in 2026, knowing who owns what matters for long-term bets.

## The span model for agent workflows

Let me get concrete about how traces map to agent steps. I’m going to use a real example: a customer support agent that classifies a ticket, retrieves relevant knowledge base articles, drafts a response, and reviews it before sending.

Here’s the trace structure:

```
Trace: customer_support_agent (trace_id: abc123)
├── Span: classify_intent (LLM call)
│   ├── gen_ai.system: "anthropic"
│   ├── gen_ai.request.model: "claude-sonnet-4-6"
│   ├── gen_ai.usage.input_tokens: 342
│   ├── gen_ai.usage.output_tokens: 28
│   └── duration: 1.2s
├── Span: retrieve_knowledge (tool call)
│   ├── tool.name: "vector_search"
│   ├── retrieval.document_count: 5
│   ├── retrieval.top_score: 0.89
│   └── duration: 0.3s
├── Span: draft_response (LLM call)
│   ├── gen_ai.system: "anthropic"
│   ├── gen_ai.request.model: "claude-sonnet-4-6"
│   ├── gen_ai.usage.input_tokens: 1847
│   ├── gen_ai.usage.output_tokens: 312
│   └── duration: 3.1s
└── Span: review_response (LLM call)
    ├── gen_ai.system: "openai"
    ├── gen_ai.request.model: "gpt-4o-mini"
    ├── gen_ai.usage.input_tokens: 654
    ├── gen_ai.usage.output_tokens: 45
    ├── review.passed: true
    └── duration: 0.8s
```
Total trace duration: 5.4 seconds. Total tokens: 3,228. You can see that the draft_response span takes 57% of the total time and 67% of the token spend. That’s where optimization efforts should go.

When this agent fails, the trace tells you exactly where. If the retrieval step returns zero documents, you see `retrieval.document_count: 0` and a low `retrieval.top_score`. If the review step rejects the draft, you see `review.passed: false` and can inspect why. If the LLM times out, you see the span duration spike.

For [parallel agent architectures](https://www.buildmvpfast.com/blog/parallel-sequential-agent-architecture-saas-design-2026), each parallel branch becomes a set of concurrent child spans under the same parent. The trace visualizer renders them as horizontal bars running at the same time, so you can immediately see if one branch is bottlenecking the others.

## Instrumenting your agents (the practical part)

Slight detour, but this matters. The gap between “understanding traces conceptually” and “actually instrumenting your agent code” is where most teams stall. So let me walk through the two main approaches.

**Approach 1: Auto-instrumentation (the easy way)**

If you’re using a supported framework, OpenLLMetry handles this with one line:

```
from traceloop.sdk import Traceloop
Traceloop.init(app_name="my-agent")
```
That’s it. Every OpenAI, Anthropic, and Cohere call in your application gets traced automatically. If you’re using LangChain or LlamaIndex, those calls are instrumented too. The SDK creates spans with standard GenAI attributes, captures token counts, records latency, and forwards everything to whatever OpenTelemetry backend you’ve configured (Jaeger, Grafana Tempo, Arize Phoenix, Langfuse).

JetBrains shipped native OpenTelemetry support in Koog 0.3.0, their Kotlin agent framework. The Agno agent framework added Traceloop integration with “just two lines” of code. This pattern of “initialize once, instrument everything” is becoming standard across agent frameworks.

**Approach 2: Manual spans (when you need control)**

Auto-instrumentation doesn’t cover custom tool calls, business logic steps, or homegrown orchestration. For those, you create spans manually:

```
from opentelemetry import trace
tracer = trace.get_tracer("my-agent")
with tracer.start_as_current_span("validate_refund_eligibility") as span:
    span.set_attribute("order.id", order_id)
    span.set_attribute("order.total", order_total)
    span.set_attribute("refund.reason", reason)
    result = check_eligibility(order_id, reason)
    span.set_attribute("eligibility.approved", result.approved)
    span.set_attribute("eligibility.rule_matched", result.rule)
```
In practice, most teams use both. Auto-instrumentation catches all LLM calls. Manual spans cover the business logic glue between them. Together, you get a complete picture.

One thing I learned the hard way: always add a `span.set_status(StatusCode.ERROR)` and `span.record_exception(e)` in your except blocks. Without this, failed spans look identical to successful ones in the trace view, and you’re back to grepping logs.

Fair warning about auto-instrumentation: one developer on r/Observability reported that “auto-instrumentors create duplicate spans, break trace-log correlation for post-response processing, and truncate content.” They switched to manual instrumentation for their OpenAI calls while keeping auto-instrumentation for everything else. If your traces look noisy, that’s probably why.


## Langfuse, Arize Phoenix, and LangSmith

Now here’s where it gets interesting. You’ve got your traces. Where do you send them? The observability tool market for AI agents has gotten crowded, and a few things have shifted recently.

**Langfuse** is open-source, self-hostable, and has 10,000+ GitHub stars. It does tracing and prompt management in one platform, with evaluation layered on top. You can version prompts alongside their traces, which means you can answer “which prompt version caused this regression?” directly from the trace view. Their Python and JS SDKs integrate with OpenAI, Anthropic, LangChain, and LlamaIndex. They also accept OpenTelemetry traces natively now.

What I like about Langfuse: the prompt management + tracing combination. Most tools do one or the other. When you’re debugging a prompt regression, being able to see both the prompt version and its execution trace in the same view saves a lot of tab-switching.

**Arize Phoenix** is another open-source option, more focused on ML observability. It started as a tool for traditional ML model monitoring and expanded into LLM tracing. The standout feature is built-in evaluation metrics. You can run evals directly on your traces without exporting them. It also has a visual trace viewer that renders the span waterfall with inline token counts.

**LangSmith** by LangChain added OpenTelemetry support in late 2024. It now ingests traces in OpenLLMetry format, which means you can use standard OTel instrumentation and send traces to LangSmith without their proprietary SDK. That said, LangSmith is tightly coupled to the LangChain ecosystem. If you’re using LangGraph, it’s the path of least resistance. If you’re not, Langfuse or Phoenix give you more flexibility.

Worth noting: **Helicone** was acquired by Mintlify in early 2026. A thread on r/LLMDevs titled “Helicone was acquired by Mintlify, what are the best alternatives now?” had 15 comments of developers scrambling. The consensus: Langfuse for open-source, Braintrust for enterprise. If you were using Helicone, now’s the time to migrate.

One developer on Twitter summed up the tool fragmentation: “we were literally integrating langfuse, posthog, braintrust, langsmith, traceloop, axiom, signoz, datadog, and many others to see which one works with AI SDK well.” That’s the reality right now. Too many options, not enough standardization.

## What to actually trace (and what to skip)

I realize I glossed over something: not everything needs a span. Over-instrumentation makes traces unreadable and eats storage. Here’s what to capture and what to leave out.

**Always trace:**

- Every LLM call (model, tokens in/out, temperature, latency, response status)
- Every tool/function call (tool name, input args summary, output summary, duration)
- Every retrieval step (query, document count, top relevance score, source)
- Agent decision points (which branch was taken and why)
- Cache hits and misses (did this LLM call hit the [semantic cache](https://www.buildmvpfast.com/blog/semantic-caching-ai-agents-cost-optimization) or not?)
- Errors and retries (exception type, retry count, [fallback model used](https://www.buildmvpfast.com/blog/llm-fallback-strategies-primary-model-secondary-model-2026) )

**Skip these:**

- Individual prompt template rendering (trace the LLM call, not the string formatting)
- Internal framework plumbing (LangChain’s chain assembly steps, CrewAI’s internal routing)
- Full prompt text in production (capture a hash or version ID instead for privacy and storage)
- Sub-millisecond operations (JSON parsing, config lookups, variable assignments)

The reason I emphasize skipping prompt text in production traces: compliance. If your agent handles customer data, PII in your traces creates a whole new category of problems. Capture `prompt.version: "v2.3.1"` and `prompt.hash: "a4f2c8"` instead. You can always look up the full prompt from your prompt versioning system when you need it.

**The attributes that actually help you debug:**

| Attribute | Why It Matters | 
|---|---|
| gen_ai.usage.input_tokens | Cost attribution per step | 
| gen_ai.usage.output_tokens | Spot runaway generation (token leaks) | 
| retrieval.document_count | Zero documents = retrieval failure | 
| retrieval.top_score | Low score = bad embedding or stale index | 
| tool.status_code | API tool failures | 
| agent.iteration_count | Detect infinite loops in ReAct agents | 
| cache.hit | Measure your caching ROI | 
| error.type + error.message | Self-explanatory | 

One developer observed this about the OTel-vs-custom tracing debate: “We built an OTel layer for LLM apps because standard tracing was not enough.” The standard GenAI conventions cover 80% of what you need. The remaining 20% is custom attributes specific to your agent’s domain logic.

## The minimum viable tracing stack for 2026

If I’m being honest, most teams overthink this. You don’t need five observability tools. Here’s what I’d set up today for a team shipping their first AI agent to production.

**Instrumentation:** OpenLLMetry (still open-source, still works post-acquisition). One line to initialize. Auto-instruments all major LLM providers, LangChain, LlamaIndex. Free. If your team is already standardized on Anthropic, Claude Code now documents OTel spans, metrics, and events directly, and Claude Cowork can stream OTel activity on Team and Enterprise plans.

**Backend:** Start with **Langfuse** (open-source, self-hostable). Tracing + prompt management + basic evaluation. Their free cloud tier handles most early-stage products. If you’re already running Grafana, you can also export OTel traces to **Grafana Tempo** for the trace backend and use Langfuse just for the AI-specific features.

**Visualization:** Langfuse’s built-in trace viewer works. For more complex debugging, **AgentPrism** (launched September 2025) is a React component library specifically for visualizing OpenTelemetry traces from AI agents. LLM calls, tool executions, and agent workflows rendered as interactive span hierarchies. If you’re building a custom internal dashboard for your AI operations, it’s worth a look.

**Alerting:** Set up alerts on three things: (1) trace duration exceeding your SLA, (2) token count anomalies (sudden spikes mean something is generating uncontrolled output), and (3) error rates per agent step. If you’re tracking [inference costs](https://www.buildmvpfast.com/blog/ai-saas-inference-cost-metrics-tracking-2026), add token cost per trace as a fourth alert.

That’s it. OpenLLMetry for instrumentation, Langfuse for backend, basic alerting on duration/tokens/errors. You can add Arize Phoenix for evaluation, Braintrust for experiments, or Datadog for enterprise-scale monitoring later. But this gets you from “black box agent” to “I can debug any failure in 30 seconds” in an afternoon.

If you’re [building with unreliable AI](https://www.buildmvpfast.com/blog/building-with-unreliable-ai-error-handling-fallback-strategies-2026) (and you are, because all AI is unreliable), tracing is what turns “it broke” into “step 3 failed because the API returned a 429 and the fallback model hallucinated the tool schema.” That level of specificity is the difference between a 2-hour debugging session and a 5-minute fix.

## Frequently Asked Questions

## Read next

Tap + on a card to add it to your Read next list.
