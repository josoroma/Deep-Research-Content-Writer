---
source_id: S-07
url: https://www.cos.io/blog/benchmarking-llm-agents-on-scientific-tasks-introducing-replicatorbench
title: 'Benchmarking LLM Agents on Scientific Tasks: Introducing ReplicatorBench'
author: Center for Open Science
published: null
fetched: '2026-10-09T21:23:42Z'
word_count: 718
---
# Benchmarking LLM Agents on Scientific Tasks: Introducing ReplicatorBench

Last fall, COS [announced a new initiative](https://www.cos.io/blog/from-open-science-to-ai-benchmarking-llms-on-reproducibility-robustness-and-replication) to systematically evaluate how well large language model (LLM) agents can perform and reason through the scientific research lifecycle. 

The first active phase of this work has produced ReplicatorBench, a benchmark for evaluating LLM agents on research replication in the social and behavioral sciences.

**About the Project**

[Benchmarking LLM Agents on Scientific Tasks](https://www.cos.io/benchmarking-llm-agents-on-scientific-tasks) is a multi-year, multi-team effort led by COS with support from Coefficient Giving and in collaboration with researchers at Pennsylvania State University, Old Dominion University, and the University of Notre Dame. Each partner contributes to different dimensions of the framework, including task design, agent development, evaluation methods, and theoretical modeling of AI scientific behavior. The project evaluates LLM agents across three researcher personas—Replicator, Peer Reviewer, and Discovery Scientist—mapped onto various stages of the research lifecycle to create a scalable framework for benchmarking AI in scientific contexts.

**What ReplicatorBench Does**

What sets ReplicatorBench apart from prior work is its focus on the full replication process, not just the final outcome. Most existing benchmarks evaluate whether an agent arrives at the right answer—but science is not just about outcomes. ReplicatorBench requires agents to first preregister their replication plan, then execute their analysis according to that plan, mirroring the standards of rigorous human research.

The benchmark assesses agents across three stages: extracting and retrieving the right information, designing and executing the analysis, and interpreting results against the original claims. It also includes both replicable and non-replicable studies, so agents must demonstrate they can recognize when a result does not hold, not just reproduce one that does. Agents are evaluated on the accuracy of their outputs, reasoning, adherence to their preregistered plan, and ability to handle ambiguity and missing information.

The resulting paper, *ReplicatorBench: Benchmarking LLM Agents for Replicability in Social and Behavioral Sciences*, has been accepted to the inaugural AI for Sciences track at the Knowledge Discovery and Data Mining (KDD) 2026 conference (August 9–13, Jeju, Korea) and is currently in production. A preprint is available on [arXiv](https://arxiv.org/abs/2602.11354). All code and data are publicly available.

ReplicatorBench has also been accepted into the [Holistic Agent Leaderboard](https://hal.cs.princeton.edu/) (HAL), a rigorous evaluation infrastructure developed at Princeton to address inconsistencies in how benchmarks and agents are assessed across the field. HAL maintains a curated set of benchmarks vetted for methodological quality and does not automatically include submissions. Acceptance means ReplicatorBench is now part of HAL's cost-controlled, standardized evaluation harness, and is among the active infrastructure that AI developers and researchers use to test and compare their agents. The benchmark will continue generating new data on model capabilities as the field evolves, rather than becoming a static, one-time project.

**Current Focus: Robustness**

Building on ReplicatorBench, the team is now developing a Robustness benchmark. Replication asks whether a result holds when tested with new data—but a separate, and equally important, question is whether results hold when the same data are analyzed in different, equally justifiable ways. Researchers routinely face genuine degrees of freedom in how they operationalize variables, preprocess data, and select analytical approaches, and reasonable choices at each of these decision points can lead to meaningfully different conclusions.

The Robustness benchmark evaluates whether LLM agents navigate this analytical landscape in ways that are consistent, justified, and transparent. Results and protocols will be released openly as the benchmark matures.

**What’s Next**

Subsequent phases will extend the framework to Peer Reviewer and Discovery Scientist benchmarks, building toward a continuous, community-driven infrastructure for testing AI capabilities and limitations as a scientific collaborator. Opportunities for collaboration, including contributing annotations, evaluation rubrics, or replication studies, are welcome.

Researchers and organizations interested in learning more or getting involved can contact Tim Errington ([tim@cos.io](mailto:tim@cos.io)) or Shakhlo Nematova ([shakhlo@cos.io](mailto:shakhlo@cos.io)). For more information about Benchmarking LLM Agents on Scientific Tasks, visit the [project webpage](https://www.cos.io/benchmarking-llm-agents-on-scientific-tasks).

**Responsible stewards of your support**

COS has earned top recognition from **[Charity Navigator](https://www.charitynavigator.org/ein/461496217)** and **[Candid](https://www.guidestar.org/profile/46-1496217)** (formerly GuideStar) for our financial transparency and accountability to our mission. COS and the OSF were also awarded SOC2 accreditation in 2023 after an independent assessment of our security and procedures by the **[American Institute of CPAs (AICPA)](https://www.aicpa-cima.com/resources/landing/system-and-organization-controls-soc-suite-of-services)**.

We invite all of our sponsors, partners, and members of the community to learn more about how our organization operates, our impact, our financial performance, and our nonprofit status.
