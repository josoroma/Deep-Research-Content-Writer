---
source_id: S-13
url: https://arxiv.org/html/2502.18836v1
title: 'REALM-Bench: A Real-World Planning Benchmark for LLMs and Multi-Agent Systems'
author: Longling Geng email gll; Stanford; CA; USA
published: null
fetched: '2026-10-09T21:42:07Z'
word_count: 5357
---
# REALM-Bench: A Real-World Planning Benchmark for LLMs and Multi-Agent Systems

# REALM-Bench: A Real-World Planning Benchmark 

for LLMs and Multi-Agent Systems

###### Abstract.

This benchmark suite provides a comprehensive evaluation framework for assessing both individual LLMs and multi-agent systems in real-world planning scenarios. The suite encompasses eleven designed problems that progress from basic to highly complex, incorporating key aspects such as multi-agent coordination, inter-agent dependencies, and dynamic environmental disruptions. Each problem can be scaled along three dimensions: the number of parallel planning threads, the complexity of inter-dependencies, and the frequency of unexpected disruptions requiring real-time adaptation. The benchmark includes detailed specifications, evaluation metrics, and baseline implementations using contemporary frameworks like LangGraph, enabling rigorous testing of both single-agent and multi-agent planning capabilities. Through standardized evaluation criteria and scalable complexity, this benchmark aims to drive progress in developing more robust and adaptable AI planning systems for real-world applications.

###### Keywords:

LLMs, Multi-Agent Systems, Planning Benchmark
## 1. Introduction

