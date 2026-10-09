---
source_id: S-28
url: https://kernel.yaala.ai/docs/advanced/traceability
title: Traceability and Observability | Agent Kernel
author: Yaala Labs
published: null
fetched: '2026-10-09T21:41:53Z'
word_count: 2057
---
# Traceability and Observability | Agent Kernel

Track, monitor, and debug all agent operations with built-in tracing and observability features.

## Overview[](https://kernel.yaala.ai#overview)

Agent Kernel provides comprehensive observability capabilities through integration with popular tracing platforms. Monitor agent execution, debug issues, and gain insights into your AI agent systems.

## Supported Platforms[](https://kernel.yaala.ai#supported-platforms)

Agent Kernel supports the following observability platforms:

- **Langfuse** - Open-source LLM engineering platform for tracing, evaluating, and monitoring AI applications
- **OpenLLMetry (Traceloop)** - OpenTelemetry-based observability for LLM applications with support for multiple backends
- **Pydantic Logfire** - OpenTelemetry-based observability from the Pydantic team, with a native OpenAI Agents SDK integration

## Getting Started with Langfuse[](https://kernel.yaala.ai#getting-started-with-langfuse)

### Installation[](https://kernel.yaala.ai#installation)

Install Agent Kernel with Langfuse support:

```
pip install agentkernel[langfuse]
```
Or if you need multiple framework integrations:

```
# OpenAI with Langfuse
pip install agentkernel[openai,langfuse]
# LangGraph with Langfuse
pip install agentkernel[langgraph,langfuse]
# CrewAI with Langfuse
pip install agentkernel[crewai,langfuse]
# Google ADK with Langfuse
pip install agentkernel[adk,langfuse]
```
### Configuration[](https://kernel.yaala.ai#configuration)

#### Method 1: Configuration File[](https://kernel.yaala.ai#method-1-configuration-file)

Create or update `config.yaml`:

```
trace:
  enabled: true
  type: langfuse
```
#### Method 2: Environment Variables[](https://kernel.yaala.ai#method-2-environment-variables)

```
export AK_TRACE__ENABLED=true
export AK_TRACE__TYPE=langfuse
```
With tracing enabled in config, all agent interactions will be automatically traced to Langfuse.

### Langfuse Credentials[](https://kernel.yaala.ai#langfuse-credentials)

Configure Langfuse credentials via environment variables:

```
export LANGFUSE_PUBLIC_KEY=pk-lf-...
export LANGFUSE_SECRET_KEY=sk-lf-...
export LANGFUSE_HOST=https://cloud.langfuse.com  # or your self-hosted instance
```
Or add them to your `.env` file:

```
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com
```
### Getting Langfuse Credentials[](https://kernel.yaala.ai#getting-langfuse-credentials)

