---
source_id: S-20
url: https://docs.fiddler.ai/observability/agentic
title: Agentic Observability - Fiddler Documentation
author: null
published: null
fetched: '2026-10-09T21:23:52Z'
word_count: 660
---
# Agentic Observability - Fiddler Documentation

## Dashboards & Visualization

Agentic observability uses a dedicated UI with Projects → Applications (instead of the legacy Projects → Models structure) designed specifically for observing agent workflows.
### Agentic Dashboards

Access pre-built dashboards optimized for agentic workflows:
- **Agent Performance Overview** - Monitor success rates, latency, and throughput across all agents
- **Workflow Execution Traces** - Visualize complete multi-step reasoning chains from start to finish
- **Tool Usage Analytics** - Track which external tools and APIs your agents are calling
- **Error & Exception Tracking** - Identify where agent workflows fail and why

### Trace Visualization

Every agent interaction is captured as a hierarchical trace showing:
- **Agent Steps** - Each decision point in the agent’s reasoning process
- **LLM Calls** - All language model interactions with inputs, outputs, and metadata
- **Tool Invocations** - External function calls, API requests, and data retrievals
- **Timing Information** - Duration of each step to identify performance bottlenecks
- **Parent-Child Relationships** - How multi-agent systems coordinate and delegate tasks

**Viewing Traces:**

1. Navigate to your Application in the Fiddler UI
2. Select a conversation or workflow from the list
3. Click on any trace to expand the full execution tree
4. Drill down into individual spans to see inputs, outputs, and metadata

### Custom Dashboards

Create custom dashboards to monitor specific agent behaviors:
- Combine multiple charts to track KPIs relevant to your use case
- Filter by agent type, user segments, or time periods
- Share dashboards with team members
- Set up alerts based on dashboard metrics

## Metrics & Analytics

Agentic observability provides specialized metrics that go beyond traditional model monitoring:
### Agent-Specific Metrics

- **Agent Success Rate** - Percentage of workflows that complete successfully
- **Tool Call Distribution** - Which tools agents use most frequently
- **Reasoning Chain Length** - Average number of steps per workflow
- **Agent Handoffs** - How often agents delegate to other agents
- **Retry & Recovery Rate** - How often agents recover from errors

### Performance Metrics

- **End-to-End Latency** - Total time from user request to final response
- **Per-Step Latency** - Duration of individual reasoning steps, LLM calls, and tool invocations
- **Token Usage** - Track LLM consumption across all agent interactions
- **API Call Volume** - Monitor external tool and API usage

### Quality Metrics

- **Response Accuracy** - Validate agent outputs against expected results (requires ground truth)
- **Hallucination Detection** - Identify when agents generate unsupported claims
- **Safety & Guardrails** - Track safety violations and guardrail activations
- **User Satisfaction** - Capture feedback signals from end users

### Analyzing Metrics

All metrics are available in:
- **Real-time Dashboards** - Monitor live agent performance
- **Historical Trends** - Analyze patterns over days, weeks, or months
- **Comparative Analysis** - Compare different agent versions or configurations
- **Custom Queries** - Use Fiddler Query Language (FQL) for advanced analysis

## Integration Options

Agentic observability ingests OpenTelemetry spans and traces from your agent applications. Choose the integration method that fits your framework:
### LangGraph Applications

**Best for:**Applications built with LangGraph or LangChain The Fiddler LangGraph SDK provides automatic instrumentation with zero code changes required.

[- Get started in 10 minutes →](https://docs.fiddler.ai/developers/quick-starts/langgraph-sdk-quick-start)

**LangGraph SDK Quick Start**
[- Complete integration guide](https://docs.fiddler.ai/sdk-api/langgraph/fiddler-client)

**LangGraph SDK Documentation**
### Strands Agent Framework

**Best for:**Applications built with Strands Agents The Fiddler Strands SDK integrates directly with the Strands framework for seamless monitoring.

[- Get started in 15 minutes →](https://docs.fiddler.ai/developers/quick-starts/strands-agent-quick-start)

**Strands Agent SDK Quick Start**
[- Complete integration guide](https://docs.fiddler.ai/sdk-api/strands/strands-agent-instrumentor)

**Strands SDK Documentation**
### Custom Instrumentation (OpenTelemetry)

**Best for:**Custom agent frameworks or non-Python applications Use OpenTelemetry directly for maximum flexibility and control.

[- Get started in 20 minutes →](https://docs.fiddler.ai/developers/quick-starts/opentelemetry-quick-start)

**OpenTelemetry Quick Start**
[- Complete integration guide](https://docs.fiddler.ai/integrations/agentic-ai/opentelemetry-integration)

**OpenTelemetry Documentation**
### LiteLLM (SDK & Proxy)

**Best for:**Applications or gateways routing LLM calls through LiteLLM LiteLLM’s built-in OpenTelemetry integration sends every LLM call to Fiddler — no Fiddler-specific package required. →

[- Complete integration guide](https://docs.fiddler.ai/integrations/agentic-ai/litellm-integration)

**LiteLLM Integration**
### AI Gateways (Kong, AgentGateway, LiteLLM)

**Best for:**Traffic already routed through a third-party AI gateway. Fiddler plugs into Kong, AgentGateway, or LiteLLM at the proxy layer for observability and guardrail enforcement, with no application code changes. →

[- Capability comparison and per-gateway setup links](https://docs.fiddler.ai/integrations/agentic-ai/ai-gateways)

**AI Gateway Integrations**
### Integration Comparison

## Next Steps

- **Getting Started:** Learn the concepts behind agentic observability in our[Agentic Observability Getting Started Guide](https://docs.fiddler.ai/getting-started/agentic-monitoring)
- **Choose Integration:** Pick your framework and follow the quick start guide above
- **Explore Features:** Set up dashboards, configure alerts, and analyze agent performance
- **Advanced Topics:** Learn about[custom metrics](https://docs.fiddler.ai/observability/platform/custom-metrics) ,[alerts](https://docs.fiddler.ai/observability/platform/alerts-platform) , and[segmentation](https://docs.fiddler.ai/observability/platform/segments)
