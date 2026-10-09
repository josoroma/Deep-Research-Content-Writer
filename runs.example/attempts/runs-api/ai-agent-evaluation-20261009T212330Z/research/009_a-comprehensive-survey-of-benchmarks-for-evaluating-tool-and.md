---
source_id: S-09
url: https://huggingface.co/datasets/tuandunghcmut/BFCL_v4_information/blob/main/A%20Comprehensive%20Survey%20of%20Benchmarks%20for%20Evaluating%20Tool%20and%20Function%20Calling%20in%20Large%20Language%20Models.md
title: A Comprehensive Survey of Benchmarks for Evaluating Tool and Function Calling
  in Large Language Models.md · tuandunghcmut/BFCL_v4_information at main
author: null
published: null
fetched: '2026-10-09T21:23:43Z'
word_count: 4198
---
# A Comprehensive Survey of Benchmarks for Evaluating Tool and Function Calling in Large Language Models.md · tuandunghcmut/BFCL_v4_information at main

# 
**A Comprehensive Survey of Benchmarks for Evaluating Tool and Function Calling in Large Language Models**

In recent years, Large Language Models (LLMs) have undergone a revolutionary transformation. Initially designed and evaluated based on their ability to perform traditional Natural Language Processing (NLP) tasks such as translation, summarization, and question answering, modern LLMs have transcended the boundaries of mere text processing.[25, 26] They are progressively evolving into autonomous agents, capable of interacting with external environments, planning, and executing actions to accomplish complex goals.[25, 27]

The foundation of this transformation is the capability of tool use, also known as function calling. This capability allows LLMs to overcome inherent limitations, such as knowledge cutoffs or the inability to perform real-world actions.[26, 2] For example, an LLM can summarize the content of an email, but it cannot send a reply on its own without access to a mail-sending tool or API.[26] Projects like Gorilla were developed precisely to address this issue, by connecting LLMs to thousands of APIs, enabling them to convert natural language requests into executable API calls that are both syntactically and semantically correct.[28, 29, 30] This marks a fundamental step towards creating AI systems capable of solving practical problems in a meaningful way.

The rise of these agentic capabilities has exposed significant limitations in traditional NLP benchmarks. Benchmarks such as MMLU or HellaSwag, while useful for measuring passive knowledge and language reasoning, are entirely inadequate for evaluating these new competencies.[31, 32] They primarily test a model's ability to generate a correct text response to a known input, within a static and non-interactive environment.[31]

However, tool use is a dynamic, multi-step, and highly interactive process. It requires the model to plan, execute actions, process feedback from the environment, and adjust its strategy.[25, 26, 27] A model that scores highly on a math test might completely fail when asked to chain three consecutive API calls or maintain context over a ten-turn conversation.[5] This difference is not merely an extension of skills but a paradigm shift in the definition of "model performance." Evaluation is no longer just about validating static output ("Is the generated text correct?") but has shifted to validating a dynamic process ("Did the sequence of actions achieve the desired outcome?"). This creates a critical evaluation gap, demanding a new generation of benchmarks.

The rapid development of LLM agents like AutoGPT and AgentGPT has outpaced the development of systematic evaluation methods, leading to a fragmented and often confusing landscape.[25, 33, 34] Researchers and developers lack a standard set of tools to objectively measure and compare the capabilities of different models in their role as agents.[25, 31]

This report aims to address that gap by providing a comprehensive and systematic survey of benchmarks designed to quantitatively evaluate the tool and function calling capabilities of LLMs. Starting from a well-known reference point, the Berkeley Function Calling Leaderboard (BFCL) [3], the report will explore a broader ecosystem of benchmarks, from basic function calling tests to complex, stateful agent evaluations. The goal is to provide a clear analytical framework for understanding, classifying, and comparing these evaluation methods, thereby fostering the development of more robust and reliable AI agents.

