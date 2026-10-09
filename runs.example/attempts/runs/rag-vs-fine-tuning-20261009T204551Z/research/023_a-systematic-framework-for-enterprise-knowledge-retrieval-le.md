---
source_id: S-23
url: https://arxiv.org/html/2512.05411v2
title: 'A Systematic Framework for Enterprise Knowledge Retrieval: Leveraging LLM-Generated
  Metadata to Enhance RAG Systems Thanks: Accepted to: 2026 IEEE Conference on Artificial
  Intelligence (CAI). © 2026 IEEE. Personal use of this material is permitted. Permission
  from IEEE must be obtained for all other uses, in any current or future media, including
  reprinting/republishing this material for advertising or promotional purposes, creating
  new collective works, for resale or redistribution to servers or lists, or reuse
  of any copyrighted component of this work in other works.'
author: Pranav Pushkar Mishra Affiliation Mokshit Bharat Surana; Fatemeh Sarayloo
published: null
fetched: '2026-10-09T20:53:47Z'
word_count: 5441
---
# A Systematic Framework for Enterprise Knowledge Retrieval: Leveraging LLM-Generated Metadata to Enhance RAG Systems Thanks: Accepted to: 2026 IEEE Conference on Artificial Intelligence (CAI). © 2026 IEEE. Personal use of this material is permitted. Permission from IEEE must be obtained for all other uses, in any current or future media, including reprinting/republishing this material for advertising or promotional purposes, creating new collective works, for resale or redistribution to servers or lists, or reuse of any copyrighted component of this work in other works.

###### Abstract

In enterprise settings, efficiently retrieving relevant information from large and complex knowledge bases is essential for operational productivity and informed decision-making. This research presents a systematic empirical framework for metadata enrichment using large language models (LLMs) to enhance document retrieval in Retrieval-Augmented Generation (RAG) systems. Our approach employs a structured pipeline that dynamically generates meaningful metadata for document segments, substantially improving their semantic representations and retrieval accuracy. Through a controlled experimental matrix, we compare three chunking strategies—semantic, recursive, and naive—and evaluate their interactions with three embedding techniques—content-only, TF-IDF weighted, and prefix-fusion—isolating the contribution of each component through ablation analysis. The results demonstrate that metadata-enriched approaches consistently outperform content-only baselines, with recursive chunking paired with TF-IDF weighted embeddings yielding 82.5% precision and naive chunking with prefix-fusion achieving the strongest ranking quality (NDCG 0.813). Our evaluation employs cross-encoder reranking for silver-standard ground truth generation, with statistical significance confirmed via Bonferroni-corrected paired -tests. These findings confirm that metadata enrichment improves vector space organization and retrieval effectiveness while maintaining sub-30 ms P95 latency, providing a quantitative decision framework for deploying high-performance, scalable RAG systems in enterprise settings.

## I INTRODUCTION