As large language models (LLMs) continue to advance in reasoning and planning, as demonstrated by OpenAI’s GPT-4o-Task ([OpenAI, 2024](https://arxiv.org#bib.bib20)), DeepSeek’s R1 ([DeepSeek-AI et al., 2025](https://arxiv.org#bib.bib10)), Anthropic’s Claude 3.5 Sonnet ([Anthropic, 2024](https://arxiv.org#bib.bib2)), and Gemini ([Team et al., 2023](https://arxiv.org#bib.bib25)), the research community is increasingly focusing on developing multi-agent systems (MAS) powered by these models. Recent innovations include AutoGen ([Wu et al., 2024](https://arxiv.org#bib.bib26)), CAMEL ([Li et al., 2023](https://arxiv.org#bib.bib17)), CrewAI ([Moura, 2024](https://arxiv.org#bib.bib19)), LangGraph ([LangChain AI, 2024](https://arxiv.org#bib.bib16)), Dspy ([Khattab et al., 2023](https://arxiv.org#bib.bib15)), and XAgent ([XAgent Team, 2023](https://arxiv.org#bib.bib27)), among others.
Although individual LLMs demonstrate significant capabilities, their true potential is realized when they collaborate
to tackle complex real-world problems ([Chang, 2024](https://arxiv.org#bib.bib6)).

Most AI benchmarks emphasize perception, language understanding, or basic reasoning. However, real-world challenges, such as supply chain management, disaster response, healthcare logistics, and investment strategies, demand coordinated planning and decision-making among specialized agents. There is a pressing need for robust benchmarks that can evaluate the performance of both single-agent systems and MAS in these complex, high-stakes domains.

### 1.1. The REALM Benchmark Suite

REALM-Bench (Real-world Planning Benchmark for LLMs and Multi-Agent Systems) addresses the need for rigorous evaluation with carefully curated planning challenges. These scenarios are designed to be both tractable, enabling human validation and debugging, and sufficiently complex to push the boundaries of current AI systems. Each challenge requires reasoning and validation over sequential actions
parallel processes, resource constraints, and unexpected disruptions
([Chang, 2025](https://arxiv.org#bib.bib7); [Chang, 2023b](https://arxiv.org#bib.bib5); [Chang, 2023a](https://arxiv.org#bib.bib4); [Chen et al., 2024](https://arxiv.org#bib.bib8); [Huang et al., 2024](https://arxiv.org#bib.bib14)).

The suite consists of eleven scenarios that progressively increase in complexity across three key dimensions:

1. 1.
Parallel Planning Threads: The number of concurrent planning processes that must be coordinated.
2. 2.
Inter-Dependencies: The complexity of relationships and constraints between these planning threads.
3. 3.
Disruption Frequency and Impact: The rate and severity of unexpected events that require the adaptation of the plan.

Next, we describe how each scenario can be scaled along these three dimensions.

### 1.2. Benchmark Scalability

While the base versions of each scenario enable detailed analysis and debugging, they can be scaled along the three dimensions defined above: parallel planning threads, inter-dependencies, and disruption frequency and impact.

For example, an urban ride-sharing scenario becomes increasingly complex as the number of vehicles and passengers grows, with interdependent carpooling routes and frequent traffic disruptions necessitating real-time plan adjustments.

This scalability allows AI planning systems to be evaluated under progressively challenging conditions, while still allowing detailed analysis of failure modes in simpler scenarios.

### 1.3. Availability and Access

The REALM-Bench Suite V1.0 is available on GitHub ([Geng and Chang, 2025](https://arxiv.org#bib.bib12)). In addition, we plan to host competitions and workshops at major AI conferences in 2025 to foster community engagement and further development.

## 2. Related Benchmark

Planning benchmarks have evolved from testing basic STRIPS-style planning to evaluating increasingly sophisticated planning capabilities. The International Planning Competition (IPC) has been a primary driver of planning benchmarks since 1998, using PDDL to specify domains like BlocksWorld, Logistics, and Rovers ([Taitler et al., 2024](https://arxiv.org#bib.bib24)). While valuable for testing classical planning algorithms, these benchmarks focus on deterministic environments with complete information and lack the dynamic disruptions common in real-world scenarios.

More recent benchmarks, such as the Process Planning Competition (PPC), have shifted toward continuous processes and temporal constraints ([Smith and Johnson, 2020](https://arxiv.org#bib.bib23)). Their manufacturing scenarios include parallel activities and resource dependencies, but the disruptions remain limited to machine breakdowns with known repair distributions. Similarly, the Dynamic Planning Competition introduces environmental changes during plan execution, yet it focuses primarily on path planning and navigation scenarios ([Doe and Roe, 2022](https://arxiv.org#bib.bib11)).

The annual Automated Negotiation Agents Competition (ANAC), established in 2010, has evolved to incorporate planning elements within its supply chain scenarios ([Miller and Davis, 2023](https://arxiv.org#bib.bib18)). However, its scope remains primarily focused on bilateral negotiations rather than comprehensive planning under uncertainty. For example, the 2024–25 competition featured a main challenge titled “Split the Pie,” an artificial yet simplified negotiation scenario where agents divide resources between parties. The supply chain problems in ANAC do not involve contingency planning, resource reallocation, or adaptation to unexpected disruptions.

Specifically for testing LLMs’ planning capabilities, TimeBench ([Chu et al., 2023](https://arxiv.org#bib.bib9)) and TaskBench ([Shen et al., 2023](https://arxiv.org#bib.bib22)) represent two approaches to evaluating AI planning. TimeBench focuses on temporal reasoning by testing systems’ ability to understand time dependencies and scheduling constraints, though it often relies on synthetic scenarios that fail to capture the dynamic nature of real-world temporal relationships, where deadlines shift and durations remain uncertain. TaskBench, on the other hand, evaluates practical task automation and step-by-step planning; it provides valuable insights into an AI system’s ability to decompose complex goals into manageable steps, but its scenarios may oversimplify the challenges of real-world automation, where outcomes are uncertain and processes are deeply interconnected.

This landscape reveals several gaps in existing benchmarks:

1. 1.
Limited Disruption Modeling: Most benchmarks treat uncertainties as static probability distributions rather than dynamic, interdependent events that can cascade through systems.
2. 2.
Simplified Dependencies: Real-world planning problems involve rich networks of temporal, resource, and causal dependencies that exceed the complexity found in current benchmarks.
3. 3.
Restricted Scope: Benchmarks tend to focus on specific subproblems (path planning, task allocation, etc.) rather than end-to-end planning scenarios that combine multiple challenges.
4. 4.
Artificial Constraints: Many benchmarks use simplified representations (like PDDL) that cannot capture the nuanced constraints and objectives found in real-world planning problems.
5. 5.
Limited Scalability: Few benchmarks allow systematic scaling of complexity along multiple dimensions while maintaining problem tractability for analysis.
6. 6.
LLM Specific Challenges: Although LLMs have achieved remarkable successes, the transformer architecture exhibits certain limitations. For example, an attention sink phenomenon can cause certain tokens to be neglected, potentially skewing model predictions ( [Xiao et al., 2024](https://arxiv.org#bib.bib28) ). Additionally, maximum likelihood training can introduce biases that limit output diversity and quality ([Holtzman et al., 2020](https://arxiv.org#bib.bib13) ;[Chang, 2023b](https://arxiv.org#bib.bib5) ). Finally, chain-of-thought approaches may suffer from pitfalls such as error propagation and inconsistent reasoning ([Brown et al., 2020](https://arxiv.org#bib.bib3) ;[Prystawski et al., 2023](https://arxiv.org#bib.bib21) ). A test suite should specifically examine these LLM-related issues.

Our proposed REALM-Bench addresses these limitations by providing scenarios that combine dependencies, dynamic disruptions, and scalability while remaining tractable for systematic evaluation. This allows testing of planning systems under conditions that better reflect the challenges of real-world applications.

## 3. Benchmark Structure

Problems are categorized into three difficulty levels based on the number of parallel execution threads, the complexity of dependencies, and real-time disruptions.

### 3.1. Entry Level (1-2 threads)

Problems focusing on basic coordination with limited dependencies:

- -
Single or dual thread execution
- -
Basic timing and resource constraints
- -
Simple disruption scenarios
- -
Example: Campus tour coordination with one and two groups

### 3.2. Intermediate (3-4 threads)

Problems requiring significant coordination across multiple execution paths:

- -
Three to four parallel threads
- -
Complex timing dependencies
- -
Resource sharing constraints
- -
Example: Wedding logistics with multiple vehicles and tasks

### 3.3. Advanced (5+ threads)

Problems with real-world complexity:

- -
Five or more parallel threads
- -
Complex inter-dependencies
- -
Multiple resource conflicts
- -
Dynamic disruption scenarios
- -
Example: Thanksgiving dinner coordination, natural disaster relief, and supply chain management

### 3.4. Evaluation Metrics

Each problem is evaluated across five key dimensions:

- -
Planning Quality: Effectiveness of initial plan generation
- -
Coordination: Management of parallel thread execution
- -
Adaptation: Response to disruptions and changes
- -
Resource Management: Resolution of resource conflicts
- -
Constraint Satisfaction: Maintenance of problem constraints

## 4. Benchmark Problem Specifications

REALM-Bench comprises eleven foundational problem frameworks that systematically evaluate both sequential and reactive planning. Building on the key dimensions introduced earlier (parallel threads, inter-dependencies, and dynamic disruptions), these frameworks progress from straightforward single-thread execution to complex multi-agent scenarios with real-time challenges.

##### Considerations #1 Problem Complexity:

Each framework can be further scaled to create more challenging variants:

- @itemi
Expanding the scale of agents and resources (e.g., from dozens to thousands)
- @itemi
Widening geographic distribution (e.g., local to global)
- @itemi
Increasing disruption frequency and severity (e.g., isolated events to cascading failures)
- @itemi
Introducing uncertainties in execution times and outcomes (e.g., probabilistic durations)
- @itemi
Adding hierarchical dependency networks (e.g., sub-networks with internal dependencies)
- @itemi
Accounting for agent properties (e.g., atomicity, idempotency)

This extensible design enables researchers to incrementally assess their systems’ capabilities while preserving each scenario’s fundamental planning challenge.

##### Considerations #2 Implementation:

Three main approaches can be used to tackle these problems:

- •
Rudimentary Manual Approach: Hand-craft a directed graph, choose a solver, and input parameter values to obtain a solution. Although direct, this method demands considerable human effort and domain expertise.
- •
LLM-Assisted Semi-automation: Use an LLM to suggest algorithms, extract parameters from specifications, and assist with coding. This approach can handle moderate complexity but becomes less feasible at scale.
- •
Full Automation: Provide the problem statement to a multi-agent framework (e.g., MACI ( [Chang, 2025](https://arxiv.org#bib.bib7) )) that executes end-to-end, including validation and replanning. This approach, combined with human oversight, scales best for complex scenarios with large numbers of nodes and frequent environmental changes.

### 4.1. P1: Campus Single-Tour Navigation

Problem Statement: A single autonomous agent must navigate a predefined campus environment to complete a sequence of waypoints while minimizing travel time. The scenario assumes a static environment without disruptions.

Problem Specification:

- -
Environment: A known map with a finite set of locations.
- -
Goal: Visit all designated waypoints within a given timeframe.
- -
Constraints: Opening hours of each location, each location at least 30 minutes, and must be completed before 5 PM.
- -
Optimization Metric: Shortest path (time or distance).

A meta-plan, shown in Table [1](https://arxiv.org#S4.T1), provides the high-level structure and constraints for the problem. This meta-plan serves as input to specialized solvers, such as dynamic programming or Monte Carlo algorithms, which then generate detailed, executable workflows. The process transforms abstract planning requirements into concrete, implementable sequences of actions while respecting all specified constraints and optimization objectives.

### 4.2. P2: Multi-Group Campus Tour

Problem Statement: Multiple groups of visitors require guided tours in different locations on a university campus, with optimized scheduling of multiple tour guides. This problem shares the same metrics as P1.

Problem Specification:

- -
Multiple agents (tour guides) must coordinate to serve different groups of visitors.
- -
Each group has predefined preferences and time constraints.
- -
Agents must follow non-overlapping paths while minimizing idle time.
- -
Location visiting hours must be observed.

### 4.3. P3: Urban Ride-Sharing (URS)

Problem Statement: Optimize real-time ride assignments for multiple vehicles and passengers in an urban environment, balancing efficiency, fuel use, and service quality.

Problem Specification:

- -
City Map: A graph where locations and roads have distances and travel times.
- -
Ride Requests: A set of requests , each defined by: 
  - –
Passenger ID, pickup/drop-off locations, time windows.
- –
- -
Vehicles: A set of available vehicles , each with: 
  - –
Location, battery/fuel level, passenger capacity and speed.
- –

### P4: Urban Ride Sharing (URS) with Disruptions

Problem Specification: Details are provided in Table [4](https://arxiv.org#S4.T4), including two disruption scenarios: airport route traffic delay and local road closure. Other possible disruptions could involve cancelation of passengers or late arrivals.

### P5: Wedding Reunion

Problem Specification: Table [5](https://arxiv.org#S4.T5) presents a coordinated wedding event travel problem. Several friends arrive at different times and locations before a 3:00 PM wedding photo session. The challenge includes managing two vehicles for airport pick-ups (aimed at those who cannot drive or wish to cut costs) and completing critical errands, such as collecting the wedding gift and retrieving formal attire from the tailor. All activities must be scheduled to ensure that everyone arrives at the wedding venue before the photo time.

This problem introduces more constraints than the URS problems in P3 and P4, and it also lays the groundwork for a more challenging disruption case discussed in P8.

### P6: Thanksgiving Dinner

Consider a Thanksgiving dinner scenario in which a family of five must return home in a Boston suburb for dinner. The problem involves coordinating departure times, managing travel logistics (including possible traffic delays), and ensuring timely arrival. Table [6](https://arxiv.org#S4.T6) formalizes these challenges as a sequential planning problem.

This scenario also lays the groundwork for a more advanced disruption case, which has proven difficult for standalone LLMs, as discussed in P9.

Problem Specification:

Setup:

- @itemi
Mom (Sarah) hosts dinner at 6:00 PM in Boston.
- @itemi
Family arrivals: 
  - –
Dad (James) from San Francisco, lands at 1:00 PM ET.
  - –
Sister (Emily) from Chicago lands at 2:30 PM.
  - –
Brother (Michael) driving from NY arrives at 3:00 PM.
- –
- @itemi
Grandma, who is healthy, needs to pick up nearby.

Constraints:

- @itemi
James must rent a car post-landing.
- @itemi
Emily needs an airport pickup (no alternatives).
- @itemi
Turkey requires 4 hours to cook; someone must be home once it’s in the oven for safety.
- @itemi
Side dishes need 2 hours of preparation.
- @itemi
Travel times: 
  - –
Home to BOS Airport: 1 hour.
  - –
BOS Airport to Grandma’s: 1 hour.
  - –
Home to Grandma’s: 30 minutes.
- –

Key Planning Questions:

1. 1.
When should cooking start?
2. 2.
Who picks up Emily, and when?
3. 3.
When and by whom should Grandma be picked up?

### P7: Disaster Relief Logistics Problem

### P8: Wedding Reunion with Disruptions

Problem Extension: This problem extends P5 with road closures and dynamic rerouting.

The disruption scenario becomes more challenging because, when a road closure is announced, the planner must know each vehicle’s current location to determine whether it is affected. Since LLMs are inherently stateless, they cannot keep track of previous scheduling events and thus struggle to adapt the plan in real-time.

### P9: Thanksgiving Dinner with Disruptions

This problem extends P6 by introducing flight delays. Specifically, when a flight from SFO to BOS is delayed by hours, the new arrival time is confirmed at the originally expected arrival time minus the flight’s scheduled duration. Although this early notice provides an opportunity to adjust travel and dinner plans, current LLM-based systems fail to leverage this information in a timely manner, only beginning to react at the original arrival time and missing the window for earlier intervention.

For example, consider James’s flight, which was originally scheduled to arrive in Boston at 1 PM but has been delayed to 4 PM. He learns of this new arrival time at 10 AM EST (the flight’s intended departure from SFO), offering a three-hour lead for adjustments. However, existing LLM-based solutions do not adapt the plan until 1 PM, thus squandering the opportunity to re-optimize the schedule.

### P10: Global Supply Chain

| Component | Details | 
|---|---|
| GPU Procurement & Shipments |  | 
| Total GPU Target | 100,000 units | 
| Vendors |  | 
| Order Timing | All orders placed on Day 1 | 
| Shipment Schedule | Quarterly shipments; e.g., a 600,000 unit order results in 3 shipments of 200,000 units at the end of Q1, Q2, and Q3 | 
| Payment Terms | 50% deposit at order (day 1), 50% at delivery (each quarter) | 
| Natural Disaster Impacts |  | 
| Risk Probabilities | Earthquake: 10% per quarter; Typhoon: 10% per quarter (assessed over entire project) | 
| Delay Impact | Cascading 1-month delay on all subsequent shipments if a disaster occurs in a quarter | 
| Cost Impact | 30% price increase applied only to the affected quarter’s shipment | 
| Shipment Expedition Impact | Expedite one shipment by 1 month and all subsequent shipments are moved up by 1 month (lock stepped) | 
| Cluster Construction & Infrastructure |  | 
| Cluster Definition | Each cluster requires 50,000 GPUs; clusters can be built concurrently once required GPUs are delivered | 
| Networking Infrastructure (per cluster) |  | 
| Duration | 1 months | 
| Cost | $25 million | 
| Dependencies | Can begin only after GPUs have arrived, power is ready, and cooling is operational | 
| Power & Cooling (per cluster) |  | 
| Requirements | Power: 150 MW; Cooling: 1M gallons/day | 
| Lead Time Options |  | 
| Testing & Certification (per cluster) |  | 
| Normal Process | 2 months, $15 million | 
| Expedited Process | 1 month, $45 million (150% cost premium) | 
| Expedition Options | Expedite power/cooling, networking (50% time reduction, 150% cost premium), and testing independently per cluster | 
| Business Impact of Delays |  | 
| Delay Costs | $50 million lost revenue + $10 million additional operating costs per month of delay | 
| Overall Objective |  | 
| Objective | Minimize the end-to-end construction cost (procurement, construction, maintenance, delay costs, expedition premiums) while meeting the 15-month deadline. If the 15-month not met, adding delay costs | 

| NVIDIA: $15k/unit, 200k units/quarter capacity, 20% maintenance risk (of unit price over 1 year) | 
| AMD: $10k/unit, 150k units/quarter capacity, 50% maintenance risk (of unit price over 1 year) | 

| Regular: 2 months at $30M per cluster | 
| Expedited: 1 months at $75M per cluster (150% cost premium) | 

Table [8](https://arxiv.org#S4.T8) presents a comprehensive problem in data center GPU deployment that captures the complexity of large-scale infrastructure projects. The objective is to complete a 1 million GPU data center in 15 months while minimizing total costs. The problem encompasses procurement decisions between NVIDIA (k/unit) and AMD (k/unit) GPUs, where each vendor has different maintenance risks (20% vs 50% of unit price over one year) and quarterly shipment capacities.

The construction process is organized around 50,000 GPU clusters, which require coordinated deployment of power, cooling, and networking infrastructure. Each cluster demands significant resources: 150 MW of power capacity and 1 million gallons per day of cooling water. Infrastructure development follows strict dependencies: Power and cooling systems must be operational before networking installation can begin, and each cluster must complete testing before becoming operational.

The problem incorporates real-world complexities such as risks of natural disasters (10% probability per quarter for both earthquakes and typhoons), which can cause cascading delays and cost increases. Management can expedite various components; power / cooling installation can be accelerated from 4 to 2.5 months for a 80% cost premium, while testing can be shortened from 2 to 1 month by doubling the cost.

The financial implications are significant, as each month of delay incurs M in combined revenue loss and additional operating costs. This creates a complex optimization challenge: balancing procurement costs, expedition premiums, and risk mitigation strategies while adhering to physical and temporal constraints in the construction sequence.

### P11: Stock Prediction/Forecasting

Consider a stock market prediction scenario where an automated system must forecast future stock prices while integrating multiple data streams and accounting for market dynamics. The problem involves processing real-time data, managing prediction updates, and responding to market events. Table [9](https://arxiv.org#S4.T9) formalizes this as a sequential planning problem, presenting a comprehensive framework for building an adaptive prediction system. The problem statement details the requirements for creating a robust prediction pipeline that can handle real-time market data, maintain high accuracy, and adapt to changing market conditions. A sample workflow demonstrating the system’s architecture and data flow is provided in Table [9](https://arxiv.org#S4.T9).

Problem Specification:

Setup:

- @itemi
Objective: Predict a portfolio of stock prices for time , enabling actionable insights for risk management, investment decisions, and automated trading.
- @itemi
Historical Data: 
  - –
Training period: 2010–2020.
  - –
Validation period: 2021–2023.
  - –
Real-time data feed required during operation.
- –
- @itemi
Data Sources: Yahoo Finance, SEC EDGAR, news feeds, macroeconomic indicators.
- @itemi
Required Features: 
  - –
Technical Indicators: MA, MACD, RSI, Bollinger Bands.
  - –
Market Context: Sector indices, competitor stock performance, correlation metrics.
  - –
External Events: Economic reports, policy changes, earnings announcements.
  - –
Sentiment Analysis: Real-time news, social media, financial disclosures.
- –

Constraints:

- @itemi
Processing latency: Under 5 minutes for real-time predictions.
- @itemi
Prediction confidence interval: 95% confidence bounds required.
- @itemi
Model Dependencies: 
  - –
Data collection before feature extraction.
  - –
Feature extraction before model training.
  - –
Model training before prediction generation.
- –
- @itemi
Performance Requirements: 
  - –
Mean Absolute Percentage Error (MAPE) 5% on validation.
  - –
False alert rate 1%.
  - –
System uptime 99.9% during market hours.
- –

State Space:

- @itemi
Processing Nodes (): 
  - –
Data Nodes: DC (data collection), FE (feature extraction).
  - –
Model Nodes: MT (model training), PG (prediction generation).
  - –
Integration Nodes: IG (integration), AG (alert generation).
- –
- @itemi
Dependencies (): 
  - –
Pipeline: .
  - –
Feedback: for adaptive updates.
  - –
External: Market events affect all nodes.
- –

Market Regime Adaptation:

- @itemi
Detect shifts in volatility, liquidity, and trend strength.
- @itemi
Adjust prediction models based on regime detection.
- @itemi
Implement fallback strategies for extreme market shifts.

Adaptive Refresh Rates:

- @itemi
(data collection) adjusts based on market volatility.
- @itemi
(news updates) increases during high-impact events.

Decision Module:

- @itemi
Trading Strategy: Buy/sell signals, stop losses, risk thresholds.
- @itemi
Risk Assessment: Hedging, diversification, leverage constraints.
- @itemi
Dynamic Adjustment: Rebalancing frequency, asset weighting, market response.

Backtesting and Iterative Validation:

- @itemi
Run models on historical data to evaluate predictive accuracy.
- @itemi
Compare performance on different market regimes/conditions.
- @itemi
Adjust hyperparameters based on validation results.

### 4.4. Execution Example: Urban Ride Sharing

For a benchmark suite, we encourage users to devise novel methodologies to solve the problems. However, for this illustrative example of Urban Ride Sharing (URS) (P3), we employ a customized specification language that extends PDDL (Planning Domain Definition Language) and workflow networks to support:

- -
Dynamic constraints and real-time updates.
- -
Integration with streaming data sources.
- -
Explicit representation of uncertainty.
- -
Temporal and spatial dependencies.

The solver, whether manual or automatic, approaches the planning problem in three steps:

1. 1.
Convert the problem statement into a formal specification: 
  - -
Key objectives and constraints.
  - -
Required resources and their capabilities.
  - -
Performance metrics and success criteria.
  - -
Temporal and spatial dependencies.
2. -
3. 2.
Transform the specification into a workflow graph: 
  - -
Nodes represent processing stages, decision points, or actions.
  - -
Edges capture dependencies, data flow, and execution sequence.
  - -
Agents are assigned to both nodes and edges.
  - -
Concrete parameters and thresholds are specified.
4. -
5. 3.
Select and apply solving algorithms: 
  - -
Test multiple solution approaches (e.g., dynamic programming, Monte Carlo).
  - -
Evaluate solutions against specified metrics.
  - -
Select and validate the best-performing solution.
  - -
Present results with performance analyses.
6. -

We walk through these three steps to solve the URS problem.

#### 4.4.1. URS Problem Specification

#### 4.4.2. URS Workflow

#### 4.4.3. URS Results

Figure [3](https://arxiv.org#acmlabel2) presents an optimal solution with a total travel distance of 87 km, outperforming both GPT-4o-Task and DeepSeek R1 (Figure [4](https://arxiv.org#acmlabel3)), which require 123 km. This represents a significant improvement of 41.37%.

##### Extended Materials

We also used LangGraph to implement both P3 and P4, as presented in Appendix [A](https://arxiv.org#A1). Furthermore, we provide a solution to P11 for the prediction of the stock value. These sample implementations validate the completeness of the problem statements in this benchmark.

## 5. Conclusion

REAL-Bench represents a significant step toward systematically evaluating AI systems’ capabilities in real-world planning scenarios. By providing 11 carefully designed problems that progress in complexity, the benchmark enables researchers to:

- -
Assess planning capabilities in multiple dimensions of difficulty.
- -
Test system performance on real-world planning challenges.
- -
Evaluate handling of unexpected interruptions and adaptations.
- -
Compare different approaches using standardized metrics.

The benchmarks are designed to be both tractable for systematic evaluation and challenging for current systems. Each problem can be scaled along multiple dimensions, including the number of parallel threads, complexity of dependencies, and frequency of disruptions, allowing researchers to progressively stress-test their systems. Inclusion of validation metrics and baseline implementations facilitates meaningful comparisons between different approaches.

Looking ahead, we envision this benchmark suite evolving with community contributions and feedback. Future extensions might include more complex scenarios, additional evaluation metrics, and expanded validation tools. For instance, in many workflows, transaction properties must be preserved:

- -
Atomicity: An operation either completes entirely or not at all, with no partial execution state (e.g., a ride-sharing trip must either complete fully or be canceled entirely).
- -
Idempotency: Multiple identical requests produce the same outcome as a single request, preventing duplicate actions (e.g., multiple identical order submissions should not result in multiple orders).

Most importantly, by providing a common framework for evaluating planning capabilities of both individual LLMs and multi-agent systems, we hope to accelerate progress toward more robust and capable AI planning systems that can handle real-world complexity and uncertainty. The REALM benchmark suite, along with detailed documentation and baseline implementations, will be available as an open source resource after the peer review process.

## References

- Anthropic (2024)
Anthropic. 2024.
Claude Technical Report.
[https://www.anthropic.com](https://www.anthropic.com)
- Brown et al. (2020)
Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. 2020.
Language Models are Few-Shot Learners.
*arXiv preprint arXiv:2005.14165* (2020).
- Chang (2023a)
Edward Y. Chang. 2023a.
CRIT: Prompting Large Language Models With the Socratic Method.
*IEEE  Annual Computing and Communication Workshop and Conference* (March 2023).
- Chang (2023b)
Edward Y Chang. 2023b.
Examining GPT-4’s Capabilities and Enhancement with SocraSynth. In *The  International Conf. on Computational Science and Computational Intelligence* .
- Chang (2024)
Edward Y. Chang. 2024.
*Multi-LLM Agent Collaborative Intelligence: The Path to Artificial General Intelligence* .
SocraSynth.com.[https://www.amazon.com/dp/1962463079](https://www.amazon.com/dp/1962463079)
- Chang (2025)
Edward Y. Chang. 2025.
MACI: Multi-Agent Collaborative Intelligence for Adaptive Reasoning and Temporal Planning.
arXiv:2501.16689 [cs.AI]
[https://arxiv.org/abs/2501.16689](https://arxiv.org/abs/2501.16689)
- Chen et al. (2024)
Junzhe Chen, Xuming Hu, Shuodi Liu, Shiyu Huang, Wei-Wei Tu, Zhaofeng He, and Lijie Wen. 2024.
LLMArena: Assessing Capabilities of Large Language Models in Dynamic Multi-Agent Environments. In *Proceedings of ACL* . Association for Computational Linguistics, 13055–13077.[doi:10.18653/v1/2024.acl-long.705](https://doi.org/10.18653/v1/2024.acl-long.705)
- Chu et al. (2023)
Zheng Chu, Jingchang Chen, Qianglong Chen, Weijiang Yu, Haotian Wang, Ming Liu, and Bing Qin. 2023.
Timebench: A Comprehensive Evaluation of Temporal Reasoning Abilities in Large Language Models.
*ArXiv preprint* (2023).
arXiv:2311.17667
- DeepSeek-AI et al. (2025)
DeepSeek-AI, Daya Guo, Dejian Yang, and more. 2025.
DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning.
arXiv:2501.12948 [cs.CL]
[https://arxiv.org/abs/2501.12948](https://arxiv.org/abs/2501.12948)
- Doe and Roe (2022)
J. Doe and R. Roe. 2022.
The Dynamic Planning Competition 2022: Challenges and Results. In *Proceedings of the International Conference on Automated Planning and Scheduling (ICAPS)* . ICAPS, Virtual.
- Geng and Chang (2025)
Longling Geng and Edward Y. Chang. 2025.
REALM-Bench Github Repository: A Real-World Planning Benchmark for LLMs and Multi-Agent Systems.
[https://github.com/genglongling/REALM-Bench](https://github.com/genglongling/REALM-Bench)
- Holtzman et al. (2020)
Ari Holtzman, Jan Buys, Li Du, Maxwell Forbes, and Yejin Choi. 2020.
The Curious Case of Neural Text Degeneration.
arXiv:1904.09751 [cs.CL]
[https://arxiv.org/abs/1904.09751](https://arxiv.org/abs/1904.09751)
- Huang et al. (2024)
Xu Huang, Weiwen Liu, Xiaolong Chen, Xingmei Wang, Hao Wang, Defu Lian, Yasheng Wang, Ruiming Tang, and Enhong Chen. 2024.
Understanding the planning of LLM agents: A survey.
arXiv:2402.02716 [cs.AI]
[https://arxiv.org/abs/2402.02716](https://arxiv.org/abs/2402.02716)
- Khattab et al. (2023)
Omar Khattab, Arnav Singhvi, Paridhi Maheshwari, Zhiyuan Zhang, and more. 2023.
DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines.
arXiv:2310.03714 [cs.CL]
[https://arxiv.org/abs/2310.03714](https://arxiv.org/abs/2310.03714)
- LangChain AI (2024)
LangChain AI. 2024.
LangGraph: Building Structured Applications with LLMs.
[https://github.com/langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) .
- Li et al. (2023)
Guohao Li, Hasan Abed Al Kader Hammoud, Hani Itani, Dmitrii Khizbullin, and Bernard Ghanem. 2023.
CAMEL: Communicative Agents for "Mind" Exploration of Large Language Model Society.
arXiv:2303.17760 [cs.AI]
[https://arxiv.org/abs/2303.17760](https://arxiv.org/abs/2303.17760)
- Miller and Davis (2023)
E. Miller and F. Davis. 2023.
Automated Negotiation Agents Competition 2023: Benchmarking Negotiation Strategies. In *Proceedings of the International Conference on Autonomous Agents and Multiagent Systems (AAMAS)* . IFAAMAS, Virtual.
- Moura (2024)
Joao Moura. 2024.
CrewAI Framework.
[https://github.com/joaomdmoura/crewAI](https://github.com/joaomdmoura/crewAI) .
- OpenAI (2024)
OpenAI. 2024.
Hello GPT-4o.
[https://openai.com/index/hello-gpt-4o/](https://openai.com/index/hello-gpt-4o/) Accessed: Jan. 30, 2025.
- Prystawski et al. (2023)
Bart Prystawski, M. Y. Li, and Noah Goodman. 2023.
Why think step by step? Reasoning emerges from the locality of experience. In *NeurIPS* .
- Shen et al. (2023)
Yongliang Shen et al. 2023.
Taskbench: Benchmarking large language models for task automation.
*arXiv preprint arXiv:2311.18760* (2023).
- Smith and Johnson (2020)
A. Smith and B. Johnson. 2020.
The Process Planning Competition 2020: An Overview. In *Proceedings of the International Conference on Automated Planning and Scheduling (ICAPS)* . ICAPS, Virtual.
- Taitler et al. (2024)
Ayal Taitler, Ron Alford, Joan Espasa, Gregor Behnke, Daniel Fišer, Michael Gimelfarb, Florian Pommerening, Scott Sanner, Enrico Scala, Dominik Schreiber, Javier Segovia-Aguas, and Jendrik Seipp. 2024.
The 2023 International Planning Competition.
*AI Magazine* 45, 2 (2024), 280–296.[doi:10.1002/aaai.12169](https://doi.org/10.1002/aaai.12169) arXiv:https://onlinelibrary.wiley.com/doi/pdf/10.1002/aaai.12169
- Team et al. (2023) Gemini Team, Rohan Anil, Sebastian Borgeaud, Yonghui Wu, Jean-Baptiste Alayrac, Jiahui Yu, Radu Soricut, Johan Schalkwyk, et al. 2023. Gemini: A Family of Highly Capable Multimodal Models. arXiv:2312.11805 [cs.CL]
- Wu et al. (2024)
Qingyun Wu, Gagan Bansal, Jieyu Zhang, Yiran Wu, and Chi Wang. 2024.
AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation. In *COLM 2024* .
- XAgent Team (2023)
XAgent Team. 2023.
XAgent: An Autonomous Agent for Complex Task Solving.
[https://github.com/OpenBMB/XAgent](https://github.com/OpenBMB/XAgent) .
- Xiao et al. (2024)
Guangxuan Xiao, Yuandong Tian, Beidi Chen, Song Han, and Mike Lewis. 2024.
Efficient Streaming Language Models with Attention Sinks.
arXiv:2309.17453 [cs.CL]
[https://arxiv.org/abs/2309.17453](https://arxiv.org/abs/2309.17453)

## Appendices

In these Appendices, we provide sample implementations of selected problems, illustrating that each problem specification is implementable and can produce feasible solutions. This serves as a verification of completeness for the problem definitions. We encourage readers to review the code and use it as a reference for designing improved solutions to these challenges.

The three problems selected are P3, P4, and P11, representing sequential planning, reactive planning, and the most complex planning scenario, respectively.

## Appendix A P3 & P4: Urban Ride Sharing Sample Implementation

This appendix presents an implementation of P3 and P4: Urban Ride Sharing without and with interrupts, using LangGraph ([LangChain AI, 2024](https://arxiv.org#bib.bib16)).

### A.1. Agentic Workflow Formulation

In this first stage, we define agents to manage the nodes of the workflow, including data collection, route planning, vehicle dispatch, traffic adjustment, monitoring and alert, and logging agents. At the end, we use the >> syntax to specify dependencies among agents. The transition from problem specifications to workflow formulation is handled automatically by MACI ([Chang, 2025](https://arxiv.org#bib.bib7)) in LangGraph.

### A.2. P3: Execute Meta Plan without Disruption

Now that the meta-plan workflow has been constructed, the second step involves providing real data for workflow execution. The following code snippet illustrates how vehicle and passenger locations are specified, followed by the corresponding agent executions.

### A.3. P4: Execute Meta Plan with Disruption

This section depicts the execution of the meta-plan (workflow) under traffic disruption. In this scenario, the system dynamically identifies traffic delays and integrates real-time updates into the planning process. Each agent plays a crucial role: the data collection agent continuously monitors traffic conditions; the route planning agent adjusts travel routes based on congestion data; and the dispatch agent ensures that vehicle assignments are optimized despite delays. The workflow demonstrates how coordinated agent interventions, including dynamic rerouting and schedule adjustments, effectively mitigate the impact of heavy traffic, maintaining timely transportation, and enhancing overall operational efficiency.

## Appendix B P11: Stock Prediction Sample Implementation on LangGraph

This appendix presents an implementation of the P11 Stock Prediction problem using LangGraph ([LangChain AI, 2024](https://arxiv.org#bib.bib16)). The implementation demonstrates how AI-driven planning can be applied to financial forecasting by leveraging historical data, technical indicators, and real-time market updates.

### B.1. Agentic Workflow Formulation

In this first stage, we define agents to manage the nodes of the workflow, including data collection, feature extraction, model training, integration, and alert. In the end, we use the >> syntax to specify dependencies among agents.

### B.2. Workflow Execution With Historical Data for Prediction

Following the dependency graph presented above (also see Figure 1), the agents are executed in sequence: starting with data collection, then feature extraction, followed by model training, and finally prediction. For brevity, while data for five stocks is provided, we illustrate the execution flow using only APPL.

### B.3. Output: Alert Generation

Based on the problem specification in Section [4](https://arxiv.org#S4.SSx8), when the prediction confidence is , a recommended trading action is sent to the subscriber as an alert.

Based on the above prediction, on 1/3, 1/5, and 1/7 the prediction confidence exceeds the threshold and the stock’s moving direction is up, down, and up, respectively. Therefore, the alerts issued before the opening of the market on those three days are: BUY, SELL, and STRONG BUY, respectively.