To bring clarity to the "fragmented landscape of agent evaluation" [33, 34], a multi-dimensional classification system is necessary. This framework not only helps organize existing benchmarks but also reveals a developmental trajectory of the field, from verifying discrete skills to assessing holistic intelligence.

- **Single-Function / Single-Tool Calling:** This is the most fundamental level, testing the model's ability to correctly invoke a single, specified function. Tests focus on generating the correct function name and required parameters.[14, 33]
- **Multi-Function / Multi-Tool Calling:** These scenarios require more complex decision-making. The model may have to select the most appropriate tool from an available set [14, 35] or orchestrate calls to various tools to fulfill a single user request.[26, 36]
- **Sequential & Parallel Calling:** Tasks may require a linear sequence of calls, where the output of one tool is the input for the next. Conversely, some tasks allow for independent function calls to be executed in parallel for efficiency.[18, 14]
- **Agentic Planning & Reasoning:** This is the highest level of complexity, requiring multi-hop reasoning, long-term planning, and decision-making in open-ended environments. The solution path is not predetermined, and the agent must discover and construct it on its own.[25, 27, 37]

- **Stateless / Single-Turn Evaluation:** Each task is treated as an independent, isolated event. The agent has no memory of past interactions. This design simplifies evaluation, increases speed, and ensures reproducibility, but lacks realism.[38, 39] Most early function calling benchmarks fall into this category.[40, 41]
- **Stateful / Multi-Turn / Conversational Evaluation:** The agent must maintain context across multiple conversational turns. Its actions can modify a persistent environmental state, and future actions depend on this modified state.[38, 39, 10, 42] This is crucial for simulating realistic user interactions and complex workflows but also poses significant evaluation challenges.[38, 40, 42, 43]

- **Syntactic and Structural Matching (e.g., AST):** Evaluation is based on comparing the structure of the generated code or function call against a ground truth reference, often using an Abstract Syntax Tree (AST). This method is fast and scalable but may penalize functionally equivalent but syntactically different solutions.[18, 8]
- **Execution-Based Validation:** The generated tool call is executed in a real or sandboxed environment, and the result is checked for correctness. This method is more robust than AST but can be slow, costly, and non-deterministic with live APIs.[18, 3]
- **Outcome-Centric Evaluation:** Focuses solely on the final state of the environment or the final answer provided by the agent, regardless of the specific path taken to achieve it. This allows for flexibility in the agent's strategy but requires clear and unambiguous ground truth outcomes.[15, 26]
- **LLM-as-a-Judge:** Uses a powerful LLM (often GPT-4 or its successors) to score or compare the outputs of the model under test. This method is highly scalable for open-ended tasks but comes with its own biases and reliability issues.[44, 37, 45]

This taxonomy reveals a clear evolution in the field. The earliest and simplest benchmarks focused on stateless, single-function tasks evaluated by syntactic matching. The primary question was: "Did the model generate the correct syntax for the call?". The next generation of benchmarks expanded to multi-tool scenarios and execution-based validation, asking: "Can the model choose the right tool and execute it successfully?". Finally, the most advanced benchmarks today push the boundaries into stateful interactions and agentic reasoning, using outcome-centric or LLM-as-a-Judge methods. The question now is: "Can the model behave as a competent agent to achieve a complex goal in a dynamic environment?". This progression reflects the field's ambition, moving from verifying discrete skills to assessing holistic intelligence.

The benchmarks in this section form the foundational layer of tool use evaluation. They focus primarily on correctness, scalability, and stateless interaction scenarios, laying the groundwork for more complex agentic assessments.

- **Objective & Motivation:** BFCL was created to provide a public and comprehensive "obstacle course" to evaluate the core ability of LLMs to call external functions in a variety of realistic contexts.[18, 3]
- **Evolution & Scope:** The benchmark has evolved through multiple versions, each introducing increasingly complex scenarios:
  - **v1:** Introduced the Abstract Syntax Tree (AST) based evaluation method to ensure scalability and reliability.[18, 8]
  - **v2:** Expanded the dataset with functions contributed by enterprises and the open-source community.[8]
  - **v3:** Introduced multi-step and multi-turn interactions, moving beyond single-turn scenarios. Tasks included handling missing parameters, missing functions, and long-context inputs.[14, 8]
  - **v4:** Shifted towards "holistic agentic evaluation," assessing the ability to reason and decide not to act in stateful settings.[18, 8]