Efficiently retrieving and leveraging information from large-scale knowledge repositories is vital for modern organizational productivity and innovation. Retrieval-Augmented Generation (RAG) systems have emerged as a powerful paradigm for enhancing Large Language Models (LLMs) by integrating external knowledge sources [[16](https://arxiv.org#bib.bib16)]. This approach addresses inherent limitations of LLMs, such as knowledge cut-off dates, lack of domain-specificity, and hallucinations [[17](https://arxiv.org#bib.bib17)].

While effective for structured datasets, traditional retrieval methods often struggle with the complexity, scale, and dynamic nature of enterprise knowledge bases. Manual curation becomes impractical as repositories expand, and these methods are prone to overlooking relevant information in lengthy contexts, resulting in the ’Lost in the Middle’ phenomenon.

Recent advancements in LLMs offer transformative solutions. LLMs can process unstructured data, extract meaningful insights, and generate structured metadata aligned with semantic and contextual needs.Despite these developments, building effective RAG pipelines remains challenging, requiring management of large data volumes, optimization of retrieval strategies, and continual performance tuning.

This paper contributes a controlled empirical study that systematically isolates and quantifies the interactions between chunking strategies and metadata integration techniques within RAG pipelines—an axis of variation that prior metadata-aware retrieval work has not examined in a unified experimental framework. We propose MetaRAG, a structured pipeline where an LLM-based metadata enrichment module generates semantic, technical, and content annotations for document segments, which are then integrated into retrieval through three distinct embedding strategies. The resulting configuration matrix—spanning three chunking strategies (semantic, recursive, naive) and three embedding approaches (content-only, TF-IDF weighted, prefix-fusion)—is evaluated under standardized information retrieval metrics with full statistical rigor. Our principal contributions are:

1. 1.
A reproducible metadata enrichment pipeline that generates structured, multi-category annotations for document chunks using LLMs, integrated into retrieval via TF-IDF weighting and prefix-fusion embedding strategies.
2. 2.
A controlled factorial evaluation isolating the individual and interaction effects of chunking granularity and metadata integration technique on retrieval performance, including ablation analysis of metadata component contributions.
3. 3.
A practitioner-oriented configuration decision framework, grounded in statistically validated benchmarks (Bonferroni-corrected paired -tests, bootstrap confidence intervals), identifying optimal chunking–embedding pairings for different retrieval objectives.

## II Related Work

This section reviews recent advances in RAG architectures, metadata enrichment, and embedding optimization, and positions our contributions relative to the most closely related work.

### II-A RAG Architectures and Evaluation

RAG systems span a complexity spectrum from Naive RAG, which indexes and retrieves document chunks directly, through Advanced RAG with query rewriting and reranking, to Modular RAG with configurable pipeline components [[4](https://arxiv.org#bib.bib4)]. Lewis et al. [[1](https://arxiv.org#bib.bib1)] established the foundational RAG paradigm by combining parametric and non-parametric memory for knowledge-intensive tasks, while Shuster et al. [[2](https://arxiv.org#bib.bib2)] demonstrated hallucination reduction in conversational AI through retrieval augmentation. Chen et al. [[5](https://arxiv.org#bib.bib5)] introduced evaluation benchmarks revealing limitations in LLMs’ rejection and integration capabilities within RAG contexts.

Recent architectural innovations include GraphRAG [[21](https://arxiv.org#bib.bib21)], which constructs corpus-wide entity-relationship knowledge graphs via LLM extraction and applies community detection to generate hierarchical summaries for global sensemaking queries. While effective for corpus-level thematic questions, GraphRAG fundamentally replaces chunk-based vector retrieval and does not evaluate how chunking granularity or embedding strategies affect per-query retrieval quality. On the search side, Wang et al. [[7](https://arxiv.org#bib.bib7)] unified diverse search tasks under autoregressive text generation, Shao et al. [[14](https://arxiv.org#bib.bib14)] developed ITER-RETGEN for iterative retrieval-generation synergy, and Wang et al. [[15](https://arxiv.org#bib.bib15)] introduced Self-Knowledge Guided Retrieval for adaptive knowledge-gap recognition. These innovations address query routing and generation but do not examine how document-level preprocessing, specifically, metadata enrichment and chunking, affects retrieval effectiveness.

For automated evaluation, Saad-Falcon et al. [[11](https://arxiv.org#bib.bib11)] proposed ARES, which fine-tunes DeBERTa-v3-Large classifiers on synthetic data to judge context relevance, answer faithfulness, and answer relevance, applying Prediction-Powered Inference with human-annotated validation sets (150 samples). While ARES provides scalable system-level evaluation, it treats RAG pipelines as black boxes, ranking configurations without investigating how individual components (chunking strategy, embedding technique, metadata enrichment) contribute to retrieval quality.

### II-B Metadata Enrichment for Information Retrieval

Metadata is foundational to retrieval systems, yet traditional curation methods scale poorly to unstructured enterprise datasets. Sundaram and Musen’s FAIRMetaText framework [[6](https://arxiv.org#bib.bib6)] aligned metadata with FAIR principles using GPT-based embeddings, though performance varied across domains. Song et al. [[8](https://arxiv.org#bib.bib8)] applied taxonomy-guided few-shot prompting for metadata completion in Earth science datasets, improving completeness and accuracy within a narrow disciplinary scope.

Most closely related to our work, Mombaerts et al. [[9](https://arxiv.org#bib.bib9)] introduced Meta Knowledge Summaries, generating document-level metadata and synthetic QA pairs using Claude 3 Haiku. However, their approach *replaces* chunk-based retrieval entirely, embeds only synthetic questions for matching, not original document segments, and evaluates a single chunking baseline (256 tokens, 10% overlap) with a single embedding model, precluding analysis of how chunking and embedding choices interact. Harris et al. [[10](https://arxiv.org#bib.bib10)] demonstrated LLM-based text enrichment using ChatGPT 3.5 to holistically rewrite texts with bundled techniques (context enrichment, grammar correction, terminology normalization). While effective on select MTEB benchmarks, their approach produces monolithic rewrites without structured metadata separation, tests only a single embedding model on classification tasks rather than RAG retrieval, and provides no ablation isolating which enrichment components contribute to performance.

In contrast, our framework preserves original chunk content and enriches it with a generalizable three-category metadata taxonomy (content, technical, semantic) via prefix-fusion, maintaining separability between categories for component-level ablation within a full RAG pipeline.

### II-C Embedding and Retrieval Optimization

Karpukhin et al. [[3](https://arxiv.org#bib.bib3)] established that dense vector embeddings outperform sparse methods for open-domain retrieval. Cuconasu et al. [[13](https://arxiv.org#bib.bib13)] challenged traditional assumptions by showing that controlled injection of irrelevant documents can paradoxically improve RAG generation quality. Anantha et al. [[12](https://arxiv.org#bib.bib12)] proposed Context Tuning, which enriches *queries* with user-behavioral signals from context stores prior to retrieval, training a lightweight LambdaMART ranker for tool selection. Context Tuning operates entirely on the query side; our approach is complementary, enriching the *document side* with structured metadata to improve chunk embedding quality for document QA.

### II-D Research Gaps and Contributions

Despite the advances surveyed above, three critical gaps remain. First, existing studies lack a systematic evaluation of the *interplay* between chunking methods and embedding strategies: Meta Knowledge [[9](https://arxiv.org#bib.bib9)] tests one chunking–embedding pair, Harris et al. [[10](https://arxiv.org#bib.bib10)] omit chunking entirely, and ARES [[11](https://arxiv.org#bib.bib11)] evaluates systems without decomposing pipeline components. Second, no prior work provides a structured metadata taxonomy with ablation evidence quantifying individual category contributions to retrieval metrics. Third, GraphRAG [[21](https://arxiv.org#bib.bib21)] and Context Tuning [[12](https://arxiv.org#bib.bib12)] address complementary aspects (corpus-level sensemaking and query disambiguation) but neither optimizes chunk-level embedding representations.

Our framework addresses these gaps through: (1) a systematic experimental matrix crossing three chunking strategies with three embedding techniques, enabling controlled ablation; (2) a three-category metadata taxonomy (content, technical, semantic) with prefix-fusion preserving original content while enriching embeddings; and (3) a silver-standard pseudo-ground truth evaluation based on cross-encoder reranking, enabling reproducible assessment without human annotation.

## III Methodology

This section outlines the methodology, which involves a systematic pipeline for transforming raw technical documentation into optimized retrieval components. The primary research question examines how document chunking strategies, metadata generation techniques, and embedding approaches interact to impact retrieval accuracy and efficiency. The pipeline, from data ingestion to evaluation, is illustrated in Fig. [1](https://arxiv.org#S2.F1) and each subsection below corresponds to a stage in the architecture.

### III-A Document Processing and Chunking Strategies

We employ three distinct chunking approaches, summarized in Table [I](https://arxiv.org#S3.T1) and illustrated in the first part of Fig. [1](https://arxiv.org#S2.F1). Parameters for each strategy were configured to produce comparable chunk length distributions across the corpus, ensuring that observed performance differences primarily reflect boundary selection methodology rather than chunk size effects. Naive chunking serves as a fixed-size baseline. Recursive chunking preserves document structure by splitting at progressively finer delimiters (paragraph breaks, then sentence boundaries) only when necessary. Semantic chunking detects natural breakpoints via similarity drops between consecutive sentence embeddings and merges smaller fragments with their nearest semantic neighbors.

| Strategy | Boundary | Context | Granularity | 
|---|---|---|---|
| Naive | Fixed-size | None | Uniform | 
| Recursive | Structural | Overlap | Hierarchical | 
| Semantic | Embedding-based | Merge similar | Adaptive | 

### III-B Metadata Enrichment Pipeline

A central component of this study is the systematic generation of metadata to enhance retrieval performance, as illustrated in the Fig. [1](https://arxiv.org#S2.F1). Our LLM-based pipeline creates structured annotations for each document segment across three categories. Content metadata includes content type classification (procedural, conceptual, reference, warning, example), extracted keywords, entities, and code example detection. Technical metadata identifies primary and secondary categories, mentioned services, and referenced tools. Semantic metadata provides concise summaries, identifies user intents (how-to, debugging, comparison, reference), and generates potential user questions the chunk addresses.

The system processes chunks using a specialized LLM prompt engineered to extract structured metadata consistently, employing batched processing for efficiency and maintaining a consistent schema across chunking strategies.

### III-C Embedding Techniques

We evaluated the following distinct embedding approaches to represent document chunks in vector space:

#### III-C1 Snowflake Arctic-Embed Model

The Snowflake Arctic-Embed model is considered as the primary embedding framework. This model was selected for its superior performance on technical documentation and its ability to effectively capture domain-specific terminology. The arctic-embed-m variant offers an optimal balance between retrieval performance and computational efficiency, supporting the long contexts required for technical documentation [[19](https://arxiv.org#bib.bib19)].

### III-D Embedding Techniques

We employ the Snowflake Arctic-Embed model (arctic-embed-m, dimensions=1536) as the primary embedding framework, selected for its strong performance on technical documentation and domain-specific terminology [[19](https://arxiv.org#bib.bib19)]. Three embedding strategies leverage this model in different configurations:

1. 1.
Content-only embeddings generate vector representations using only the raw chunk text, serving as the baseline.
2. 2.
TF-IDF weighted embeddings combine content embeddings (weighted ) with TF-IDF vectors derived from metadata (weighted ), creating a hybrid representation. The optimal ratio is determined via sensitivity analysis (Section IV).
3. 3.
Prefix-fusion embeddings inject structured metadata directly into document text as formatted prefixes before encoding, allowing the model to jointly represent content and metadata in a unified vector.

| Chunking | : | HR@10 | MRR | NDCG | P@10 | 
|---|---|---|---|---|---|
| Semantic | 80:20 | 70.0 | 42.1 | 60.4 | 56.8 | 
|  | 90:10 | 70.0 | 45.6 | 61.7 | 58.5 | 
|  | 95:05 | 72.0 | 45.4 | 61.0 | 57.5 | 
| Naive | 80:20 | 87.5 | 49.0 | 67.1 | 59.3 | 
|  | 90:10 | 90.0 | 50.8 | 68.7 | 61.5 | 
|  | 95:05 | 90.0 | 50.6 | 68.4 | 61.3 | 
| Recursive | 80:20 | 75.0 | 45.3 | 67.6 | 60.2 | 
|  | 90:10 | 82.5 | 45.5 | 69.5 | 63.0 | 
|  | 95:05 | 77.5 | 46.2 | 71.1 | 64.5 | 

### III-E Retriever Architectures

We implement three retriever architectures, each corresponding to an embedding methodology as shown in Fig. [1](https://arxiv.org#S2.F1). The content retriever utilizes content-only embeddings for baseline similarity matching. The TF-IDF retriever combines content embeddings with metadata-derived TF-IDF vectors using the optimized weighting ratio. The prefix-fusion retriever leverages prefix-augmented embeddings with automatic intent detection for query enhancement.

Each retriever is instantiated across all three chunking strategies, yielding a experimental matrix of nine configurations. This design enables systematic analysis to isolate the effects of both chunking granularity and embedding methodology on retrieval performance.

### III-F Ground Truth Generation and Evaluation Framework

Since manual annotation at scale is prohibitive for technical documentation corpora, we adopt a silver-standard pseudo-ground truth derived from cross-encoder reranking. For each query, we retrieve the top 50 candidate chunks using each retriever configuration and score them using BAAI/bge-reranker-base [[20](https://arxiv.org#bib.bib20)], which jointly encodes query-chunk pairs to capture fine-grained interaction patterns that surpass bi-encoder models in relevance discrimination. Scores are normalized to  and thresholded at  to establish relevance labels.

This approach enables scalable, reproducible evaluation but introduces inherent limitations: relevance labels reflect model-based assessments rather than human judgments, and only chunks retrieved by at least one method enter the candidate pool (retrieval pool bias). Consequently, absolute metric values should be interpreted with caution, while relative comparisons between configurations—the primary focus of this study—remain valid and informative.

## IV Experimental Results

In this section, we present a comprehensive analysis of the experimental outcomes obtained from evaluating our proposed systems. We begin by discussing the dataset used, including its composition and inherent challenges, followed by a detailed description of the experimental setup encompassing data processing, chunking strategies, embedding techniques, and retrieval architectures. Subsequently, we systematically compare the performance of different components—such as semantic, recursive, and naive chunking methods—across various evaluation metrics. This structured comparison enables us to identify the strengths and limitations of each approach, providing valuable insights into the optimal configurations for enhancing retrieval accuracy and efficiency in enterprise knowledge management contexts.

### IV-A Data Corpus Composition and Experiment setup

Our study employed a carefully curated dataset derived from AWS S3 documentation [[22](https://arxiv.org#bib.bib22)], selected for its intricate structure and diverse content types. The corpus consists of four main components: the S3 User Guide (2,499 pages), the API Reference (3,013 pages), the S3 Glacier Developer Guide (558 pages), and the S3 on Outposts documentation (217 pages). This comprehensive dataset offers a realistic and challenging environment for assessing the effectiveness of metadata-enriched retrieval strategies in practical, real-world technical contexts.

We implemented our evaluation framework on technical documentation datasets processed through three distinct chunking strategies: recursive (max_tokens=512, overlap=128), naive (fixed_length=1024), and semantic (adaptive with max_tokens=1024). For each strategy, we generated embeddings using the Snowflake Arctic-Embed model (dimensions=1536) with three configurations: content-only, TF-IDF weighted, and prefix-fusion approaches. The TF-IDF weighting ratio was determined via a sensitivity analysis across chunking strategies (Table [II](https://arxiv.org#S3.T2)), which revealed that the 90:10 content-to-metadata ratio (, ) consistently maximized or matched peak performance across all three chunking methods. Metadata features function as a complementary signal, analogous to a seasoning effect, where a small proportion meaningfully improves disambiguation, but higher metadata weighting degrades retrieval by diluting the dominant semantic representation. All subsequent TF-IDF experiments adopt the 90:10 ratio accordingly.

Retrieval experiments were conducted using exact vector search with cosine similarity across varying  values. For silver-standard ground truth generation, we employed a cross-encoder reranking methodology using BAAI/bge-reranker-base [[20](https://arxiv.org#bib.bib20)] to establish relevance judgments with threshold . Statistical significance was assessed using paired -tests across all nine retriever configurations with Bonferroni correction () to control for family-wise error rate. Effect sizes are reported using Cohen’s , and 95% confidence intervals are computed via bootstrap resampling (1,000 iterations).

The evaluation query set comprises 100 queries manually curated to cover distinct technical documentation retrieval scenarios. Each query is annotated along multiple overlapping dimensions: intent, complexity, and domain coverage; to characterize the test set composition. Table [III](https://arxiv.org#S4.T3) summarizes the distribution across these dimensions. To prevent data leakage, none of the test queries were included in the few-shot prompts used during metadata generation; all evaluation was performed on held-out queries.

| Dimension | Category | % | 
| Intent | Procedural (How-to) | 62.5 | 
|  | Conceptual (Definition) | 32.5 | 
|  | Comparison / Reference | 5.0 | 
| Complexity | Complex | 80.0 | 
|  | Moderate | 20.0 | 
| Domain | S3 Core | 55.0 | 
|  | S3 API / Auth | 20.0 | 
|  | S3 Glacier | 12.5 | 
|  | S3 on Outposts | 12.5 | 

Performance evaluation employed standard information retrieval metrics: Hit Rate@10, Mean Reciprocal Rank (MRR), Normalized Discounted Cumulative Gain (NDCG), and precision. We maintained consistent query processing procedures and embedding dimensionality across all experimental configurations to isolate the effects of metadata enrichment and chunking strategies.

Metadata generation utilized GPT-4o (gpt-4o-2024-05-13) with controlled temperature (0.5) and structured output formats for consistency.

### IV-B Evaluation Metrics

We established a rigorous evaluation methodology as shown in Fig. [1](https://arxiv.org#S2.F1) to assess the impact of metadata enrichment on RAG performance. The evaluation utilized a test set of diverse technical queries executed against our documentation corpus. Our framework evaluates both retrieval effectiveness through standard information retrieval metrics and response quality through semantic and factual accuracy measurements.

For the retriever evaluation, we used standard information retrieval metrics:

- •
Hit Rate@k: Proportion of queries with at least one highly relevant document (above 95th percentile threshold based on ground truth reranker scores) in the top-k results
- •
Metadata Consistency: Consistency of document categories within top-k results, measuring the retriever’s tendency to return semantically coherent chunks
- •
Precision@k: Proportion of relevant documents among top-k results
- •
MRR (Mean Reciprocal Rank): Average reciprocal rank of first relevant document
- •
NDCG@k: Ranking quality based on graded relevance and positional importance.

### IV-C Embedding and Chunking Analysis

We first analyzed the structural quality of embeddings generated using different techniques and chunking methods. Table [IV](https://arxiv.org#S4.T4) reports Silhouette Scores (higher indicates better-defined clusters) and Davies-Bouldin Index (DBI; lower indicates more compact, well-separated clusters) across representative configurations.

| Chunking | Embedding | Silhouette | DBI | 
|---|---|---|---|
| Naive | Content-Only | 0.054 | 3.04 | 
| Semantic | TF-IDF | 0.028 | 3.77 | 
| Semantic | Prefix-Fusion | 0.039 | 3.12 | 
| Recursive | Prefix-Fusion | 0.051 | 3.14 | 

Prefix-fusion embeddings achieved a DBI of 3.12, substantially outperforming TF-IDF weighted embeddings (DBI = 3.77). This gap reflects a fundamental difference in fusion strategy: prefix-fusion allows the encoder to jointly process metadata and content as a unified input, enabling learned contextual relationships between the two, whereas TF-IDF weighting blends separately computed vectors via linear combination—an approach that assumes alignment between inherently dissimilar representation spaces. When metadata is sparse or generic, this post-hoc blending can pull combined embeddings toward irrelevant clusters, explaining the weaker vector space organization. Recursive chunking with prefix-fusion demonstrated competitive cluster structure (Silhouette = 0.051, DBI = 3.14), suggesting that hierarchical chunking preserves coherent semantic groupings.

Semantic chunking produced significantly more chunks (5,706) compared to recursive chunking (4,099), representing a 39% increase. While this results in a larger index size, the finer granularity provided by semantic chunking enables more precise retrieval targeting.

### IV-D Retriever Performance Analysis

Based on our evaluation metrics, retrieval performance demonstrates complex interactions between chunking strategies and embedding techniques. The Hit Rate@10 results (Table [V](https://arxiv.org#S4.T5)) reveal that naive chunking achieves the highest performance (0.900) with both TF-IDF and prefix-fusion embeddings, closely followed by recursive chunking with content-only and prefix-fusion (0.875). This contradicts conventional assumptions about semantic chunking superiority.

| Embedding | Hit Rate@10 |  |  | MRR@10 |  |  | NDCG@10 |  |  | Precision@10 |  |  | 
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|  | Sem | Naive | Rec | Sem | Naive | Rec | Sem | Naive | Rec | Sem | Naive | Rec | 
| Content | 0.788 | 0.713 | 0.875 | 0.669 | 0.538 | 0.713 | 0.730 | 0.669 | 0.782 | 0.733 | 0.640 | 0.783 | 
| Prefix-Fusion | 0.775 | 0.900 | 0.875 | 0.534 | 0.750 | 0.673 | 0.699 | 0.813 | 0.800 | 0.745 | 0.798 | 0.785 | 
| TF-IDF | 0.700 | 0.900 | 0.825 | 0.456 | 0.508 | 0.455 | 0.617 | 0.687 | 0.695 | 0.585 | 0.615 | 0.630 | 

For MRR, which evaluates ranking quality (Table [V](https://arxiv.org#S4.T5)), recursive chunking with content-only embeddings achieves 0.713, outperforming metadata-enriched approaches in the semantic configuration—likely because semantic chunking’s adaptive boundaries create variable-sized segments where metadata prefixes exert uneven influence, diluting ranking precision. Naive chunking with prefix-fusion demonstrates the strongest MRR (0.750), as uniform chunk sizes ensure consistent metadata integration, allowing the prefix to reliably prime the encoder’s interpretation of each segment.

NDCG scores (Table [V](https://arxiv.org#S4.T5)), which assess overall ranking quality with position weighting, favor naive chunking with prefix-fusion (0.813), followed by recursive chunking with prefix-fusion (0.800) and content-only (0.782). The precision metrics further confirm this pattern, with naive chunking and prefix-fusion achieving the highest precision (0.798), closely followed by recursive configurations (0.785).

These results demonstrate that no single configuration universally outperforms across all metrics, and that the method of metadata integration matters as much as its presence. TF-IDF weighting, which treats content and metadata as separate vector spaces blended post-embedding, shows diminishing returns as metadata weight increases—sparse metadata signals can dilute the stronger content representation without proportional retrieval benefit. Prefix-fusion avoids this by encoding metadata and content jointly, enabling the model to learn contextual dependencies rather than relying on assumed vector space alignment.

To quantify statistical reliability, Table [VI](https://arxiv.org#S4.T6) reports 95% bootstrap confidence intervals for the top-performing configurations under naive chunking. Paired -tests with Bonferroni correction confirm that the prefix-fusion configuration significantly outperforms the content-only baseline across all metrics (, Cohen’s ), indicating large effect sizes.

To isolate the contribution of individual metadata components, we conducted an ablation study using the prefix-fusion retriever with semantic chunking. As shown in Table [VII](https://arxiv.org#S4.T7), progressively removing metadata categories degrades retrieval quality, with the full metadata configuration achieving an NDCG of 0.699 compared to 0.615 for content-only—a 13.7% improvement attributable to metadata enrichment. The addition of semantic metadata to technical annotations yields further gains in MRR (0.510 vs. 0.460), confirming that LLM-generated semantic descriptions aid in ranking relevant chunks higher.

| Retriever | MRR | NDCG@10 | Prec.@10 | 
|---|---|---|---|
| Prefix-Fusion | 0.7500.121 | 0.8130.077 | 0.7500.085 | 
| TF-IDF | 0.5700.130 | 0.7170.080 | 0.5500.082 | 
| Content-Only | 0.5380.134 | 0.6690.093 | 0.5250.089 | 

| Active Components | HR@10 | NDCG@10 | MRR | 
|---|---|---|---|
| All Metadata | 0.775 | 0.699 | 0.519 | 
| Technical + Semantic | 0.775 | 0.683 | 0.510 | 
| Technical Only | 0.775 | 0.660 | 0.460 | 
| Content Only (No Meta) | 0.700 | 0.615 | 0.389 | 

Table [VIII](https://arxiv.org#S4.T8) reports retrieval latency measured at P50 and P95 percentiles. All configurations operate well within interactive thresholds, with P95 latencies below 30 ms. Prefix-fusion retrieval achieved the lowest median latency (12.7 ms), likely due to favorable vector distribution properties of the unified embedding. End-to-end index construction, comprising chunking and embedding generation for the full corpus, completed in approximately 7.4 seconds.

| Configuration | P50 (ms) | P95 (ms) | 
|---|---|---|
| Prefix-Fusion | 12.7 | 21.8 | 
| TF-IDF () | 17.7 | 19.4 | 
| TF-IDF () | 18.6 | 25.6 | 

### IV-E Exploratory Response Quality Validation

We conducted supplementary quality assessment of RAG-generated responses across three retrieval configurations: content-only baseline, TF-IDF weighted metadata enrichment, and prefix-fusion approaches. These evaluations serve as exploratory validation rather than primary experimental outcomes. The TF-IDF metadata-enriched approach demonstrated consistently superior performance across all quality dimensions compared to both the content-only baseline and prefix-fusion alternatives, with notable improvements in response faithfulness and corresponding reductions in hallucination rates. Coverage metrics similarly favored this configuration. However, these indicators should be interpreted as directional confirmation that improved retrieval quality translates to more plausible generated responses, rather than definitive benchmarks of generation capability. LLM-based quality metrics are susceptible to confounding factors including prompt design variations, reference construction methodology, and generation temperature settings, that remain outside the scope of our primary experimental controls.

### IV-F Key Findings and Insights

Our comprehensive evaluation revealed several important insights:

- •
Naive chunking with prefix-fusion consistently delivered the strongest retrieval performance, achieving the highest MRR (0.750), NDCG (0.813), and precision (0.798), while matching the best Hit Rate@10 (0.900). Uniform chunk sizes ensure that prefixed metadata exerts consistent influence across all segments, whereas variable-length chunks from semantic or recursive strategies can unevenly distribute this influence—larger chunks may bury the prefix signal, while smaller ones overemphasize it. For formally structured documentation such as AWS S3 [ [22](https://arxiv.org#bib.bib22) ], which features clear sectional boundaries and hierarchical organization, naive segmentation avoids the over-fragmentation that semantic methods introduce in dense technical text with varying information density.
- •
Recursive chunking demonstrated robust performance across all embedding techniques, with content-only embeddings achieving competitive results (NDCG 0.782, Precision 0.783, MRR 0.713). Its hierarchical splitting preserves document structure at natural boundaries, providing reliable representations regardless of embedding methodology. This stability makes recursive chunking a dependable default when corpus structural properties are unknown or heterogeneous.
- •
The weight sensitivity analysis reveals that metadata integration exhibits a seasoning effect: a 10% metadata contribution consistently enhances retrieval across all chunking strategies, while higher ratios progressively degrade performance. This occurs because TF-IDF metadata vectors are inherently sparser and less semantically rich than content embeddings; excessive weighting amplifies shallow keyword matches over deep content relevance. Prefix-fusion sidesteps this limitation entirely by allowing the encoder to contextually modulate metadata influence during encoding rather than through post-hoc vector arithmetic.

These results empirically validate that metadata enrichment frameworks must be carefully tailored to specific retrieval objectives. The findings establish quantitative benchmarks for implementing high-performance RAG systems, highlighting the non-trivial interactions between chunking strategies and embedding techniques in determining retrieval effectiveness across standardized information retrieval metrics.

Table [IX](https://arxiv.org#S4.T9) summarizes these findings as a configuration decision matrix for practitioners deploying metadata-enriched RAG systems in production environments.

| Priority | Configuration | Key Metric | 
|---|---|---|
| Best Ranking | Naive + Prefix-Fusion | NDCG 0.813 | 
| Max Hit Rate | Naive + TF-IDF/PF | HR@10 0.900 | 
| Best Stability | Recursive + Content | Prec. 0.783 | 
| Lowest Latency | Content-Only | P50 12 ms | 
| Balanced | TF-IDF () | NDCG 0.687 | 

## V Conclusion

This study demonstrates that integrating LLM-based metadata enrichment into retrieval pipelines significantly enhances RAG system performance in technical documentation contexts. Our  factorial evaluation reveals that the method of metadata integration matters as much as the choice of chunking strategy. Prefix-fusion—which allows the encoder to jointly process metadata and content as a unified input—consistently outperforms TF-IDF weighting, where separately computed vectors are blended via linear combination under an assumption of vector space alignment that does not hold in practice. Naive chunking with prefix-fusion emerges as the strongest configuration on our corpus, as the uniform segment sizes ensure consistent metadata influence across chunks. This advantage is amplified by the inherently well-structured nature of AWS S3 documentation [[22](https://arxiv.org#bib.bib22)], where clear sectional boundaries reduce the value of semantically-aware splitting. Chunking strategy selection is thus fundamentally domain-dependent: formally structured corpora may favor simpler segmentation augmented with metadata, whereas less structured documents may benefit from adaptive semantic chunking. Recursive chunking offers the most stable cross-configuration performance, making it a robust default when corpus properties are unknown.

Metadata operates as a seasoning effect: a small proportion (10%) consistently improves retrieval by injecting discriminative signals, while higher ratios degrade performance as sparse metadata features dilute the content representation. Prefix-fusion avoids this degradation entirely by enabling the encoder to contextually modulate metadata influence during encoding rather than through post-hoc vector arithmetic. These insights, combined with sub-30 ms P95 latency and improved vector space organization (DBI: 3.12 vs. 3.77), confirm that metadata-enriched RAG systems are production-viable and provide actionable configuration guidance for practitioners.

Future work should explore scalability to larger and more diverse corpora, dynamic metadata generation for evolving content, and integration within real-time retrieval systems with adaptive chunking strategies.

### V-A Limitations

Our evaluation relies on silver-standard pseudo-ground truth derived from cross-encoder reranking rather than human annotations, and scores only chunks retrieved by at least one configuration, introducing retrieval pool bias. Consequently, absolute metric values should be interpreted with caution, while relative comparisons between configurations remain valid. Additionally, the evaluation is conducted on a single domain (AWS S3 documentation); replication on heterogeneous corpora is necessary to establish broader generalizability.

## ACKNOWLEDGMENT

This project has been completed under the supervision of Fatemeh Sarayloo. The first four authors were pursuing their master’s programs while working on this project. We appreciate the support of the University of Illinois Business College.

## References

- [1] P. Lewis, E. Perez, A. Piktus, F. Petroni, V. Karpukhin, N. Goyal, H. Küttler, M. Lewis, W.-t. Yih, T. Rocktäschel, S. Riedel, and D. Kiela, “Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks,” in Advances in Neural Information Processing Systems (NeurIPS), vol. 33, pp. 9459–9474, 2020.
- [2] K. Shuster, S. Poff, M. Chen, D. Kiela, and J. Weston, “Retrieval Augmentation Reduces Hallucination in Conversation,” in Findings of the Association for Computational Linguistics: EMNLP 2021, Punta Cana, Dominican Republic, pp. 3784–3803, 2021. DOI: 10.18653/v1/2021.findings-emnlp.320.
- [3] V. Karpukhin, B. Oguz, S. Min, P. Lewis, L. Wu, S. Edunov, D. Chen, and W.-t. Yih, “Dense Passage Retrieval for Open-Domain Question Answering,” in Proc. 2020 Conf. on Empirical Methods in Natural Language Processing (EMNLP), pp. 6769–6781, 2020. DOI: 10.18653/v1/2020.emnlp-main.550.
- [4] Y. Gao, Y. Xiong, X. Gao, K. Jia, J. Pan, Y. Bi, Y. Dai, J. Sun, Q. Guo, M. Wang, and H. Wang, “Retrieval-Augmented Generation for Large Language Models: A Survey,” arXiv preprint arXiv:2312.10997, 2024.
- [5] J. Chen, H. Lin, X. Han, and L. Sun, “Benchmarking Large Language Models in Retrieval-Augmented Generation,” in Proc. AAAI Conf. on Artificial Intelligence, vol. 38, no. 16, pp. 17754–17762, 2024. DOI: 10.1609/aaai.v38i16.29728.
- [6] S. S. Sundaram and M. A. Musen, “Making Metadata More FAIR Using Large Language Models,” in DaMaLOS Workshop, co-located with ESWC 2023, Hersonissos, Greece, 2023. arXiv: 2307.13085. DOI: 10.4126/FRL01-006444995.
- [7] L. Wang, N. Yang, X. Huang, L. Yang, R. Majumder, and F. Wei, “Large Search Model: Redefining Search Stack in the Era of LLMs,” ACM SIGIR Forum, vol. 57, pp. 1–16, 2024. DOI: 10.1145/3642979.3643006.
- [8] H. Song, S. Bethard, and A. K. Thomer, “Metadata Enhancement Using Large Language Models,” in Proc. Fourth Workshop on Scholarly Document Processing (SDP 2024), Bangkok, Thailand, pp. 145–154, 2024. DOI: 10.18653/v1/2024.sdp-1.14.
- [9] L. Mombaerts, T. Ding, A. Banerjee, F. Felice, J. Taws, and T. Borogovac, “Meta Knowledge for Retrieval Augmented Large Language Models,” in Workshop on Generative AI for Recommender Systems and Personalization (GenAIRecP), KDD 2024, Barcelona, Spain, 2024. arXiv: 2408.09017.
- [10] N. Harris, A. Butani, and S. M. Y. Hashmy, “Enhancing Embedding Performance through Large Language Model-based Text Enrichment and Rewriting,” Advances in Artificial Intelligence and Machine Learning, vol. 4, no. 2, pp. 2358–2368, 2024. DOI: 10.54364/aaiml.2024.42136.
- [11] J. Saad-Falcon, O. Khattab, C. Potts, and M. Zaharia, “ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems,” in Proc. 2024 Conf. of the North American Chapter of the Association for Computational Linguistics (NAACL), Mexico City, Mexico, pp. 338–354, 2024. DOI: 10.18653/v1/2024.naacl-long.20.
- [12] R. Anantha and D. Vodianik, “Context Tuning for Retrieval Augmented Generation,” in Proc. 1st Workshop on Uncertainty-Aware NLP (UncertaiNLP), EACL 2024, St Julians, Malta, pp. 15–22, 2024. DOI: 10.18653/v1/2024.uncertainlp-1.2.
- [13] F. Cuconasu, G. Trappolini, F. Siciliano, S. Filice, C. Campagnano, Y. Maarek, N. Tonellotto, and F. Silvestri, “The Power of Noise: Redefining Retrieval for RAG Systems,” in Proc. 47th Int. ACM SIGIR Conf. on Research and Development in Information Retrieval (SIGIR ’24), Washington, DC, USA, pp. 719–729, 2024. DOI: 10.1145/3626772.3657834.
- [14] Z. Shao, Y. Gong, Y. Shen, M. Huang, N. Duan, and W. Chen, “Enhancing Retrieval-Augmented Large Language Models with Iterative Retrieval-Generation Synergy,” in Findings of the Association for Computational Linguistics: EMNLP 2023, Singapore, pp. 9248–9274, 2023. DOI: 10.18653/v1/2023.findings-emnlp.620.
- [15] Y. Wang, P. Li, M. Sun, and Y. Liu, “Self-Knowledge Guided Retrieval Augmentation for Large Language Models,” in Findings of the Association for Computational Linguistics: EMNLP 2023, Singapore, pp. 10303–10315, 2023. DOI: 10.18653/v1/2023.findings-emnlp.691.
- [16] B. E. Perron, L. Goldkind, Z. Qi, and B. G. Victor, “Human Services Organizations and the Responsible Integration of AI: Considering Ethics and Contextualizing Risk(s),” Journal of Technology in Human Services, vol. 43, no. 1, pp. 20–33, 2025. DOI: 10.1080/15228835.2025.2457045.
- [17] S. Liu, A. B. McCoy, and A. Wright, “Improving large language model applications in biomedicine with retrieval-augmented generation: a systematic review, meta-analysis, and clinical development guidelines,” Journal of the American Medical Informatics Association, vol. 32, no. 4, pp. 605–615, 2025. DOI: 10.1093/jamia/ocaf008.
- [18]
A. Ramachandran, “Advancing Retrieval-Augmented Generation (RAG): Innovations, Challenges, and the Future of AI Reasoning,” IBM Research, Feb. 2025. [Online]. Available: [https://www.researchgate.net/publication/388722115](https://www.researchgate.net/publication/388722115)
- [19]
L. Merrick, D. Xu, D. Campos, et al., “Arctic-Embed 2.0: Multilingual Retrieval Without Compromise,” arXiv preprint arXiv:2412.04506, 2024. Model: [https://huggingface.co/Snowflake/snowflake-arctic-embed-m-v2.0](https://huggingface.co/Snowflake/snowflake-arctic-embed-m-v2.0)
- [20]
J. Chen, S. Xiao, P. Zhang, K. Luo, D. Lian, and Z. Liu, “BGE M3-Embedding: Multi-Lingual, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation,” arXiv preprint arXiv:2402.03216, 2024. Model: [https://huggingface.co/BAAI/bge-reranker-base](https://huggingface.co/BAAI/bge-reranker-base)
- [21] D. Edge, H. Trinh, N. Cheng, J. Bradley, A. Chao, A. Mody, S. Truitt, and J. Larson, “From Local to Global: A Graph RAG Approach to Query-Focused Summarization,” arXiv preprint arXiv:2404.16130, 2024.
- [22]
Amazon Web Services, “Amazon S3 Documentation,” [https://docs.aws.amazon.com/s3/](https://docs.aws.amazon.com/s3/) , 2024.
