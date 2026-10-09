---
source_id: S-17
url: https://pedropizarrodiaz.it/blog/ai-agent-metrics-before-production.html
title: AI Agent Metrics to Define Before You Build | Pedro Pizarro
author: Pedro Pizarro Diaz
published: '2026-08-29'
fetched: '2026-10-09T21:41:43Z'
word_count: 524
---
# AI Agent Metrics to Define Before You Build | Pedro Pizarro

**Follow this publication in Google.**Select this site to see more of its articles in eligible Google news and AI surfaces.

This article expands an edition of [The Chill AI guy on LinkedIn](https://www.linkedin.com/pulse/before-you-build-another-agent-decide-what-youll-pedro-pizarro-diaz-ra4qf).

## Start with the decision, not the dashboard

Agent teams often choose metrics after the system exists. They instrument latency, count successful calls and add an evaluation score, then try to infer whether the investment is working.

The sequence should run the other way. First decide which production decision the evidence must support: release, expand, constrain, redesign or stop. Then define the minimum measures needed to make that choice.

## Level 1: does it run?

The first layer describes technical operation. Useful measures include latency at a stated percentile, cost per attempted task, availability and the rate of tool, integration or model errors.

These measures expose instability and cost growth. They do not show whether the agent completed the work correctly.

A system can be fast, cheap and wrong. That is why an aggregate success response from an API is not a task-success metric.

## Level 2: does it do the work?

This layer follows the workflow. Measure task completion against a defined acceptance condition, rework required from a person, tool-use accuracy and the rate of cases that need escalation.

The denominator matters. Task success should refer to a clear set of eligible cases, not only the clean cases the agent chose to complete.

Review effort also belongs here. If a person must reconstruct the source and repeat the work for every output, the agent may pass a quality check while failing the operating model.

## Level 3: is it worth operating?

The third layer connects performance to value and risk. It can include cost per successful task, cycle-time change, unsupported claim rate, unauthorised action rate and the effect on the decision the workflow exists to make.

These measures should keep benefits and controls visible at the same time. An agent that reduces handling time by taking actions outside its permission boundary has not created an acceptable result.

The right threshold depends on the workflow, impact and review model. A suggested number in a workshop is a hypothesis, not evidence.

## A compact metric contract

For each metric, record its definition, denominator, data source, collection period and decision owner. Also state which decision the metric can authorise and which conclusion it cannot support.

- **Name:** use a label that describes the observable behaviour.
- **Definition:** specify what counts and what does not.
- **Evidence:** identify the event, review record or test result retained.
- **Owner:** name who reviews the result and can act on it.
- **Decision:** connect the measure to release, expansion, iteration or stop.
- **Limit:** state what the number cannot prove.

This is deliberately small. A metric becomes useful when it changes a decision, not when it fills a dashboard.

## Use all three levels together

Level 1 tells you whether the system is stable. Level 2 tells you whether the workflow receives usable work. Level 3 tells you whether the result is valuable and acceptable.

Removing any layer creates a blind spot. The measurement plan is part of the product and governance design, so it belongs before the build.