- **Dataset & Task Types:** BFCL covers a wide range of call types (simple, multiple-function, parallel, parallel-multiple) and supports multiple languages (Python, Java, JavaScript, REST API, SQL).[17, 14] It also includes "relevance detection" tasks to test if a model correctly refrains from tool calling when inappropriate.[17, 14]
- **Evaluation Methodology:** BFCL employs a dual approach: an AST-based method for scalable checking without execution, and direct execution-based validation for live APIs.[18, 8]

- **Objective & Motivation:** ToolBench was created to close the performance gap between closed-source and open-source LLMs in tool manipulation, while enabling training and evaluation on an unprecedented scale.[36, 46]
- **Dataset & Scope:** ToolBench's defining feature is its massive scale, encompassing over 16,000 real-world APIs and 3,451 tools across 49 categories, all sourced from RapidAPI.[36, 47] The dataset contains over 126,000 instruction-solution path pairs.[36, 47]
- **Methodology (DFSDT):** A key innovation of ToolBench is its use of a Depth-First Search-based Decision Tree (DFSDT) powered by an LLM to automatically generate complex, multi-step solution paths. This method allows for exploration and backtracking, enabling the efficient annotation of tasks too complex for simpler methods like Chain-of-Thought.[36, 47]
- **Evaluation System (ToolEval):** ToolEval is the automated evaluator for ToolBench. It uses an LLM-as-a-Judge (ChatGPT) to assess performance based on two key metrics:**Pass Rate** (successful task completion) and**Win Rate** (pairwise comparison against a reference model).[45, 47] The reliability of this evaluator was validated against human annotators, showing high agreement.[45]

- **Objective & Motivation:** API-Bank was designed to answer three core research questions: (1) How effective are current LLMs at tool use? (2) How can this capability be enhanced? (3) What are the key obstacles?.[2, 35, 20]
- **Dataset & Structure:** API-Bank has a unique structure with separate datasets for evaluation and training:
  - **Evaluation Set:** A smaller, manually annotated set of 314 dialogues with 753 API calls across 73 tools, designed for rigorous, executable evaluation.[2, 35, 20]
  - **Training Set:** A much larger set of 1,888 dialogues across 2,138 APIs and 1,000 domains, generated automatically using a multi-agent LLM process to reduce annotation costs by 98%.[35, 20]
- **Evaluation Focus:** API-Bank explicitly dissects the tool-use process into three core capabilities:**Planning** (determining the sequence of calls),**Retrieving** (selecting the correct API from a large pool), and**Calling** (generating the correct parameters).[2, 35, 19] The benchmark's difficulty is structured along these dimensions (e.g., few vs. many APIs, single vs. multiple calls) to isolate and test each capability.[35]

These foundational benchmarks represent a fundamental trade-off in evaluation design: between realism and reproducibility. ToolBench aims for maximum realism by using thousands of live APIs from RapidAPI, offering real-world diversity and complexity.[36] However, live APIs can change, become unavailable, or return different data, making it difficult to reproduce experiments. The ToolBench project itself acknowledged this challenge by introducing "StableToolBench," a version that uses simulated API responses to increase stability.[47] In contrast, BFCL and API-Bank use more tightly curated sets of tools/APIs, offering greater control and reproducibility at the cost of ToolBench's scale and diversity.[18, 2] This reveals a core trade-off: prioritizing the unpredictable realism of the live web or the controlled, reproducible environment of a scientific experiment.

Moving beyond testing the correctness of individual function calls, these advanced benchmarks are designed to evaluate the holistic capabilities of an agent, including planning, reasoning, and state management in complex, interactive environments.

