---
source_id: S-26
url: https://arxiv.org/html/2603.18196v2
title: Retrieval-Augmented LLMs for Security Incident Analysis
author: Xavier Cadet Affiliation Dartmouth College
published: null
fetched: '2026-10-09T20:54:02Z'
word_count: 9119
---
# Retrieval-Augmented LLMs for Security Incident Analysis

###### Abstract.

Investigating cybersecurity incidents requires collecting and analyzing evidence from multiple log sources, including intrusion detection alerts, network traffic records, and authentication events. This process is labor-intensive: analysts must sift through large volumes of data to identify relevant indicators and piece together what happened. We present a RAG-based system that performs security incident analysis through targeted query-based filtering and LLM semantic reasoning. The system uses a query library with associated MITRE ATT&CK techniques to extract indicators from raw logs, then retrieves relevant context to answer forensic questions and reconstruct attack sequences. We evaluate the system with five LLM providers on malware traffic incidents and multi-stage Active Directory attacks. We find that LLM models have different performance and tradeoffs, with Claude Sonnet 4 and DeepSeek V3 achieving 100% recall across all four malware scenarios, while DeepSeek costs 15 less ($0.008 vs. $0.12 per analysis). Attack step detection on Active Directory scenarios reaches 100% precision and 82% recall. Ablation studies confirm that a RAG architecture is essential: LLM baselines without RAG-enhanced context correctly identify victim hosts but miss all attack infrastructure including malicious domains and command-and-control servers. These results demonstrate that combining targeted query-based filtering with RAG-based retrieval enables accurate, cost-effective security analysis within LLM context limits.

###### Keywords:

network security, incident analysis, retrieval-augmented generation, large language models, log analysis
## 1. Introduction