1. Sign up for a free account at [https://cloud.langfuse.com](https://cloud.langfuse.com)
2. Create a new project
3. Navigate to **Settings** →**API Keys**
4. Copy your Public Key and Secret Key

For self-hosted Langfuse, see the [Langfuse documentation](https://langfuse.com/docs/deployment/self-host).

## Getting Started with OpenLLMetry (Traceloop)[](https://kernel.yaala.ai#getting-started-with-openllmetry-traceloop)

### Installation[](https://kernel.yaala.ai#installation-1)

Install Agent Kernel with OpenLLMetry support:

```
pip install agentkernel[openllmetry]
```
Or if you need multiple framework integrations:

```
# OpenAI with OpenLLMetry
pip install agentkernel[openai,openllmetry]
# LangGraph with OpenLLMetry
pip install agentkernel[langgraph,openllmetry]
# CrewAI with OpenLLMetry
pip install agentkernel[crewai,openllmetry]
# Google ADK with OpenLLMetry
pip install agentkernel[adk,openllmetry]
```
### Configuration[](https://kernel.yaala.ai#configuration-1)

#### Method 1: Configuration File[](https://kernel.yaala.ai#method-1-configuration-file-1)

Create or update `config.yaml`:

```
trace:
  enabled: true
  type: openllmetry
```
#### Method 2: Environment Variables[](https://kernel.yaala.ai#method-2-environment-variables-1)

```
export AK_TRACE__ENABLED=true
export AK_TRACE__TYPE=openllmetry
```
### OpenLLMetry Credentials[](https://kernel.yaala.ai#openllmetry-credentials)

Configure Traceloop credentials via environment variables:

```
export TRACELOOP_API_KEY=your-api-key
# Optional: for self-hosted instances
export TRACELOOP_BASE_URL=https://api.traceloop.com
```
Or add them to your `.env` file:

```
TRACELOOP_API_KEY=your-api-key
TRACELOOP_BASE_URL=https://api.traceloop.com
```
### Getting Traceloop Credentials[](https://kernel.yaala.ai#getting-traceloop-credentials)

1. Sign up for an account at [https://www.traceloop.com](https://www.traceloop.com)
2. Create a new project
3. Navigate to **Settings** ��→**API Keys**
4. Copy your API key

For self-hosted deployment or other backends (like Datadog, New Relic, Honeycomb), see the [Traceloop documentation](https://www.traceloop.com/docs/openllmetry/getting-started).

### OpenLLMetry Features[](https://kernel.yaala.ai#openllmetry-features)

OpenLLMetry provides:

- **OpenTelemetry Standards** : Industry-standard telemetry data
- **Multiple Backends** : Send traces to Traceloop, Datadog, New Relic, Honeycomb, and more
- **Automatic Instrumentation** : Zero-code instrumentation for popular LLM frameworks
- **Performance Monitoring** : Track latency, token usage, and costs
- **Distributed Tracing** : Follow requests across multiple services

## What Gets Traced[](https://kernel.yaala.ai#what-gets-traced)

When tracing is enabled, Agent Kernel automatically captures:

### Execution Metrics[](https://kernel.yaala.ai#execution-metrics)

- **Request/Response** : Full input prompts and agent responses
- **Latency** : Execution time for each agent interaction
- **Token Usage** : Input and output tokens consumed

### Agent Context[](https://kernel.yaala.ai#agent-context)

- **Agent Name** : Which agent handled the request
- **Session ID** : Conversation session identifier
- **Metadata** : Custom metadata and tags

### LLM Interactions[](https://kernel.yaala.ai#llm-interactions)

- **Model Calls** : All LLM API calls with parameters
- **Prompt Templates** : Resolved prompts sent to models
- **Completions** : Model responses and reasoning

### Tool Usage[](https://kernel.yaala.ai#tool-usage)

- **Tool Invocations** : Which tools were called
- **Tool Parameters** : Arguments passed to tools
- **Tool Results** : Return values and execution status

## Viewing Traces[](https://kernel.yaala.ai#viewing-traces)

### In Langfuse[](https://kernel.yaala.ai#in-langfuse)

After running your agents with Langfuse tracing enabled:

1. Log in to your Langfuse dashboard
2. Navigate to **Traces**
3. View detailed execution traces including:
  - Full conversation flow
  - LLM calls with prompts and completions
  - Tool invocations
  - Performance metrics
  - Token consumption

**Langfuse Features:**

- **Search and Filter** : Find specific traces by agent, session, or metadata
- **Timeline View** : See execution flow and timing
- **Cost Analysis** : Track token usage and estimated costs
- **Error Tracking** : Debug failed executions
- **Performance Metrics** : Latency analysis and bottleneck identification

### In OpenLLMetry/Traceloop[](https://kernel.yaala.ai#in-openllmetrytraceloop)

After running your agents with OpenLLMetry tracing enabled:

1. Log in to your Traceloop dashboard (or your configured backend)
2. Navigate to **Traces** or**Observability**
3. View detailed execution traces including:
  - Distributed trace timeline
  - LLM API calls with full context
  - Token usage and costs
  - Performance metrics
  - Error details

**OpenLLMetry/Traceloop Features:**

- **OpenTelemetry Standards** : Compatible with any OpenTelemetry backend
- **Multi-Backend Support** : View traces in Traceloop, Datadog, New Relic, etc.
- **Distributed Tracing** : Track requests across multiple services
- **Custom Metrics** : Add custom spans and metrics
- **Real-time Monitoring** : Live trace streaming and alerts

## Troubleshooting[](https://kernel.yaala.ai#troubleshooting)

### Langfuse Issues[](https://kernel.yaala.ai#langfuse-issues)

**Traces Not Appearing:**

1. **Check Credentials** : Verify`LANGFUSE_PUBLIC_KEY` ,`LANGFUSE_SECRET_KEY` , and`LANGFUSE_HOST` are set correctly
2. **Verify Configuration** : Ensure`trace.enabled` is set to`true` and`trace.type` is`langfuse`
3. **Check Installation** : Confirm`agentkernel[langfuse]` is installed
4. **Review Logs** : Look for trace initialization messages in your application logs

**Authentication Errors:**

```
# Verify your Langfuse credentials
python -c "from langfuse import Langfuse; client = Langfuse(); print(client.auth_check())"
```
This should return `True` if credentials are valid.

### OpenLLMetry Issues[](https://kernel.yaala.ai#openllmetry-issues)

**Traces Not Appearing:**

1. **Check Credentials** : Verify`TRACELOOP_API_KEY` is set correctly
2. **Verify Configuration** : Ensure`trace.enabled` is set to`true` and`trace.type` is`openllmetry`
3. **Check Installation** : Confirm`agentkernel[openllmetry]` is installed
4. **Review Logs** : Look for Traceloop initialization messages in your application logs

**Connection Errors:**

```
# Verify your Traceloop setup
python -c "from traceloop.sdk import Traceloop; Traceloop.init(app_name='test'); print('Success')"
```
### Logfire Issues[](https://kernel.yaala.ai#logfire-issues)

**Traces Not Appearing:**

1. **Check Token** : Verify`LOGFIRE_TOKEN` is set — without it, Logfire runs locally and does not ship traces
2. **Verify Configuration** : Ensure`trace.enabled` is`true` and`trace.type` is`logfire`
3. **Check Installation** : Confirm`agentkernel[logfire]` is installed
4. **Review Logs** : Look for the`ak.trace.logfire` "Logfire configured" debug message

**Setup Check:**

```
python -c "import logfire; logfire.configure(send_to_logfire='if-token-present'); print('Success')"
```
### Performance Impact[](https://kernel.yaala.ai#performance-impact)

Tracing adds minimal overhead:

- **Latency** : < 50ms per request
- **Memory** : Negligible (~1-2MB)
- **Network** : Async batched uploads to minimize impact

## Best Practices[](https://kernel.yaala.ai#best-practices)

1. **Enable in All Environments** : Use tracing in development, staging, and production
2. **Set Appropriate TTLs** : Configure data retention in Langfuse settings
3. **Use Tags** : Add meaningful tags for better organization
4. **Monitor Costs** : Track token usage to manage LLM costs
5. **Review Regularly** : Set up alerts for errors and performance degradation

## Privacy and Security[](https://kernel.yaala.ai#privacy-and-security)

### Data Handling[](https://kernel.yaala.ai#data-handling)

When tracing is enabled:

- All prompts and completions are sent to your chosen tracing platform
- **Langfuse** : Data sent to Langfuse cloud or self-hosted instance
- **OpenLLMetry** : Data sent to Traceloop or configured OpenTelemetry backend
- **Logfire** : Data sent to Logfire when`LOGFIRE_TOKEN` is set; otherwise kept local
- Ensure compliance with your data privacy requirements
- Consider self-hosting for sensitive data

### Security Best Practices[](https://kernel.yaala.ai#security-best-practices)

1. **Protect Credentials** : Never commit API keys to version control
2. **Use Environment Variables** : Store credentials securely
3. **Rotate Keys** : Regularly rotate API keys
4. **Network Security** : Use TLS/SSL for all connections (enabled by default)

### Compliance[](https://kernel.yaala.ai#compliance)

For regulated industries:

- Use self-hosted instances within your infrastructure
- Configure appropriate data retention policies
- Implement access controls in your tracing platform
- Review and redact sensitive information before tracing

## Self-Hosting Options[](https://kernel.yaala.ai#self-hosting-options)

### Self-Hosting Langfuse[](https://kernel.yaala.ai#self-hosting-langfuse)

For maximum control and privacy, self-host Langfuse:

1. Follow the [Langfuse self-hosting guide](https://langfuse.com/docs/deployment/self-host)
2. Update your configuration:

```
export LANGFUSE_HOST=https://langfuse.your-domain.com
```
### OpenLLMetry with Custom Backends[](https://kernel.yaala.ai#openllmetry-with-custom-backends)

OpenLLMetry supports multiple backends via OpenTelemetry:

**Datadog:**

```
export TRACELOOP_BASE_URL=https://api.datadoghq.com
export DD_API_KEY=your-datadog-api-key
```
**New Relic:**

```
export TRACELOOP_BASE_URL=https://otlp.nr-data.net
export NEW_RELIC_LICENSE_KEY=your-license-key
```
**Honeycomb:**

```
export TRACELOOP_BASE_URL=https://api.honeycomb.io
export HONEYCOMB_API_KEY=your-api-key
```
**Self-Hosted OpenTelemetry Collector:**

```
export TRACELOOP_BASE_URL=http://your-otel-collector:4318
```
See [OpenLLMetry documentation](https://www.traceloop.com/docs/openllmetry/integrations) for more backend options.

## Getting Started with Pydantic Logfire[](https://kernel.yaala.ai#getting-started-with-pydantic-logfire)

[Pydantic Logfire](https://logfire.pydantic.dev) is an OpenTelemetry-based observability platform from the Pydantic team.

### Installation[](https://kernel.yaala.ai#installation-2)

```
pip install agentkernel[logfire]
```
Or with a framework integration:

```
# OpenAI with Logfire
pip install agentkernel[openai,logfire]
# CrewAI with Logfire
pip install agentkernel[crewai,logfire]
# Google ADK with Logfire
pip install agentkernel[adk,logfire]
```
### Configuration[](https://kernel.yaala.ai#configuration-2)

#### Method 1: Configuration File[](https://kernel.yaala.ai#method-1-configuration-file-2)

```
trace:
  enabled: true
  type: logfire
```
#### Method 2: Environment Variables[](https://kernel.yaala.ai#method-2-environment-variables-2)

```
export AK_TRACE__ENABLED=true
export AK_TRACE__TYPE=logfire
```
### Logfire Credentials[](https://kernel.yaala.ai#logfire-credentials)

Set your Logfire write token via an environment variable:

```
export LOGFIRE_TOKEN=your-write-token
```
Without `LOGFIRE_TOKEN`, Logfire runs locally and does **not** ship traces (Agent Kernel configures it with `send_to_logfire="if-token-present"`), so your agents still run.

### Getting a Logfire Token[](https://kernel.yaala.ai#getting-a-logfire-token)

1. Sign up at [https://logfire.pydantic.dev](https://logfire.pydantic.dev)
2. Create a new project
3. Copy the project's **write token**

### Framework Coverage[](https://kernel.yaala.ai#framework-coverage)

Logfire configures the global OpenTelemetry tracer provider, and each non-streaming agent run (`execution.mode: invoke`) is wrapped in a Logfire span carrying the `session_id`. Streaming runs (`execution.mode: stream`) are not wrapped in a session span — matching the Langfuse and OpenLLMetry runners — though deep instrumentation still emits LLM/tool spans where it is active. Deep (LLM/tool-level) instrumentation depends on the framework:

| Framework | Depth under Logfire | 
|---|---|
| OpenAI Agents SDK | Full — native `logfire.instrument_openai_agents()` | 
| CrewAI | Full — OpenInference CrewAI + LiteLLM instrumentors | 
| Google ADK | Full — OpenInference Google ADK instrumentor | 
| LangGraph | Session span only | 
| Smolagents | Session span only | 

## Integrate with Your Own Traceability Platform[](https://kernel.yaala.ai#integrate-with-your-own-traceability-platform)

Agent Kernel's plugin architecture makes it easy to integrate your own observability platform. If you're already using a different monitoring solution or have specific requirements, you can add support in just a few steps.

### How to Add Your Own Platform[](https://kernel.yaala.ai#how-to-add-your-own-platform)

1. **Create Framework-Specific Runners**

Runner wraps the framework's execution with your tracing logic:

```
from agentkernel.openai.openai import OpenAIRunner
from agentkernel.core import Session
class MyCustomOpenAIRunner(OpenAIRunner):
    def __init__(self, client):
        super().__init__()
        self._client = client
    
    async def run(self, agent, session: Session, prompt):
        # Start a trace span
        with self._client.start_span("agent-execution") as span:
            span.set_attribute("session_id", session.id)
            span.set_attribute("prompt", prompt)
            
            # Run the agent
            result = await super().run(agent=agent, prompt=prompt, session=session)
            
            span.set_attribute("result", result)
            return result
```
1. **Initialize the module with the custom runner**

Initialize the module with your custom runner

```
OpenAIModule([general_agent], runner=MyCustomOpenAIRunner())
```
Custom runner supersedes all other trace configurations

```
export MY_TRACE_API_KEY=your-api-key
```
Your custom observability platform is now integrated with Agent Kernel.

### Example Use Cases[](https://kernel.yaala.ai#example-use-cases)

- **Proprietary Monitoring Systems** : Integrate with your company's internal monitoring tools
- **Compliance Requirements** : Route traces to approved, compliant systems
- **Custom Aggregation** : Combine multiple backends or add custom processing
- **Cost Optimization** : Use cheaper or self-hosted alternatives

The extensible architecture ensures you're never locked into a specific platform.

## Roadmap[](https://kernel.yaala.ai#roadmap)

Upcoming observability features:

- **Custom Spans** : Manual span creation for custom tracking
- **Trace Sampling** : Configurable sampling strategies
- **Metric Exports** : Prometheus and StatsD integrations
- **Real-time Dashboards** : Built-in monitoring dashboards
- **Anomaly Detection** : Automatic detection of unusual patterns
- **Enhanced Correlation** : Better correlation between traces and logs

## Related Resources[](https://kernel.yaala.ai#related-resources)

## Summary[](https://kernel.yaala.ai#summary)

- Enable observability with simple configuration
- **Three Platform Options** : Choose between Langfuse, OpenLLMetry, and Pydantic Logfire
- **Langfuse** : Specialized LLM observability platform with rich analytics
- **OpenLLMetry** : OpenTelemetry-based solution with multi-backend support
- **Pydantic Logfire** : OpenTelemetry-based platform with a native OpenAI Agents SDK integration
- Comprehensive trace data including LLM calls, tools, and performance
- Minimal performance impact
- Self-hosting and custom backend options for data privacy
- Production-ready for all framework integrations (OpenAI, LangGraph, CrewAI, Google ADK)