- **Objective & Motivation:** AgentBench was the first systematic benchmark designed to quantitatively evaluate the reasoning and decision-making abilities of LLMs as autonomous agents in challenging interactive environments.[25, 27]
- **Dataset & Environments:** The hallmark of AgentBench is its 8 distinct environments, designed to test a range of core capabilities [48, 25, 24]:
  - **Computer Operation:** Interacting with an Operating System (OS) and querying a Database (DB).[48, 24]
  - **Information Seeking:** Traversing a Knowledge Graph (KG), Web Shopping, and Web Browsing.[48, 24]
  - **Real-Life Scenarios:** House-Holding (based on ALFWorld), Digital Card Games, and Lateral Thinking Puzzles.[48]
- **Task Design:** Tasks in AgentBench are multi-turn and open-ended, requiring 5 to 50 steps to solve. This is intended to explicitly test long-term reasoning and instruction following—identified as key obstacles for current agents.[48, 25, 27] The latest version uses a function calling format and containerized deployment to enhance reproducibility.[24]

- **Objective & Motivation:** ToolSandbox was created to address the limitations of previous benchmarks, which focused on stateless RESTful APIs or single-turn requests.[40, 41, 10] It is specifically designed to evaluate agents in**stateful** , conversational, and interactive contexts.[10, 42]
- **Core Concept (Statefulness):** The ToolSandbox environment has a persistent "world state" (e.g., databases for contacts, messages, settings) that tools can modify.[42] This creates implicit dependencies between tools (e.g., an agent must turn on Wi-Fi before it can send a message), forcing the agent to reason about the state of the world.[40, 42]
- **Evaluation Methodology (Milestone DAG):** Instead of just checking the final outcome, ToolSandbox uses a "Milestone Directed Acyclic Graph" (DAG). This structure defines critical intermediate states that an agent must achieve in a specific order to complete the task.[42, 43] The evaluation involves matching the agent's action trajectory against this DAG, allowing for flexible solution paths while still ensuring key steps are taken.[42]
- **Task Types:** Includes challenging scenarios like State Dependency, Canonicalization (e.g., converting "this Friday" to a specific date), and Insufficient Information to test agent robustness and reasoning.[41, 10, 42]

- **Objective & Motivation:** To evaluate agent performance within a standardized tool interaction protocol—the Model Context Protocol (MCP). This aims to solve the problem of tool fragmentation and create a benchmark that measures realistic, multi-step, multi-server workflows.[15, 44, 37, 21]
- **The MCP Ecosystem:** This benchmark is built on a testbed of dozens of live, MCP-compliant servers providing hundreds of tools across diverse domains like finance, scientific computing, and academic search.[15, 44, 37] This allows for complex tasks involving both intra-server (tools designed to work together) and inter-server orchestration.[37]
- **Task Design:** Tasks are synthetically generated to be complex, requiring multi-step planning, tool retrieval from ambiguous instructions, and grounding responses in intermediate tool results.[37] The dataset includes 600 queries across 6 categories of increasing complexity.[15, 44]
- **Evaluation Framework (MCP-Eval):** MCP-AgentBench uses a two-tier evaluation framework: (1) rule-based checks to verify execution correctness (validity, schema compliance) and (2) a rubric-driven, outcome-focused LLM-as-a-Judge (MCP-Eval) to assess task completion and strategic reasoning.[15, 44, 37]

A key insight revealed by these benchmarks is that an LLM's performance is no longer solely dependent on the base model itself. It is also heavily dependent on the "agent architecture" or prompting strategy used to elicit its agentic behavior. For example, the MCP-Universe leaderboard explicitly separates results for models using "ReAct" versus "FC" (Function Calling), and the same base model can have dramatically different success rates depending on the strategy.[46] Similarly, the ToolBench leaderboard shows large performance differences for the same model when using the "ReAct" versus "DFSDT" method.[47] This implies that when we evaluate an "agent," we are evaluating a *system* comprising the LLM and the agentic framework. This complicates direct model-to-model comparisons and suggests that future research must focus on developing better agent architectures as much as on training larger base models.