Security Operations Centers operate under increasing pressure: cyber threats grow in both volume and complexity, yet the analyst workforce has not kept pace. Modern Security Information and Event Management (SIEM) deployments routinely generate thousands of alerts per day, but empirical studies show analysts can only examine a small subset, resulting in fatigue and overlooked incidents ([Singh et al., 2025](https://arxiv.org#bib.bib15); [Kersten et al., 2023](https://arxiv.org#bib.bib23); [Tariq et al., 2025](https://arxiv.org#bib.bib24)). Investigating a security incident (identifying compromised assets, tracing attacker actions, understanding intrusion mechanisms) demands synthesis of evidence spread across intrusion detection systems, network telemetry, and endpoint logs. This labor-intensive work strains limited analyst capacity, motivating research into intelligent systems that can accelerate incident analysis.

Current detection mechanisms depend heavily on signatures and static rules, which cannot generalize to previously unseen attack patterns. Sophisticated adversaries exploit this gap through techniques like misconfigured certificate template abuse (e.g., ESC1 ([Schroeder and Christensen, 2021](https://arxiv.org#bib.bib18))), Kerberos ticket forgery ([MITRE ATT&CK, 2025](https://arxiv.org#bib.bib19)), and stepwise lateral movement through network trust relationships. Such attacks can progress over hours or days, depositing forensic artifacts across disparate log sources (Suricata alerts, Zeek connection records, Windows authentication events) where no individual entry reveals the complete attack chain. Recent machine learning approaches address alert triage and anomaly scoring ([Song et al., 2024](https://arxiv.org#bib.bib13); [Wei et al., 2025](https://arxiv.org#bib.bib14)), but these methods yield classifications or rankings, not the narrative reconstruction that incident responders require.

Large language models are well-positioned to address this problem: they can interpret unstructured text, integrate scattered facts into coherent narratives, and communicate findings in natural language ([Xu et al., 2025](https://arxiv.org#bib.bib9)). Feeding raw security logs directly into an LLM, however, is impractical. A single incident may produce millions of log entries, vastly exceeding model context limits ([Cai et al., 2025](https://arxiv.org#bib.bib17)). These logs mix genuine attack indicators with overwhelming volumes of routine activity (normal authentications, benign connections, spurious alerts), burying the attack signal. Additionally, incident response often demands rapid turnaround, while LLM inference remains comparatively slow. These challenges motivate the design of new AI-enabled security systems that extract relevant events from such large volumes of logs and generate incident reports interpretable by security analysts.

We present a RAG-based system for security incident analysis that extracts relevant threat indicators by running targeted queries on security logs, mapping the attack indicators to the MITRE ATT&CK framework, and feeding the subsequent results to a LLM with context augmented by semantically similar events to generate interpretable reports of security incidents. The framework operates in two modes: forensic question-answering and attack reconstruction. In the first mode, analysts pose specific questions (identifying infected hosts, command-and-control (C2) servers, or initial compromise vectors) and receive evidence-backed reports with explainable answers. In the second mode, the system reconstructs attack sequences by associating distinct forensic events into causal narratives of attack progression over time. Central to our approach is a security-aware context construction pipeline. Rather than pass raw logs to the LLM, we extract through targeted queries Indicators Of Compromise (IOCs), compute aggregates of log data, and organize results into semantically meaningful chunks that preserve cross-event relationships. The RAG architecture is essential in extracting the most relevant information from multiple security logs for inclusion in the LLM context, enabling the model to generate interpretable incident reports for security analysts. Our general architecture supports multiple LLM providers—both cloud APIs and locally deployed models—enabling organizations to balance performance, cost, and data sensitivity.

We make the following contributions:

Problem formulation for LLM-based incident analysis. We frame security incident analysis as two complementary tasks: (a) structured question-answering with type-specific matching functions that handle the semantics of security answers (IP addresses, hostnames, domain sets), and (b) attack sequence reconstruction that correlates discrete forensic events into causal narratives of attack progression.

Security-aware RAG architecture with cross-event semantic reasoning. We design a retrieval pipeline tailored to security data: targeted queries extract indicators, aggregators compress thousands of events into patterns, and semantic chunking preserves cross-event relationships. This enables LLMs to identify attacks requiring correlation across discrete events, such as the detection of Active Directory certificate abuse by recognizing Subject/SAN mismatches across certificate request and issuance operations. This demonstrates contextual interpretation that distinguishes coordinated exploitation from individually legitimate activities.

LLM provider evaluation with cost-effectiveness analysis. We evaluate eight LLM configurations spanning cloud APIs (Claude Sonnet 4, DeepSeek V3, GPT-4, GPT-4o, GPT-5-mini, GPT-5.2) and local deployment (Llama 3.1:70b, Cisco Foundation-Sec-8B) on malware traffic and Active Directory attack scenarios. The best-performing configurations (Claude Sonnet 4, DeepSeek V3) achieve 100% recall across all four malware scenarios that we analyzed, while attack step detection on Active Directory scenarios reaches 100% precision and 82% recall. DeepSeek achieves accuracy equivalent to Claude at 15 lower cost ($0.008 vs. $0.12 per analysis), making it the most cost-effective cloud provider. Local deployment (Llama) provides data privacy with acceptable accuracy (95% recall) for environments with strict data governance requirements. Notably, the security-specialized Cisco Foundation-Sec-8B model does not outperform general-purpose models at 90% recall, suggesting that reasoning capability matters more than domain-specific pretraining for complex forensic tasks. The system completes malware analysis in 1–2 minutes per incident with cloud providers, while Active Directory attack analysis runs in under 1 minute per 5-minute window with local deployment, demonstrating real-time feasibility for both scenario families.

To support reproducibility, we will release our implementation, including the query library, RAG pipeline, and evaluation scripts, along with detailed results for the malware traffic scenarios. The malware traffic datasets are publicly available ([Duncan, 2026](https://arxiv.org#bib.bib21)); the Active Directory data originates from a private red team exercise and has not been publicly released.

## 2. Related Work

LLMs for Cybersecurity. Large language models have emerged as tools for cybersecurity automation, with recent surveys cataloging applications across vulnerability detection, malware analysis, threat intelligence, and incident response ([Xu et al., 2025](https://arxiv.org#bib.bib9)). This body of work demonstrates both the potential and limitations of LLMs for security tasks.

Early efforts adapted pre-trained models to cybersecurity text. SecureBERT ([Aghaei et al., 2023](https://arxiv.org#bib.bib1)) introduced a domain-specific BERT model trained on cybersecurity corpora, demonstrating improved performance on tasks involving MITRE ATT&CK terminology. CySecBERT ([Bayer et al., 2024](https://arxiv.org#bib.bib10)) adopted domain adaptive pre-training to BERT on a large scale cybersecurity corpus to improve performance on cybersecurity NLP tasks such as Named Entity Recognition and Cyber Threat Intelligence. For threat taxonomy mapping, TRAM fine-tunes SciBERT to map reports to MITRE ATT&CK techniques ([MITRE, 2023](https://arxiv.org#bib.bib16)). These models provide strong semantic representations for classification and embedding tasks.

Log-based anomaly detection represents a key application area. LogLLM ([Guan et al., 2025](https://arxiv.org#bib.bib11)) combines BERT for semantic extraction with Llama for sequence classification on system log datasets. LogPrompt ([Liu et al., 2024](https://arxiv.org#bib.bib12)) explores zero-shot anomaly detection through prompt engineering. These approaches focus on system logs (e.g., HDFS, Linux) and binary anomaly labels rather than security-specific logs with multi-stage attack patterns.

Recent work explores Multi-agent LLM systems to cyber security tasks such as insider threat detection (Audit-LLM ([Song et al., 2024](https://arxiv.org#bib.bib13)) demonstrates reduced false positives for insider threat detection) while SOC-specific systems like CORTEX ([Wei et al., 2025](https://arxiv.org#bib.bib14)) propose specialized agents for alert triage. Work on CTI automation ([Tseng et al., 2024](https://arxiv.org#bib.bib7)) develops agents that extract Indicators of Compromise from threat reports. These systems advance alert-level processing but focus on triage and summarization rather than answering specific questions about detected incidents.
Examining operational use, Singh et al. analyzed queries from 45 SOC analysts, finding that LLMs function as cognitive aids that augment rather than replace expertise ([Singh et al., 2025](https://arxiv.org#bib.bib15)).

In contrast to prior work focusing on alert triage or classification, our work addresses end-to-end incident analysis formulated as question-answering over heterogeneous security logs, processing data from intrusion detection systems, network monitors, and authentication events.

Retrieval-Augmented Generation. Retrieval-Augmented Generation (RAG) addresses limitations of LLMs—hallucination, outdated knowledge, and opacity—by conditioning generation on external evidence retrieved at inference time ([Lewis et al., 2020](https://arxiv.org#bib.bib2)). RAG has become the dominant paradigm for knowledge-intensive tasks where accuracy and traceability are required. Surveys categorize RAG architectures into retriever-centric, generator-centric, and hybrid designs, with recent advances in adaptive retrieval, iterative refinement, and self-reflection ([Gao et al., 2024](https://arxiv.org#bib.bib3); [Sharma, 2025](https://arxiv.org#bib.bib4)).

Recent work applies RAG to security tasks. CyberRAG ([Blefari et al., 2026](https://arxiv.org#bib.bib5)) presents an agentic framework for cyber attack classification, using iterative retrieval over domain-specific knowledge bases to reduce false positives and generate explanations. AgCyRAG ([Kurniawan et al., 2025](https://arxiv.org#bib.bib6)) combines knowledge graph retrieval with vector search for security log analysis, orchestrating specialized agents to integrate structured threat intelligence with security log data. Work on threat intelligence automation ([Tseng et al., 2024](https://arxiv.org#bib.bib7)) uses RAG to extract Indicators of Compromise from CTI reports and generate regular expressions to assist security analysts in establishing SIEM correlation rules.
GraphRAG-based approaches ([Carvalho et al., 2025](https://arxiv.org#bib.bib8)) leverage ontology-backed knowledge graphs constructed from network logs to support LLM-driven query generation for network security monitoring.
These systems demonstrate RAG’s applicability to security data, primarily focusing on attack classification and threat intelligence extraction.

Our work applies RAG to a different task: answering structured security questions over heterogeneous log sources (Suricata alerts, Zeek connections, Windows events). This requires smart chunking strategies tailored to security data and retrieval that supports reasoning about attack progression across multiple log sources.

## 3. Problem Formulation

We formalize security incident analysis as a question-answering task and define the evaluation metrics used throughout our experiments.

### 3.1. Security Incident Analysis as Question Answering

Let denote a security incident, characterized by a collection of security logs (e.g., Suricata alerts, Zeek connection logs, Windows event logs). We formulate incident analysis as question-answering: given an incident’s logs, the system must answer forensic questions about the attack.

###### Definition 3.0 (Evaluation Questionnaire).

A questionnaire is a finite collection of question-answer pairs drawn from the space of possible questionnaires over incident :

where:

- •
is a natural language question
- •
is the reference answer
- •
is the answer type (defined below)
- •
is the number of questions in the questionnaire

#### Answer Types.

#### Concrete Questionnaire.

Throughout our experiments, we use a questionnaire of M = 5 questions targeting the essential information incident responders need to scope and contain an attack:

1. (1)
What is the IP address of the potentially infected internal host in the LAN? ()
2. (2)
What is the hostname of the potentially infected machine in the LAN? ()
3. (3)
What is the Windows user account name of the potentially infected machine in the LAN? ()
4. (4)
What are the likely fake or suspicious domains / URLs for initial infection? ()
5. (5)
What are the suspicious external IP addresses contacted, which might be involved in command-and-control (C2) communication? ()

Questions 1—3 identify affected assets, question 4 determines the initial compromise vector, and question 5 pinpoints command-and-control infrastructure. These represent core forensic questions common across incident types. The framework naturally extends to additional questions (e.g., "What MITRE ATT&CK techniques were used?" or "What files were dropped?") without modification to the underlying architecture.

Beyond forensic identification, we also evaluate attack reconstruction: deducing the attack path a malicious actor took over a given timeframe. For this task, we pose a compound question ("What did the attacker do? What defenses should be implemented?") and evaluate responses using precision (fraction of reported attack steps matching reference) and recall (fraction of advised remediations matching reference). This formulation unifies both modes within the question-answering framework, although attack recreation requires richer evaluation against known attack timelines (Section [7](https://arxiv.org#S7)).

### 3.2. Security Analyzer

The Security Analyzer is a compound AI system that takes raw security logs as input and produces answers to security questions. We decompose it into two main components.

###### Definition 3.0 (Security Analyzer).

A Security Analyzer is a function:

where is the space of security logs, is the question space, and is the response space. For an incident with logs and questionnaire :

Following the compound AI systems paradigm ([Zaharia et al., 2024](https://arxiv.org#bib.bib20)), we decompose the Security Analyzer into independently optimizable components:

#### Security Context Extraction

(): This component interfaces with the SIEM platform to retrieve logs and applies a library of predefined IOC queries to extract security-relevant features such as Suricata alerts, suspicious certificates, high-volume connections, authentication anomalies. A RAG retrieval function then selects the top-k most relevant chunks for each question based on semantic similarity.

#### RAG-LLM Analysis

(): Given the retrieved context and a question, the LLM produces a structured response with supporting evidence. This modular structure allows each component to be optimized independently: the query set determines detection coverage, the embedding model controls retrieval quality, governs context size, and the LLM provider affects reasoning accuracy.

### 3.3. Matching Functions

A key challenge in evaluating security analysis systems is defining appropriate matching functions. Unlike standard QA benchmarks where exact string matching can be sufficient, security answers have structure that must be respected.

###### Definition 3.0 (Type-Specific Matching).

For each answer type , we define a matching function . Let denote the reference answer and denote the model’s answer:

where performs case-insensitive comparison.

###### Remark 3.1 (Non-Triviality of the Task).

The matching function reveals why this task is non-trivial. Consider a baseline that generates random answers:

- •
For (private IPv4):
- •
For : The space of valid Windows hostnames grows in the billions of elements.
- •
For : Random domain generation has negligible success probability given that there are hundreds of millions of registered domains.

This contrasts with  multiple-choice QA where random baselines achieve  accuracy; for  a random baseline would be correct  of the time. Our task requires the system to *generate* structured answers from unstructured logs.

## 4. System Architecture

Our architecture comprises two components: Security Context Extraction, which reduces raw logs to security-relevant information through targeted queries, and RAG-LLM Analysis, which retrieves relevant context and prompts an LLM to answer forensic questions. Figure [1](https://arxiv.org#acmlabel1) illustrates the overall architecture.

### 4.1. Design Principles

Five principles guided our architectural decisions.

1) Filter before analysis. LLMs are too slow to process large volumes of raw logs and perform poorly on noisy data. We first extract security-relevant information using targeted IOC queries, allowing the system to scale to tractable log volumes and generate interpretable reports.

2) Embed once, query many times. Extracted data is semantically embedded into a vector database and cached to disk. The index is built once per dataset and can be queried repeatedly with different questions, LLM providers, or prompt strategies without reprocessing.

3) Periodic analysis. Rather than invoking the LLM on every event, the system performs analysis at defined intervals, batching related activity into coherent time windows.

4) Provider-agnostic design. LLM interactions are abstracted behind a common interface, enabling substitution of providers to balance cost, latency, and privacy requirements.

5) Extensible IOC query library. Detection queries are maintained as a separate library with associated MITRE ATT&CK techniques, allowing extension without modifying the core pipeline.

### 4.2. Security Context Extraction

The system integrates with existing network monitoring infrastructure through standard APIs. Our implementation uses Security Onion, an open-source platform that aggregates network traffic using Suricata and Zeek, communicating through ElasticSearch REST API calls. The architecture generalizes to any SIEM exposing a query API.

Security Context Extraction relies on a library of IOC extraction queries, each targeting a specific activity type. Table [1](https://arxiv.org#S4.T1) shows the query library for Active Directory attacks with associated MITRE ATT&CK techniques; malware traffic scenarios use a separate set targeting network-level IOCs.

The current query library was developed iteratively for the evaluated attack types using domain expertise and LLM assistance, validating each query against known attack data; extending coverage to novel attack patterns requires adding corresponding queries, though the modular design facilitates this extension.
Full query definition examples appear in Appendix [F](https://arxiv.org#A6).

| Query | MITRE ATT&CK | 
|---|---|
| PowerShell Injection | T1059 – Command and Scripting Interpreter | 
| File Drop | T1204 – User Execution | 
| Certificate Enumeration | T1649 – Steal/Forge Authentication Certificates | 
| Certificate Request | T1649 – Steal/Forge Authentication Certificates | 
| Certificate Issued | T1649 – Steal/Forge Authentication Certificates | 
| Kerberos Authentication | T1558 – Steal/Forge Kerberos Tickets | 
| Kerberos Service Tickets | T1558 – Steal/Forge Kerberos Tickets | 
| Service Installation | T1543 – Create/Modify System Process | 
| User Account Creation | T1136 – Create Account | 
| Security Group Modification | T1098 – Account Manipulation | 
| SSH to SCADA Server | T1021.004 – Remote Services: SSH | 
| SCADA Service Stopped | T1489 – Service Stop | 

Each query pairs a base filter with aggregators that compress matching events into ranked patterns, exposing behavioral signals that individual log entries would not reveal. This design is an architectural choice: the aggregation step reduces thousands of events into compact, semantically rich summaries that preserve cross-event patterns required for attack identification. The extracted aggregations are then embedded and indexed for retrieval, as described in the following section.

### 4.3. RAG-LLM Analysis

The RAG-LLM Analysis component transforms extracted security information into actionable incident reports. Given a set of security questions, it retrieves relevant context from the embedded document store and prompts an LLM to produce evidence-based findings. This design decouples index construction from analysis, enabling rapid experimentation with different questions, providers, and prompt strategies without reprocessing the source data.

Data Processing and Embedding. The Security Context Extraction component produces structured output containing aggregations and log entries from the SIEM platform. Before embedding, this output is split into semantically meaningful chunks rather than arbitrary text segments. The data chunks usually consist of aggregate results, which summarize patterns across many events.

Chunks are embedded using a pre-trained sentence embedding model and indexed in a vector store for fast similarity search.<sup>1</sup><sup>1</sup>
1
              
              
              
              
              
              
              
            Our implementation uses all-mpnet-base-v2 and FAISS; other embedding models and vector stores could be substituted. The complete index—chunks, metadata, and embeddings—is serialized to disk, allowing the embedding phase to run once per dataset.

Retrieval and Prompt Construction. Given a security question, the system retrieves relevant chunks from the embedding index using semantic similarity search. The question is embedded using the same model as the indexed chunks, and nearest neighbors are retrieved based on vector similarity. This retrieval-augmented approach grounds LLM responses in actual log data, reducing hallucination and enabling evidence-based reasoning that analysts can verify.

The prompt establishes the LLM’s role as a cybersecurity analyst, presents the question, and provides brief network context with topology information (address ranges, domain name, key infrastructure). Retrieved chunks appear next, each tagged with its source file to support attribution. The prompt concludes with an instruction to answer based on the provided evidence or indicate when information is insufficient. We provide the base prompt template in Appendix [B](https://arxiv.org#A2) and a sample network context in Appendix [C](https://arxiv.org#A3).

Security Questions.
The system supports different categories of security questions depending on the analysis goal (Appendix [D](https://arxiv.org#A4)). Identification questions focus on indicators of compromise: infected hosts, compromised accounts, malicious domains, and command-and-control servers. Timeline questions focus on attack progression: what steps did the attacker take, in what order, and when. Remediation questions focus on defensive actions: what steps should be taken to contain the incident and prevent further damage. All question types use the same retrieval and prompting pipeline, with the LLM adapting its response format based on the question framing.

Multi-LLM Support. Following design principle number 4, the system abstracts LLM interactions behind a common interface, allowing different providers to be substituted without modifying the analysis pipeline. Currently supported providers include Anthropic, OpenAI, and DeepSeek as cloud APIs, and Llama and Cisco as locally-deployed options.

Output Generation.
The system produces a structured incident report containing findings for each security question, with responses that include specific evidence (IP addresses, hostnames, timestamps) and attribute findings to source files (Appendix [E](https://arxiv.org#A5)). A summary section follows, condensing the findings into a brief overview: attack type, key indicators, and recommended actions. The report concludes with metadata for reproducibility: the LLM provider, the number of chunks analyzed, the retrieval settings, and the timing information.

### 4.4. End-to-End Example

To illustrate how extraction and RAG-LLM analysis work together, consider a malware infection where the compromised host must be identified along with the responsible user account. The raw dataset contains 3,694 log events spanning HTTP connections, Kerberos authentication, IDS alerts, and TLS certificate exchanges (Fake Authenticator Malware scenario ([Duncan, 2026](https://arxiv.org#bib.bib21))).

The extraction queries reduce this to semantically rich summaries. The Suricata alert query identifies malicious activity:

These alerts confirm malicious activity from IP 10.1.17.215, but reveal neither the user responsible nor the specific payloads retrieved. The Kerberos client query provides identity attribution:

The file download query reveals the attack payload:

No single data source provides the complete picture. The IDS alerts lack user attribution; Kerberos logs show authentication but not malicious behavior; HTTP logs capture downloads but cannot distinguish malicious from benign traffic. When these aggregations are embedded and retrieved, the LLM corroborates across sources via the shared IP address, concluding that user shutchenson on workstation DESKTOP-L8C5GSJ downloaded a PowerShell payload from a command-and-control server.

This example illustrates how extraction reduces thousands of log events into three compact aggregations while preserving the semantic links (shared IP addresses) that enable cross-source reasoning. The complete queries and corresponding LLM output appear in Appendix [F](https://arxiv.org#A6).

## 5. Experimental Overview

We evaluate the system on two complementary scenarios: malware traffic analysis, which tests forensic question-answering, and Active Directory (AD) attack analysis, which tests attack reconstruction and defense recommendation. This section presents our research questions, shared experimental setup, and evaluation metrics; Sections [6](https://arxiv.org#S6) and [7](https://arxiv.org#S7) present results for each scenario.

Research Questions. We explore the following questions:

- RQ1 (Feasibility):
- 
Can a RAG-based system achieve acceptable performance on security incident analysis?
- RQ2 (Provider Comparison):
- 
How do different LLM providers compare in performance, latency, and cost?
- RQ3 (Context Sensitivity):
- 
How does the number of retrieved chunks affect performance?
- RQ4 (Reliability):
- 
How consistent is performance across different attack types?
- RQ5 (RAG Necessity):
- 
Is RAG preprocessing essential, or can LLMs analyze raw security logs directly?
- RQ6 (Practical Utility):
- 
Do system-generated defense recommendations align with expert-defined actions?

RQ1–RQ5 are addressed in the malware traffic evaluation (Section [6](https://arxiv.org#S6)), which compares eight LLM configurations across four attack scenarios and evaluates a no-RAG baseline. RQ1 and RQ6 are addressed in the Active Directory evaluation (Section [7](https://arxiv.org#S7)), which tests attack detection and defense recommendation on a multi-stage intrusion.

LLM Providers and Models. We evaluate eight configurations spanning cloud APIs and local deployment:

- •
Claude Sonnet 4 (Anthropic): Cloud API
- •
DeepSeek V3 (DeepSeek): Cloud API
- •
GPT-4, GPT-4o, GPT-5-mini, GPT-5.2 (OpenAI): Cloud API
- •
Llama 3.1:70b (via Ollama): Local GPU deployment
- •
Cisco Foundation-Sec-8B: Local GPU deployment, security-specialized

The malware evaluation uses all providers; the AD evaluation uses Llama 3.1 to demonstrate local deployment feasibility.

RAG Configuration. The RAG pipeline uses the following parameters:

- •
Embedding model: all-mpnet-base-v2 (sentence transformer)
- •
Vector store: FAISS with cosine similarity
- •
- •
LLM parameters: temperature, max output tokens (2000 for Cisco to avoid truncation)

Each chunk contains a complete aggregation result rather than arbitrary text segments, preserving semantic coherence for retrieval.

Evaluation Metrics. We evaluate against reference sets derived from published scenario solutions and manual log analysis. Let denote the reference set and denote the model’s answer set. We compute:

For single-value questions (e.g., infected host IP), precision equals recall and scoring is binary. For set-valued questions (e.g., C2 indicators), models receive partial credit proportional to the fraction of reference indicators found.

The malware evaluation primarily reports recall, as the reference answers capture *confirmed* malicious indicators from published solutions rather than an exhaustive enumeration of all suspicious activity. Reference answers were validated by two analysts who independently reviewed the raw data using Wireshark and the Security Onion Kibana dashboard.
Models may identify additional indicators (Appendix [I](https://arxiv.org#A9)) that are legitimately suspicious but absent from the reference set. Appendix [H](https://arxiv.org#A8) provides detailed precision-recall breakdowns showing that several reported indicators not in the reference set exhibit genuinely suspicious characteristics.
The AD evaluation reports both precision and recall, as its reference timeline was manually extracted through exhaustive log review and cross-checked by two analysts.

## 6. Malware Traffic Analysis

Data. We evaluate on four malware traffic scenarios from malware-traffic-analysis.net ([Duncan, 2026](https://arxiv.org#bib.bib21)) and Unit 42 ([Duncan, 2023](https://arxiv.org#bib.bib22)), each representing a distinct attack pattern:

- •
Fake Authenticator (Jan 2025): User directed to fraudulent Google Authenticator download page, leading to multi-server C2 communication.
- •
NetSupport RAT (Nov 2024): Legitimate website injected with malicious scripts delivering fake browser updates and a Remote Access Trojan.
- •
Koi Stealer (Sep 2024): Information-stealing malware with multiple C2 endpoints and regular check-in behavior.
- •
IcedID (Apr 2023): Banking trojan delivered via Firebase Storage URL, generating HTTPS C2 traffic and BackConnect activity for post-compromise operations.

Each scenario consists of a PCAP file imported into Security Onion, which generates Zeek logs (connection, HTTP, DNS) and Suricata alerts.

### 6.1. Incident Analysis Performance

Table [2](https://arxiv.org#S6.T2) presents recall for each provider across the four scenarios, addressing RQ1 (feasibility) and RQ4 (reliability).

|  | Fake | Net. | Koi |  |  |  | 
|---|---|---|---|---|---|---|
| Provider | Auth. | RAT | Steal. | IcedID | Mean |  | 
| Claude Sonnet 4 | 100 | 100 | 100 | 100 | 100 | 0.00 | 
| DeepSeek V3 | 100 | 100 | 100 | 100 | 100 | 0.00 | 
| Ollama 3.1:70b | 100 | 100 | 80 | 100 | 95 | 0.09 | 
| Cisco 8B | 100 | 90 | 100 | 70 | 90 | 0.12 | 
| GPT-5.2 | 60 | 100 | 100 | 80 | 85 | 0.17 | 
| GPT-4o | 60 | 100 | 80 | 80 | 80 | 0.14 | 
| GPT-4 | 60 | 100 | 80 | 60 | 75 | 0.17 | 
| GPT-5-mini | 60 | 100 | 80 | 60 | 75 | 0.17 | 

Two cloud providers achieve 100% recall across all four scenarios: Claude Sonnet 4 and DeepSeek V3. These models correctly identified all reference indicators including infected hosts, user accounts, malicious domains, and C2 servers. Notably, locally-deployed models (Ollama at 95%, Cisco at 90%) perform comparably to most cloud providers, suggesting that organizations with data sensitivity requirements need not sacrifice accuracy.

The results reveal distinct failure patterns across model families. GPT models consistently underperform on the Fake Authenticator scenario (60%), failing to identify C2 servers that required correlating behavioral aggregations (connection counts, file download volumes) with Suricata alerts. In contrast, all models achieve 90–100% on NetSupport RAT, the most straightforward scenario with clear malicious domain indicators.
IcedID proves most challenging overall due to its multi-stage infection chain: an initial redirect IP leads to a Firebase Storage URL, which delivers an installer that contacts yet another domain before establishing C2 (details in Appendix [I](https://arxiv.org#A9)).
This scenario exemplifies why cross-event semantic reasoning is essential: tracing the full attack chain requires correlating redirect IPs, download URLs, and C2 domains across separate log sources.
Here, Claude, DeepSeek, Cisco, and Ollama correctly identified the initial infection IP (80.77.25.175), while all GPT models reported only C2 domains—a pattern suggesting they prioritize high-confidence alerts over tracing the full attack chain.

The standard deviation quantifies reliability (RQ4). Claude and DeepSeek exhibit zero variance across our four scenarios. Higher variance indicates inconsistent performance: Cisco () and GPT-5.2 () show scenario-dependent accuracy that complicates deployment decisions. For production use, consistency matters: a system that occasionally misses half the indicators creates false confidence.

### 6.2. Reasoning Pattern Analysis

Beyond recall metrics, models exhibit qualitatively different reasoning strategies.

In Appendix [G](https://arxiv.org#A7), we compare responses to the C2 detection question (Q5) on the Koi Stealer scenario, where the reference C2 server is 79.124.78.197.
DeepSeek identifies only the confirmed C2 server, explicitly rejecting domain-resolved IPs as insufficiently corroborated. Cisco provides tiered findings—the primary C2 plus secondary suspicious IPs with context—and notes operational considerations like domain fronting. GPT-5.2 lists seven IPs without prioritization, including the *internal* victim host (172.17.0.99) as a “suspicious external IP”—a category error revealing shallow pattern matching rather than analytical reasoning.

These patterns reflect a precision-coverage trade-off: DeepSeek minimizes false positives but risks missing secondary infrastructure; Cisco optimizes for SOC workflows where comprehensive threat visibility is prioritized; GPT-5.2’s undifferentiated enumeration increases analyst burden. Appendix [H](https://arxiv.org#A8) provides detailed precision-recall analysis for each scenario. For production deployment, evidence-weighted reasoning (distinguishing confirmed threats from suspicious activity) is preferable to exhaustive listing.

### 6.3. Impact of Context Size

We investigate how the number of retrieved chunks affects performance (RQ3). Using the Fake Authenticator scenario, we evaluate for Claude, DeepSeek, and GPT-5.2.

| Provider |  |  |  |  |  |  | 
|---|---|---|---|---|---|---|
| Claude Sonnet 4 | 60 | 93 | 93 | 100 | 100 | 100 | 
| DeepSeek V3 | 60 | 93 | 93 | 100 | 100 | 100 | 
| GPT-5.2 | 60 | 60 | 60 | 60 | 67 | 80 | 

Claude and DeepSeek both achieve 100% at , following identical progression (60% 93% 100%). At , all models identify only basic indicators (IP, hostname, malicious domain) but miss the user account and all C2 servers. At , Claude and DeepSeek correctly identify the user account and two of three C2 IPs (2/3 recall on Q5), reaching 93% overall. At , sufficient context is retrieved to detect all three C2 servers, including the primary server (5.252.153.241) which requires behavioral aggregation data showing 1,198 connections and 594 file downloads.

GPT-5.2 shows minimal improvement with additional context, reaching only 80% at . The model exhibits a persistent reasoning error: confusing the Windows machine account (DESKTOP-L8C5GSJ$) with the human user account (shutchenson) across all context sizes, resulting in 0% recall on Q3 regardless of . C2 detection also lags significantly—GPT-5.2 achieves 0/3 recall on Q5 until (1/3), only reaching 3/3 at .

### 6.4. Baseline Comparisons

No-RAG Baseline. We evaluate a no-RAG baseline to assess whether RAG preprocessing is essential or whether LLMs can analyze raw security logs directly. For each security question, we send as many raw logs as fit within the model’s context window, without any feature extraction or embedding. This represents the simplest possible approach: direct LLM analysis of unprocessed security data. While a sliding window approach processing logs in multiple batches could eventually cover all data, it would require 24 batches for this scenario’s 3,694 logs (Claude’s 158-log window), resulting in API calls versus 5 for RAG. With rate limiting (Claude required 150s between calls), total analysis time would exceed 5 hours versus 2 minutes for RAG.

| Provider | RAG | No-RAG | Logs | Attack | 
|---|---|---|---|---|
|  | (k=7) |  | Seen | Infra. | 
| Claude Sonnet 4 | 100 | 60 | 158 (4.3%) | 0/4 | 
| DeepSeek V3 | 100 | 60 | 104 (2.8%) | 0/4 | 
| GPT-4 | 60 <sup>∗</sup> | 40 <sup>∗</sup> | 22 (0.6%) | 0/4 | 
| GPT-4o | 60 <sup>∗</sup> | 40 <sup>∗</sup> | 22 (0.6%) | 0/4 | 
| <sup>∗</sup> Persistent user/hostname confusion |  |  |  |  | 

Table [4](https://arxiv.org#S6.T4) compares RAG and no-RAG performance on the Fake Authenticator scenario.
Context window constraints limit no-RAG approaches to 0.6–4.3% of available logs (22–158 out of 3,694). The logs that fit are chronologically first and contain primarily benign startup activity. All models correctly identify victim information (IP, hostname) present in these benign logs but achieve 0% detection of the attack infrastructure: the fake domain and all three C2 servers appear only in later logs containing Suricata alerts and suspicious traffic, which exceeded context limits. GPT models maintain their user/hostname confusion error even with raw logs, confirming this is a reasoning flaw rather than a retrieval artifact.

Suricata-Only Baseline. We also evaluated whether traditional IDS alerts alone suffice. Using only Suricata alerts from the Fake Authenticator scenario, an analyst could identify the infected IP and C2 infrastructure. However, hostname, user account, and initial infection domain are absent from IDS data entirely—these require Kerberos authentication logs and HTTP connection records. This yields 40% recall, comparable to no-RAG but with a different failure mode: no-RAG fails due to context limits, while Suricata-only fails due to missing data sources.

### 6.5. Cost Analysis

We compare cost-effectiveness across providers based on observed token usage. Table [5](https://arxiv.org#S6.T5) summarizes pricing (from provider documentation as of late 2025), analysis time, and performance.
The cost per analysis is computed as:

| (1) |  |  |  | 

The number of LLM calls per analysis is  (i.e., 5 questions). We use conservative estimates of input and output tokens:  and . ,  are the model’s prices in USD per million tokens from Table [5](https://arxiv.org#S6.T5).

| Provider | In | Out | Cost/ | Recall | Time | 
|  | ($/M) | ($/M) | Anlys. | (%) | (min) | 
| DeepSeek V3 | 0.28 | 0.42 | $0.008 | 100 | 1.2 | 
| Claude Sonnet 4 | 3.00 | 15.00 | $0.12 | 100 | 1.2 | 
| GPT-5.2 | 1.75 | 14.00 | $0.09 | 85 | 0.3 | 
| Ollama 3.1:70b | — | — | $0 <sup>∗</sup> | 95 | 2.5 | 
| Cisco 8B | — | — | $0 <sup>∗</sup> | 90 | 16.0 | 
| <sup>∗</sup> Local deployment; requires GPU infrastructure. |  |  |  |  |  | 

DeepSeek achieves the highest recall (100%) at the lowest cost ($0.008 per analysis), making it 15 cheaper than Claude while matching its performance. At operational scale (1,000 analyses/day), this translates to $240/month versus $3,600/month. Local deployment eliminates per-query costs but requires GPU infrastructure and incurs longer processing times: Ollama (70B) achieves 95% recall at 2.5 min/analysis, while Cisco 8B achieves 90% at 16 min due to less optimized infrastructure.

## 7. Active Directory Attack Analysis

Data. The attack data originates from a controlled red team exercise against an Active Directory environment. The scenario simulates a sophisticated attacker (Red) attempting to compromise a Windows domain while defenders (Blue) respond in real-time.

*Red Team Actions:* Initial compromise via Metasploit, certificate request with Administrator SAN, certificate enumeration, Kerberos TGT and service ticket requests, PSExec lateral movement to Domain Controller, malicious user creation, and ultimately SSH access to SCADA with service disruption (attack objective).

*Blue Team Actions:* Certificate revocation, KRBTGT reset, Domain Controller restart, password reset, and user account disable. With defensive response, Blue successfully prevented SCADA compromise.

Evaluation. Unlike the malware scenarios with discrete question-answer pairs, the AD evaluation uses the attack recreation task: given a timeframe, identify attack steps and recommend defensive actions. We evaluate on 5-minute sliding windows (15:30–15:35, 15:35–15:40, etc.), simulating real-time analysis. The reference attack steps in the timeline were manually extracted through exhaustive log review via the Security Onion Kibana dashboard, enabling evaluation of both precision and recall. Each data filtering query produces a compact result fitting in a single chunk; with 9 queries generating 9 chunks, all relevant context is retrieved simultaneously.

### 7.1. Attack Step Detection

Table [6](https://arxiv.org#S7.T6) summarizes precision and recall across analysis windows (RQ1). The system achieved 100% precision—every reported attack step corresponded to actual malicious activity. Recall averaged 82% across windows. The system correctly identified initial access (Metasploit, PowerShell injection, file drops), the credential theft chain (certificate enumeration, request, issuance, Kerberos tickets), and lateral movement (PSExec via service installation).

| Window |  | TP = | FP | Prec. | Rec. | 
| 15:30–35 | 11 | 11 | 0 | 100% | 100% | 
| 15:35–40 | 8 | 6 | 0 | 100% | 75% | 
| 15:40–46 | 7 | 5 | 0 | 100% | 71% | 
| Average | – | – | 0 | 100% | 82% | 
| R is the Reference set; A denotes the detected attack steps. |  |  |  |  |  | 

### 7.2. Multi-Step Attack Reconstruction

We examine how the system reconstructed an ESC1 certificate template abuse attack across five discrete events: certificate enumeration, certificate request with SAN:Administrator, certificate issuance with Subject:CN=<user>, Kerberos TGT as Administrator, and service ticket for krbtgt. Each event was captured by an independent query targeting specific Windows event codes (4662, 4886, 4887, 4768, 4769).

Given these events as separate chunks, the system produced:

Red enumerated certificates, then requested a certificate with SAN=Administrator. The certificate was issued, allowing impersonation of the Administrator account. Red then obtained a Kerberos TGT as Administrator and requested a service ticket for krbtgt, achieving domain-wide access.


The exploit mechanism required connecting information across chunks. The certificate *request* chunk contained SAN:upn=Administrator, while the certificate *issued* chunk showed Subject:CN=<user>. The LLM identified this Subject/SAN mismatch as the privilege escalation vector, then linked it to subsequent Kerberos events.

### 7.3. Defense Recommendation Quality

We assess whether LLM-generated recommendations align with successful defensive actions (RQ6). Table [7](https://arxiv.org#S7.T7) summarizes results.

| Window | Blue | LLM | P/R | 
|---|---|---|---|
| 15:30–35 | RC, RK, RD | RC, RK, RD, DU | 3/4, 3/3 | 
| 15:35–40 | RK, RD, RP, DU | RK, RD, RC, DU | 3/4, 3/4 | 
| 15:40–46 | RD, DU, RK | RK, DU, RC, RP | 2/4, 2/3 | 
| RC=Revoke Cert, RK=Reset KRBTGT, RD=Restart DC, |  |  |  | 
| DU=Disable User, RP=Reset Password. P/R=Precision/Recall. |  |  |  | 

The LLM achieved 100% coverage of defense action types executed across the timeline, with 80% average recall per window. Recommendations were contextually appropriate: certificate revocation after detecting certificate abuse, KRBTGT reset after Kerberos ticket acquisition, user disable after detecting malicious account creation.

One limitation emerged: the LLM occasionally recommended disabling the Administrator account, which is operationally infeasible. Production deployments would require human review before execution.

### 7.4. Operational Feasibility

The system completes analysis in approximately 61 seconds per 5-minute window: 466ms for query execution (9 queries) and under 60 seconds for LLM analysis using locally-deployed Llama 3.1:70b. This represents 20% of the window duration, leaving time for analyst review and response actions before the next analysis cycle.

This AD scenario represents a fast-moving attack with core exploitation compressed into 60 seconds. The 5-minute window suited this pace, but attack timescales vary widely: ransomware may complete encryption in under 5 minutes, while APT campaigns spread lateral movement over days. Window size must be tuned to threat characteristics. More fundamentally, analysis latency should be measured against response latency rather than attack speed. Defensive actions may require several minutes to execute, and coordinated responses involve human decision-making and approval workflows that typically dominate total incident response time. The system’s sub-minute analysis latency makes detection a small fraction of end-to-end response.

## 8. Conclusion

We presented a retrieval-augmented generation system for security incident analysis that combines targeted query-based filtering with LLM semantic reasoning. Evaluation across eight LLM models on malware and Active Directory scenarios demonstrates that RAG preprocessing is essential (no-RAG baselines miss all attack infrastructure), provider selection dominates retrieval tuning, and DeepSeek V3 achieves Claude-equivalent accuracy (100% recall) at 15 lower cost. Notably, security-specialized models (Cisco Foundation-Sec-8B) do not outperform general-purpose LLMs, suggesting that reasoning capability matters more than domain-specific pretraining for forensic analysis. Our system’s key capability is cross-event semantic reasoning: distinguishing coordinated exploitation from individually legitimate operations by correlating evidence across discrete forensic events. Our evaluation covers four malware scenarios and one Active Directory attack; while results are consistent across these cases, validation on a broader set of attack types and larger-scale deployments remains future work.

###### Acknowledgements.

This research was funded by the Defense Advanced Research Projects Agency (DARPA), under contract W912CG23C0031.
## References

- [1]
 (2025)
LLMs in the SOC: An Empirical Study of Human-AI Collaboration in Security Operations Centres.
 arXiv.
Note: arXiv:2508.18947
External Links: 2508.18947,
[Document](https://dx.doi.org/10.48550/arXiv.2508.18947) Cited by:[§1](https://arxiv.org#S1.p1.1) ,[§2](https://arxiv.org#S2.p4.1) .
- [2]
 (2023)
’Give Me Structure’: Synthesis and Evaluation of a (Network) Threat Analysis Process Supporting Tier 1 Investigations in a Security Operation Center.
pp. 97–111 (en).
External Links: ISBN 978-1-939133-36-6,
[Link](https://www.usenix.org/conference/soups2023/presentation/kersten) Cited by:[§1](https://arxiv.org#S1.p1.1) .
- [3]
 (2025)
Alert Fatigue in Security Operations Centres: Research Challenges and Opportunities.
ACM Comput. Surv. 57 (9), pp. 224:1–224:38.
External Links: ISSN 0360-0300,
[Link](https://dl.acm.org/doi/10.1145/3723158) ,[Document](https://dx.doi.org/10.1145/3723158) Cited by:[§1](https://arxiv.org#S1.p1.1) .
- [4]
 (2021)
Certified pre-owned: abusing active directory certificate services.
Technical report
 SpecterOps.
Note: Whitepaper
External Links: [Link](https://specterops.io/wp-content/uploads/sites/3/2022/06/Certified_Pre-Owned.pdf) Cited by:[§1](https://arxiv.org#S1.p2.1) .
- [5]
 (2025)Steal or forge kerberos tickets (technique t1558)(Website)
Note: Accessed: February 6, 2026
External Links: [Link](https://attack.mitre.org/techniques/T1558/) Cited by:[§1](https://arxiv.org#S1.p2.1) .
- [6]
 (2024)
Audit-LLM: Multi-Agent Collaboration for Log-based Insider Threat Detection.
 arXiv.
Note: arXiv:2408.08902
External Links: 2408.08902,
[Document](https://dx.doi.org/10.48550/arXiv.2408.08902) Cited by:[§1](https://arxiv.org#S1.p2.1) ,[§2](https://arxiv.org#S2.p4.1) .
- [7]
 (2025)
CORTEX: Collaborative LLM Agents for High-Stakes Alert Triage.
 arXiv.
Note: arXiv:2510.00311
External Links: 2510.00311,
[Document](https://dx.doi.org/10.48550/arXiv.2510.00311) Cited by:[§1](https://arxiv.org#S1.p2.1) ,[§2](https://arxiv.org#S2.p4.1) .
- [8]
 (2025)
Large Language Models for Cyber Security: A Systematic Literature Review.
ACM Trans. Softw. Eng. Methodol..
External Links: ISSN 1049-331X,
[Document](https://dx.doi.org/10.1145/3769676) Cited by:[§1](https://arxiv.org#S1.p3.1) ,[§2](https://arxiv.org#S2.p1.1) .
- [9]
 (2025)
LLMLogAnalyzer: A Clustering-Based Log Analysis Chatbot using Large Language Models.
 arXiv.
Note: arXiv:2510.24031
External Links: 2510.24031,
[Document](https://dx.doi.org/10.48550/arXiv.2510.24031) Cited by:[§1](https://arxiv.org#S1.p3.1) .
- [10]
 (2026)
Training exercises - Malware-Traffic-Analysis.net.
Note: [https://www.malware-traffic-analysis.net/training-exercises.html](https://www.malware-traffic-analysis.net/training-exercises.html) Accessed: 2026-02-25
Cited by:[Appendix C](https://arxiv.org#A3.p1.1) ,[§1](https://arxiv.org#S1.p9.1) ,[§4.4](https://arxiv.org#S4.SS4.p1.1) ,[§6](https://arxiv.org#S6.p1.1) .
- [11]
 (2023)
SecureBERT: A Domain-Specific Language Model for Cybersecurity.
In Security and Privacy in Communication Networks,  F. Li, K. Liang, Z. Lin, and S. K. Katsikas (Eds.),
Cham, pp. 39–56.
External Links: [Document](https://dx.doi.org/10.1007/978-3-031-25538-0%5F3) ,
ISBN 978-3-031-25538-0
Cited by:[§2](https://arxiv.org#S2.p2.1) .
- [12]
 (2024)
CySecBERT: A Domain-Adapted Language Model for the Cybersecurity Domain.
ACM Trans. Priv. Secur. 27 (2), pp. 18:1–18:20.
External Links: ISSN 2471-2566,
[Document](https://dx.doi.org/10.1145/3652594) Cited by:[§2](https://arxiv.org#S2.p2.1) .
- [13]
 (2023)
Threat Report ATT&CK Mapper (TRAM).
Note: [https://ctid.mitre.org/projects/threat-report-attck-mapper-tram/](https://ctid.mitre.org/projects/threat-report-attck-mapper-tram/) Cited by:[§2](https://arxiv.org#S2.p2.1) .
- [14]
 (2025)
LogLLM: Log-based Anomaly Detection Using Large Language Models.
 arXiv.
Note: arXiv:2411.08561
External Links: 2411.08561,
[Document](https://dx.doi.org/10.48550/arXiv.2411.08561) Cited by:[§2](https://arxiv.org#S2.p3.1) .
- [15]
 (2024)
LogPrompt: Prompt Engineering Towards Zero-Shot and Interpretable Log Analysis.
In Proceedings of the 2024 IEEE/ACM 46th International Conference on Software Engineering: Companion Proceedings,
ICSE-Companion ’24, New York, NY, USA, pp. 364–365.
External Links: [Document](https://dx.doi.org/10.1145/3639478.3643108) ,
ISBN 979-8-4007-0502-1
Cited by:[§2](https://arxiv.org#S2.p3.1) .
- [16]
 (2024)
Using LLMs to Automate Threat Intelligence Analysis Workflows in Security Operation Centers.
 arXiv.
Note: arXiv:2407.13093
External Links: 2407.13093,
[Document](https://dx.doi.org/10.48550/arXiv.2407.13093) Cited by:[§2](https://arxiv.org#S2.p4.1) ,[§2](https://arxiv.org#S2.p7.1) .
- [17]
 (2020)
Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.
In Advances in Neural Information Processing Systems,
Vol. 33, pp. 9459–9474.
Cited by: [§2](https://arxiv.org#S2.p6.1) .
- [18]
 (2024)
Retrieval-Augmented Generation for Large Language Models: A Survey.
 arXiv.
Note: arXiv:2312.10997
External Links: 2312.10997,
[Document](https://dx.doi.org/10.48550/arXiv.2312.10997) Cited by:[§2](https://arxiv.org#S2.p6.1) .
- [19]
 (2025)
Retrieval-augmented generation: a comprehensive survey of architectures, enhancements, and robustness frontiers.
arXiv preprint arXiv:2506.00054.
External Links: [Link](https://arxiv.org/abs/2506.00054) Cited by:[§2](https://arxiv.org#S2.p6.1) .
- [20]
 (2026)
CyberRAG: An agentic RAG cyber attack classification and reporting tool.
Future Generation Computer Systems 176, pp. 108186.
External Links: ISSN 0167-739X,
[Document](https://dx.doi.org/10.1016/j.future.2025.108186) Cited by:[§2](https://arxiv.org#S2.p7.1) .
- [21]
 (2025)
AgCyRAG: an agentic knowledge graph based RAG framework for automated security analysis.
In Proceedings of the Second International Workshop on Retrieval-Augmented Generation Enabled by Knowledge Graphs (RAGE-KG 2025),
(CEUR Workshop Proceedings).
Cited by: [§2](https://arxiv.org#S2.p7.1) .
- [22]
 (2025)
Towards the Application of GraphRAG to Network Security.
The International FLAIRS Conference Proceedings 38.
External Links: ISSN 2334-0762,
[Document](https://dx.doi.org/10.32473/flairs.38.1.138895) Cited by:[§2](https://arxiv.org#S2.p7.1) .
- [23]
 (2024)
The shift from models to compound AI systems.
Cited by: [§3.2](https://arxiv.org#S3.SS2.p2.1) .
- [24]
 (2023)
Cold as ice: Unit 42 Wireshark quiz for IcedID.
Note: [https://unit42.paloaltonetworks.com/wireshark-quiz-icedid/](https://unit42.paloaltonetworks.com/wireshark-quiz-icedid/) Accessed: 2026-02-25
Cited by:[Appendix C](https://arxiv.org#A3.p1.1) ,[§6](https://arxiv.org#S6.p1.1) .

## Appendix: Table of content

## Appendix A Information about the Malware Scenarios

The file size and number of packets is obtained via capinfos, the number of the Security Onion Logs is obtained form the Kibana Dashboard associated with Security Onion.

| Scenario | File size (MB) | Number of packets | Security Onion Logs | 
|---|---|---|---|
| Fake Authenticator (Jan 2025) |  | k |  | 
| NetSupport RAT (Nov 2024) |  | k |  | 
| Koi Stealer (Sep 2024) |  | k |  | 
| IcedID (Apr 2023) |  | k |  | 

## Appendix B Base Prompt

## Appendix C Sample Network Context

## Appendix D Questions used for LLM Analysis


## Appendix E Sample LLM Answers

We present sample answers generated by Anthropic on the Fake Authenticator scenario, using a 7-chunks context and the Claude Sonnet 4 model.

### E.1. Identifying the IP of the potentially infected host

Question: What is the IP address of the potentially infected internal host in the LAN?

The LLM Analyzer correctly identified the IP 10.1.17.215 as potentially infected, and provided evidence from Suricata Alerts, flagging Power Shell file requests as suspicious and indicating that the IP is engaged in bidirectional traffic (

### E.2. Identifying the C2 framework

Question: What are the suspicious external IP addresses contacted, which might be involved in command-and-control (C2) communication?

The LLM Analyzer correctly identified three suspicious external IPs: 45.125.66.252, 45.125.66.32 and 5.252.153.241, based on a combination self-signed certificates and high-severity Suricata Alerts among other indicators (

## Appendix F Aggregation Queries

The following Elasticsearch queries produce the aggregated results shown in Section [4.4](https://arxiv.org#S4.SS4). Each query pairs a filter with aggregations that compress matching events into ranked summaries.

### F.1. Kerberos Client Aggregation

This query extracts usernames from Kerberos authentication events (port 88) and groups them by source IP address.

### F.2. Suricata High-Severity Alert Aggregation

This query filters for IDS alerts from internal hosts and aggregates by signature name, source IP, and destination IP, with a nested filter for high-severity events.

### F.3. File Download Aggregation

This query identifies file downloads by filtering for common download ports and file extensions, then uses a script to reconstruct HTTP request patterns from log messages.

### F.4. LLM Analysis Output

When the aggregation results are retrieved and provided to the LLM, it corroborates across sources to answer forensic questions. The following output was generated by Claude Sonnet 4 (7-chunk context) for the question: “What is the Windows user account name of the potentially infected machine in the LAN?”

The LLM first identifies the compromised IP from Suricata alerts, then correlates it to a hostname and user account via Kerberos data–demonstrating the cross–query corroboration pattern described in Section [4.4](https://arxiv.org#S4.SS4).

## Appendix G Comparative Analysis of LLM Reasoning

To illustrate how different LLMs approach security incident analysis, we compare outputs from three providers on the same question from the Koi Stealer scenario: “What are the suspicious external IP addresses contacted, which might be involved in command-and-control (C2) communication?” This question requires synthesizing evidence from multiple data sources (Suricata alerts, DNS logs, connection data) and distinguishing confirmed C2 infrastructure from merely suspicious traffic.

The ground truth C2 server for this scenario is 79.124.78.197, which received 49 high-severity alerts including explicit Koi Stealer signatures.

### G.1. DeepSeek V3: Precision-Focused Analysis

DeepSeek produces a structured analysis that systematically evaluates evidence strength and explicitly rejects weak indicators.

DeepSeek explicitly acknowledges alternative candidates (the domain-resolved IPs) but rejects them because they lack corroborating IDS signatures. This demonstrates *evidence-weighted reasoning*: the model distinguishes between “contacted external IPs” and “confirmed C2 infrastructure,” prioritizing high-confidence indicators over volume.

### G.2. Cisco Foundation-Sec-8B: Comprehensive Threat Mapping

The security-specialized Cisco model produces verbose chain-of-thought reasoning that maps the full threat landscape before synthesizing conclusions.

Cisco’s analysis reveals its security domain training: it explicitly considers domain fronting as an evasion technique and provides operational recommendations (host isolation). The model includes secondary IPs as “suspicious” while correctly identifying the primary C2 server, reflecting a defense-in-depth perspective appropriate for SOC workflows where over-reporting is preferable to missed threats.

### G.3. GPT-5.2: Enumerative Listing

GPT-5.2 produces a concise response that lists all contacted external IPs without differentiating evidence strength.

GPT-5.2 conflates three distinct categories: (1) resolved IPs from suspicious domain queries, (2) the confirmed C2 server from Suricata alerts, and (3) the *internal* victim IP. Including 172.17.0.99—the compromised host itself—as a “suspicious external IP involved in C2” represents a category error. The model treats the question as a data extraction task rather than an analytical one, reporting all IPs mentioned in the context without evaluating their relevance to the specific question.

### G.4. Comparative Insights

| Dimension | DeepSeek V3 | Cisco 8B | GPT-5.2 | 
|---|---|---|---|
| Reasoning style | Evidence-weighted; explicit rejection of weak indicators | Chain-of-thought; comprehensive threat mapping | Enumerative; data extraction without filtering | 
| Evidence hierarchy | Distinguishes confirmed vs. suspicious | Tiered presentation (primary, secondary) | Flat list; no prioritization | 
| Answer precision | High (1 IP) | Medium (3 IPs with context) | Low (7 IPs including errors) | 
| Critical errors | None | None | Includes internal IP as “external C2” | 
| Operational context | Minimal | Detailed (domain fronting, isolation) | None | 
| Response length | Medium (250 words) | Long (600 words) | Short (100 words) | 

These patterns illustrate a fundamental trade-off in LLM-assisted security analysis. DeepSeek optimizes for precision, reducing analyst workload by filtering noise but risking missed indicators if its filtering is overly aggressive. Cisco optimizes for coverage and operational utility, providing defense-in-depth recommendations at the cost of verbosity. GPT-5.2 optimizes for surface-level completeness, which paradoxically reduces utility by burying the confirmed C2 server among false positives and category errors.

For SOC deployment, the ideal behavior likely falls between DeepSeek and Cisco: confident identification of high-priority indicators with explicit uncertainty quantification for secondary findings. The GPT-5.2 pattern of undifferentiated enumeration, while superficially “complete,” would increase analyst burden and erode trust in automated systems.

## Appendix H Precision-Recall Analysis

This appendix provides precision-recall metrics for set-valued questions (Q4: suspicious domains/IPs for initial infection, Q5: C2 indicators).

- •
N denotes the number of indicators reported by the LLM model;
- •
TP denotes true positives matching the reference set;
- •
Ref. denotes the reference set count;
- •
TP/N shows precision as a ratio;
- •
Rec. denotes recall (TP divided by reference set count).

The reference set captures *confirmed* malicious indicators from published solutions; several indicators reported as false positives exhibit genuinely suspicious characteristics, so true precision may be higher than reported.

### H.1. Fake Authenticator

Reference set: |Q4| = 1 suspicious domain; |Q5| = 3 C2 IPs.

|  | Q4: Initial Infection (Ref=1) |  |  | Q5: C2 IPs (Ref=3) |  |  | 
| Provider | N | TP/N | Rec. | N | TP/N | Rec. | 
| Claude Sonnet 4 | 5 | 1/5 | 1/1 | 6 | 3/6 | 3/3 | 
| DeepSeek V3 | 2 | 1/2 | 1/1 | 7 | 3/7 | 3/3 | 
| Cisco 8B | 5 | 1/5 | 1/1 | 23 | 3/23 | 3/3 | 
| Ollama 3.1:70b | 2 | 1/2 | 1/1 | 9 | 3/9 | 3/3 | 
| GPT-5.2 | 7 | 1/7 | 1/1 | 10 | 0/10 | 0/3 | 

### H.2. Koi Stealer

Reference set: |Q4| = 1 suspicious domain; |Q5| = 1 C2 IP.

|  | Q4: Initial Infection (Ref=1) |  |  | Q5: C2 IPs (Ref=1) |  |  | 
| Provider | N | TP/N | Rec. | N | TP/N | Rec. | 
| Claude Sonnet 4 | 2 | 1/2 | 1/1 | 3 | 1/3 | 1/1 | 
| DeepSeek V3 | 2 | 1/2 | 1/1 | 1 | 1/1 | 1/1 | 
| Cisco 8B | 3 | 1/3 | 1/1 | 3 | 1/3 | 1/1 | 
| Ollama 3.1:70b | 1 | 0/1 | 0/1 | 1 | 1/1 | 1/1 | 
| GPT-5.2 | 5 | 1/5 | 1/1 | 7 | 1/7 | 1/1 | 

### H.3. NetSupport RAT

Reference set: |Q4| = 2 suspicious domains; |Q5| = 1 C2 IP.

|  | Q4: Initial Infection (Ref=2) |  |  | Q5: C2 IPs (Ref=1) |  |  | 
| Provider | N | TP/N | Rec. | N | TP/N | Rec. | 
| Claude Sonnet 4 | 4 | 2/4 | 2/2 | 2 | 1/2 | 1/1 | 
| DeepSeek V3 | 4 | 2/4 | 2/2 | 5 | 1/5 | 1/1 | 
| Cisco 8B | 2 | 1/2 | 1/2 | 2 | 1/2 | 1/1 | 
| Ollama 3.1:70b | 6 | 2/6 | 2/2 | 2 | 1/2 | 1/1 | 
| GPT-5.2 | 4 | 2/4 | 2/2 | 5 | 1/5 | 1/1 | 

### H.4. IcedID

Reference set: |Q4| = 1 suspicious IP for initial infection (80.77.25.175); |Q5| = 2 C2 indicators (askamoshopsi.com, skansnekssky.com or associated IPs).

This scenario proved most challenging due to its multi-stage infection chain: an initial redirect (80.77.25.175) leads to a Firebase Storage URL delivering a ZIP archive, which contains an IcedID installer that contacts a separate domain (skigimeetroc.com) before establishing C2 communication with yet other domains (askamoshopsi.com, skansnekssky.com). Q3 required distinguishing the user account (csilva) from the hostname (DESKTOP-SFF9LJF) and machine account (DESKTOP-SFF9LJF$)—a distinction that Cisco and older GPT models failed to make.

|  | Q3: User | Q4: Initial Infection (Ref=1) |  |  | Q5: C2 Indicators (Ref=2) |  |  | 
| Provider | Account | N | TP/N | Rec. | N | TP/N | Rec. | 
| Claude Sonnet 4 |  | 5 | 1/5 | 1/1 | 5 | 2/5 | 2/2 | 
| DeepSeek V3 |  | 6 | 1/6 | 1/1 | 4 | 2/4 | 2/2 | 
| Cisco 8B |  | 3 | 1/3 | 1/1 | 5 | 1/5 | 1/2 | 
| Ollama 3.1:70b |  | 3 | 1/3 | 1/1 | 3 | 2/3 | 2/2 | 
| GPT-5.2 |  | 3 | 0/3 | 0/1 | 5 | 2/5 | 2/2 | 
| GPT-4o |  | 3 | 0/3 | 0/1 | 5 | 2/5 | 2/2 | 
| GPT-4 |  | 3 | 0/3 | 0/1 | 5 | 2/5 | 2/2 | 
| GPT-5-mini |  | 3 | 0/3 | 0/1 | 5 | 2/5 | 2/2 | 

Cisco’s lower Q5 recall (1/2) reflects reporting skigimeetroc.com (the installer domain) instead of skansnekssky.com (a C2 domain). For Q4, Claude, DeepSeek, Cisco, and Ollama all identified the initial infection vector (80.77.25.175), though with varying precision—Claude and DeepSeek reported additional indicators (5–6 total), while Cisco and Ollama were more focused (3 each). The GPT models reported only C2 domains for Q4, missing the initial redirect IP entirely. GPT-5.2 and GPT-4o correctly distinguished the user account from the hostname on Q3, while GPT-4 and GPT-5-mini did not.

## Appendix I IcedID Dataset Complexity

Here we present some aspects that make the IcedID malware particularly challenging, and how our system uncovers attack indicators.

#### Multi-Host Environment with Mixed Traffic.

The capture contains traffic from three Windows hosts in an Active Directory environment, with only one confirmed compromise. DESKTOP-SFF9LJF (10.4.19.136) follows the documented IcedID chain: Firebase-hosted installer, HTTP binary retrieval, persistent HTTPS C2 beaconing, and BackConnect activity. Other hosts in the environment (including DESKTOP-RETP4BU at 10.4.19.138) generate background traffic that includes DNS queries and web requests unrelated to the IcedID infection. This multi-host traffic creates analytical noise, as there is no structural boundary separating the infected host’s footprint from routine AD activity.

#### Volume as a Misleading Signal.

Domain join sequences and routine AD operations from uninfected hosts produce heavy Kerberos and LDAP bursts that are volumetrically louder than the infected host’s quieter but diagnostically significant IcedID C2 beaconing, making raw traffic volume an unreliable primary indicator in this capture.

#### Reference Set Scope.

The Unit 42 reference answers cover six IOCs for a single host. During evaluation, our system surfaced additional indicators confirmed valid upon manual investigation:

- •
Additional C2 domain. Our system cited spakernakurs.com resolving to 104.168.53.18, identical to askamoshopsi.com—and absent from the Unit 42 writeup. Manual lookup confirmed the domain resolves to shared IcedID infrastructure, consistent with a rotation or replacement C2 domain.
- •
Beaconing regularity. Our system’s classification of skansnekssky.com as persistent C2 activity prompted tshark verification, confirming 302-second intervals with sub-second jitter across 69+ sessions, a pattern unquantified in the reference answers.

#### Query Adaptation.

The IcedID installer delivery via Firebase Storage (firebasestorage.googleapis.com) required query modification: the standard *googleapis.com* exclusion for noise reduction would suppress the entire infection vector. We replaced broad wildcards with surgical per-subdomain exclusions and added two aggregations: (1) direct-IP TLS connections, recovering BackConnect C2 at 193.149.176.100, and (2) HTTP requests to raw IP hosts, recovering the redirect server at 80.77.25.175. This adaptation illustrates how attackers exploit common filtering heuristics and the need for dataset-aware query refinement.
