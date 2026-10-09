---
source_id: S-18
url: https://library.eval-ai.com/agent-metrics
title: Overview — Eval AI Library — Documentation
author: Aleksandr Meshkov
published: null
fetched: '2026-10-09T21:41:48Z'
word_count: 348
---
# Overview — Eval AI Library — Documentation

# Agent Metrics[¶](https://library.eval-ai.com#agent-metrics)

 Eval AI Library provides specialized metrics for evaluating AI agents — systems that use tools, maintain conversations, and complete tasks autonomously.

Unlike RAG metrics that focus on answer quality, agent metrics evaluate **behavioral properties**: Did the agent call the right tools? Did it complete the user's task? Does it actually give the user what they wanted? Does the dialogue flow naturally? Does the agent get stuck in loops? How does it behave when it doesn't know the answer?

## Available Metrics[¶](https://library.eval-ai.com#available-metrics)

 | Metric | What It Measures | LLM Calls | Default Threshold | 
|---|---|---|---|
| [Tool Correctness](https://library.eval-ai.com/tool-correctness/) | Whether correct tools were called | 0 | 0.5 | 
| [Task Success Rate](https://library.eval-ai.com/task-success/) | Whether the user's goal was achieved (checklist lens) | 2–4 | 0.7 | 
| [Goal Achievement Rate](https://library.eval-ai.com/goal-achievement/) | Whether the user actually got what they wanted (outcome lens) | 3–4 | 0.7 | 
| [Conversational Flow Rate](https://library.eval-ai.com/conversational-flow/) | How natural and coherent the dialogue is | 1 | 0.7 | 
| [Repetitive Pattern Detection](https://library.eval-ai.com/repetitive-pattern/) | Whether the agent gets stuck in loops | 1 | 0.7 | 
| [Failure Rate](https://library.eval-ai.com/failure-rate/) | How the agent handles uncertainty (honest fallback vs hallucination) | 1 | 0.7 | 
| [Role Adherence](https://library.eval-ai.com/role-adherence/) | How well the AI maintains its role | 2 | 0.7 | 
| [Knowledge Retention](https://library.eval-ai.com/knowledge-retention/) | How well context is remembered across turns | 2 | 0.7 | 
| [Tool Error Detection](https://library.eval-ai.com/tool-errors/) | Errors in tool/function usage | 1 | 0.7 | 

## Test Cases for Agents[¶](https://library.eval-ai.com#test-cases-for-agents)

 ### Single-Turn (Tool Use)[¶](https://library.eval-ai.com#single-turn-tool-use)

 ### Multi-Turn (Conversation)[¶](https://library.eval-ai.com#multi-turn-conversation)

 ## Choosing Metrics[¶](https://library.eval-ai.com#choosing-metrics)

 The right combination of metrics depends on your agent's architecture:

- **Tool-using agents** (API calls, function calling) — focus on Tool Correctness and Tool Error Detection to ensure the agent picks the right tools and uses them correctly.
- **Conversational assistants** (customer support, advisors) — use Task Success, Role Adherence, and Knowledge Retention to verify the agent helps users effectively while staying in character.
- **Complex agents with tools + conversation** — combine all metrics for comprehensive evaluation.

| Scenario | Recommended Metrics | 
|---|---|
| Tool-using agents | Tool Correctness + Tool Error Detection + Repetitive Pattern Detection | 
| Conversational assistants | Task Success + Goal Achievement + Role Adherence + Knowledge Retention | 
| Dialogue quality audits | Conversational Flow + Repetitive Pattern Detection | 
| Safety-critical / knowledge-heavy agents | Failure Rate + Goal Achievement Rate | 
| Multi-turn agents with tools | All agent metrics | 
| Task completion evaluation | Task Success Rate (with `task_description` +`success_criteria` for deterministic grading) | 

## Quick Example[¶](https://library.eval-ai.com#quick-example)