This section synthesizes findings from the discussed benchmarks to provide a holistic view of the performance of modern large language models in tool use and agentic behavior. A comparative analysis reveals that tool-use capability and agentic reasoning are distinct competencies, and a model can excel at one while faltering at the other.

To provide a clear overview, the table below summarizes the key characteristics of the analyzed benchmarks.

**Table 1: Comparative Overview of Major Tool-Use Benchmarks**

| Benchmark | Primary Objective | # of Tools/APIs | Task Complexity | Statefulness | Primary Evaluation Method | Key Differentiator | 
|---|---|---|---|---|---|---|
| **BFCL** | Evaluate core function calling accuracy and scalability. | ~1,200+ | Single/Multi-step, Sequential/Parallel | Mostly stateless (v4 has agentic elements) | AST, Execution | Scalable AST-based evaluation; diverse language coverage (Python, Java, SQL, etc.). | 
| **ToolBench** | Train and evaluate LLMs on a massive set of real-world APIs. | 3,451 tools, 16,464 APIs | Multi-step, Multi-tool | Stateless | LLM-as-a-Judge (ToolEval) | Massive scale of APIs from RapidAPI; automated data generation with DFSDT. | 
| **API-Bank** | Dissect tool-use capabilities into Planning, Retrieving, and Calling. | 2,138 APIs (train), 73 APIs (eval) | Single/Multi-step | Stateless | Execution | Separate training and evaluation sets; focus on analyzing sub-skills. | 
| **AgentBench** | Evaluate LLMs as agents in diverse interactive environments. | Environment-dependent | Multi-step, open-ended (5-50 steps) | Stateful (within each environment) | Outcome-based per environment | 8 diverse environments (OS, DB, Web, Game, etc.) to test general reasoning. | 
| **ToolSandbox** | Evaluate agents in stateful, conversational interactions. | 34 | Multi-step, Multi-turn | Highly stateful (persistent world state) | Milestone DAG | Focus on implicit state dependencies; flexible milestone-based evaluation. | 
| **MCP-AgentBench** | Evaluate agents in a standardized tool ecosystem (MCP). | ~188-250 tools | Multi-step, Multi-server | Stateless (initial version) | Two-tier: Rule-based & LLM-as-a-Judge (MCP-Eval) | Interaction with live MCP servers; emphasis on cross-domain orchestration. | 

Data from the leaderboards reveals a complex performance picture, with different models showing strengths in different types of tasks.

- Foundational Function Calling Performance (Stateless):
On benchmarks like BFCL and ToolEval, top models demonstrate high technical proficiency in generating correct function calls. Data from September 2024 shows Claude 3.5 Sonnet leading on BFCL with 90.20%, followed by Claude 3 Opus at 88.40% and GPT-4o at 83.59% . On ToolEval, GPT-4 (using DFSDT) achieves a 71.1% Pass Rate and a 70.4% Win Rate, indicating superior planning ability.[49] Open-source models like ToolLLaMA also show competitive results, especially when paired with powerful agentic frameworks.[49]

**Table 2: Performance on Foundational (Stateless) Function Calling Benchmarks**

| Model | BFCL Score (%) | ToolEval Pass Rate (DFSDT) (%) | ToolEval Win Rate (DFSDT) (%) | 
|---|---|---|---|
| **GPT-4o** | 83.59 | No data | No data | 
| **Claude 3 Opus** | 88.40 | No data | No data | 
| **Claude 3.5 Sonnet** | 90.20 | No data | No data | 
| **GPT-4** | No data | 71.1 | 70.4 | 
| **ToolLLaMA** | No data | 66.7 | 60.0 | 

- Agentic Performance (Stateful and Complex):
When moving to more complex agentic benchmarks, model performance becomes more stratified. On AgentBench, top commercial models like GPT-4 (score of 82.38 on v0.2) significantly outperform open-source competitors, highlighting the challenge of long-horizon reasoning.[25, 27, 24] In the MCP ecosystem, even the most advanced models struggle. On MCP-Atlas, GPT-5 leads with a 44.5% pass rate, followed by Claude Opus 4.1 at 40.9%, but GPT-4o performs surprisingly poorly at just 7.2%.[50] Interestingly, on MCP-AgentBench, open-source models like Qwen3-235B have shown the ability to outperform proprietary systems like GPT-4o in certain configurations.[15]

**Table 3: Performance on Advanced Agentic Benchmarks**

| Model | AgentBench Score (FC) | MCP-Atlas Pass Rate (%) | MCP-Universe Success Rate (%) | 
|---|---|---|---|
| **GPT-5** | No data | 44.50 | 44.16 | 
| **GPT-4o** | No data | 7.20 | No data | 
| **GPT-4** | 59.2 | No data | No data | 
| **Claude Opus 4.1** | No data | 40.90 | 29.44 | 
| **Claude 4.5 Sonnet** | No data | No data | 35.06 | 
| **Qwen3-235B** | No data | 12.00 | No data | 

The stark difference in performance of the same model across different benchmark types reveals a critical insight: "tool use" and "agentic reasoning" are distinct, hierarchical capabilities. A high score on a foundational benchmark like BFCL does not guarantee high performance on an agentic benchmark like MCP-Atlas. For example, GPT-4o scores 83.59% on BFCL, indicating very good basic function calling ability . However, on MCP-Atlas, its performance plummets to just 7.2%.[50] This divergence demonstrates that BFCL primarily tests the *mechanics* of tool use (syntax, parameter matching), whereas MCP-Atlas tests the *strategy* of tool use (planning, reasoning, adapting to results over multiple steps). A model can master the mechanics without mastering the strategy. This has major implications for interpreting leaderboards and selecting models for complex agentic applications.

While the array of benchmarks has driven significant progress, their underlying methodologies also have inherent limitations and challenges. Understanding these weaknesses is crucial for interpreting results correctly and for guiding future research.

- **Benefits:** The "LLM-as-a-Judge" paradigm offers a scalable and low-cost alternative to human evaluation, especially for complex, open-ended tasks where rule-based metrics fall short.[51, 52] Benchmarks like ToolEval and MCP-Eval rely on it for this reason.[44, 45] In some contexts, it has been reported to have high correlation with human judgment.[52]
- **Critiques and Challenges:** However, the method faces serious reliability and bias issues:
  - **Inherent Biases:** LLM Judges are susceptible to multiple biases that distort evaluations. Common biases include**Position Bias** (favoring the first or last answer) [22, 23],**Verbosity/Length Bias** (favoring longer answers regardless of correctness) [52, 22, 53], and**Self-Enhancement Bias** (favoring outputs stylistically similar to its own).[54, 55]
  - **Reliability & Consistency:** LLM evaluations are stochastic and can be inconsistent, even with the same input.[22, 11] Their decisions are often uninterpretable ("black-box") and highly dependent on the prompt design and the quality of the Judge model itself.[22, 6]
  - **Alignment with Human Judgment:** While sometimes high, this alignment can weaken significantly for difficult or nuanced tasks like reasoning and programming, where Judges may mark incorrect answers as correct.[22, 13, 56] They also struggle when they cannot answer the question themselves and are not provided with a high-quality reference answer.[56]
  - **Overconfidence:** A core issue is the "Overconfidence Phenomenon," where the confidence a Judge predicts in its evaluation is significantly higher than its actual accuracy, eroding trust.[55]

- **Advantages of Stateless:** Stateless agents are simpler in design, faster, more scalable, and easier to test because each interaction is independent and predictable.[38, 39] This makes for highly reproducible benchmarks.
- **Limitations of Stateless:** They lack personalization and cannot handle multi-turn conversations or complex workflows, often forcing users to repeat information.[38, 39] They fail to capture important real-world phenomena like context drift .
- **Advantages of Stateful:** Stateful agents enable personalized, contextual experiences and can engage in seamless multi-turn conversations, improving decision-making over time.[38, 39] This is essential for simulating real-world agent behavior.
- **Challenges of Stateful:** They are more complex to design and evaluate. The vast number of possible trajectories makes it difficult to define a single "correct" path, requiring novel evaluation methods like ToolSandbox's Milestone DAG.[42, 43]

A core paradox of evaluation is emerging from these analyses. The field is moving towards more realistic, stateful, and open-ended agentic benchmarks. However, these are precisely the types of benchmarks that are most difficult to evaluate with deterministic, rule-based methods. This forces benchmark designers to rely on the LLM-as-a-Judge paradigm, a method we have identified as being fraught with reliability and bias issues, especially for complex reasoning tasks.[13, 56] We are therefore facing a paradoxical situation: the more realistic and challenging our benchmarks become, the less reliable our methods for evaluating them become. The very tool we are using to measure progress (the LLM Judge) is a product of the technology we are trying to measure, and it suffers from the same fundamental flaws. This is a fundamental, recursive problem for the field and a critical area for future research.

As the capabilities of LLM agents continue to advance, evaluation methodologies must also evolve to keep pace. Current research has pointed to several critical directions and "blind spots" that need to be addressed to build a more comprehensive and trustworthy evaluation ecosystem.

Most current benchmarks focus on evaluating a single agent operating in isolation. This approach overlooks the complex dynamics that arise when multiple agents interact.[57, 5] Future research needs to develop benchmarks like **MultiAgentBench**, designed to measure aspects such as coordination, cooperation, and competition in multi-agent environments. Evaluating how agents communicate, negotiate, and resolve conflicts will be crucial for building complex AI systems capable of operating in social or economic ecosystems.

Recent surveys have pointed out critical gaps in current evaluation practices, especially those related to real-world deployment feasibility.[58]

- **Cost-Efficiency:** Most benchmarks prioritize capability over efficiency, ignoring resource consumption factors like token usage, API call costs, and inference time. Future evaluation frameworks must integrate cost as a core metric to assess deployment viability.[58]
- **Safety, Robustness, and Compliance:** There is a significant lack of focus on safety, reliability, and policy adherence.[58] Future benchmarks need to test for resilience against adversarial inputs, bias mitigation, and compliance with organizational and societal policies.[59, 58]

As agents move from research to production, evaluation must account for real-world business constraints that are often overlooked.[34]

- **Secure Access & RBAC:** Enterprise agents must operate within the confines of Role-Based Access Control (RBAC), a challenge not present in most open benchmarks.[34]
- **Long-Horizon & Dynamic Interactions:** Evaluation needs to move beyond short, episodic tasks to assess performance in long-running operations in dynamic environments, measuring phenomena like context decay and performance drift over time.[34, 60]

- **Driving Granular Evaluation:** There is a need to move beyond simple pass/fail metrics to action-level or step-level evaluation, which provides more detailed diagnostics of agent failures.[58, 61] T-Eval's decomposition of tool use into sub-processes (planning, retrieval, etc.) is a step in the right direction.[61]
- **Scaling and Automating Evaluation:** The reliance on static, manually annotated datasets is a bottleneck. Future directions include synthetic data generation and the development of more robust, less biased "Agent-as-a-Judge" systems.[58]

These directions signal a maturation of the field. The key research question is slowly shifting from a purely technical one ("Can we build an agent that completes the task?") to a more complex socio-technical and economic one ("Can we build an agent that completes the task *safely*, *affordably*, *reliably*, and *in compliance with our rules*?"). This shift suggests that the next generation of "state-of-the-art" agents will be defined not just by raw performance, but by a balanced scorecard that includes these real-world constraints. This is a profound change in how the AI community will define and measure success.
