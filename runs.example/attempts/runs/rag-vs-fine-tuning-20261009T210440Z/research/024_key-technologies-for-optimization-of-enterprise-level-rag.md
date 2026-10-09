---
source_id: S-24
url: https://www.alibabacloud.com/blog/601723
title: Key Technologies for Optimization of Enterprise-Level RAG
author: null
published: null
fetched: '2026-10-09T21:05:07Z'
word_count: 2896
---
# Key Technologies for Optimization of Enterprise-Level RAG

[Blog](https://www.alibabacloud.com/blog/)

[Events](https://resource.alibabacloud.com/event/index)

[Webinars](https://resource.alibabacloud.com/webinar/index.htm)

[Tutorials](https://community.alibabacloud.com/tags/type_blog-tagid_28404/)

[Forum](https://www.alibabacloud.com/forum)

**By Xing Shaomin**

At the 2024 Cloud Habitat Conference. This conference will guide you to understand how to use RAG technology to optimize decision support, content generation, intelligent recommend and other core business scenarios, to provide strong technical support for the digital transformation and intelligent upgrade of enterprises. Mr. Xing Shaomin, who is one of the leaders of Alibaba Cloud AI search research and development, explained to us the key technology-enterprise-level RAG full-link optimization,The main content is divided into four parts: enterprise-level RAG key links, enterprise-level RAG effect optimization, enterprise-level RAG performance optimization, and enterprise-level RAG application practices.

The definition of RAG is Retrieval-Augmented Generation (Retrieval enhancement Generation),Simply put, it is to use the search results to guide the generation of LLM. The following is a RAG link diagram of our Alibaba Cloud AI search open platform. The red part is the offline link, and the blue part is the online link. 

After a long period of research and development on RAG, our team has summed up the key points of enterprise RAG landing, namely, effect, performance, and cost.

● **Effect**: Today, many enterprises do not implement RAG on a large scale, or do not use RAG in some key scenarios, because they are worried that after using it, they will affect their business in core scenarios due to effect problems. Therefore, the effect problem is the most critical factor for RAG landing now.

● **Performance**: large models are required in many aspects of the RAG link, such as vectorization, Document parsing, and finally large model generation and large model Agent. In this way, the entire link calls the large model multiple times, resulting in different degrees of degradation of offline and online performance. Like GraphRAG, for example,A 30k document takes nearly an hour to process data properly, which makes it difficult to land in a production environment.

● **Cost**: compared with other applications, the RAG application needs to call the large model many times, and the GPU is behind the large model, but the GPU resources are scarce and expensive, which inevitably leads to the much higher cost of such applications than other applications, so many customers cannot accept this cost.

First of all, at the effect level, the first optimization point in the offline link is Document parsing. Documents have many formats, such as PDF, Word, PPT, etc., as well as some structured data. However, the biggest difficulty is some unstructured documents, because there will be different content. For example, like tables, pictures,These content AI is actually very difficult to understand. After a large number of long-term optimization, we provide Document parsing services in the search open platform, supporting a variety of common document formats and content parsing.

After the document is parsed and the content can be correctly extracted from the document, the text can be sliced next. There are many ways to slice, the most common one is Hierarchical Segmentation: extract the paragraph and slice the contents of the paragraph at the paragraph level. There is also multi-granularity Segmentation: sometimes in addition to the slices of paragraphs, you can also add slices of single sentences.These two types of slices are the most commonly used. In addition, for some scenarios, we can also perform semantic slicing based on a large model: that is, the structure of the document is processed with a large model, and then some finer document structures are extracted. Then after various slices, we can continue to vectorize.

Alibaba Cloud has developed a unified vectorization model. This vectorization model can produce both dense and sparse vectors. After the vectors are produced, they can be mixed for retrieval and then rearranged to obtain retrieval results. And this vectorization model won the first place in the C- MTEB on the Chinese vectorization list in March this year.

The three mentioned above are the core offline links, and then enter the online link. The first step of the online link is the understanding of query. query understands that we usually use vectors, which means that after query comes in, it needs to be vectorized before recalling.However, in some scenarios, the problem cannot be solved after vector recall. For example, we want to query the names of all e-commerce companies with less than 50 employees. For a data with less than 50 employees, using vectors, less than 50 employees, less than 40 employees, and less than 49 employees are actually very similar. This is a difficult problem to solve.

For such scenarios, we can convert the natural language into an SQL to perform precise lookup in the SQL database. Another is to query entities and relationships, we can convert natural language into graph query statements in the graph database to query, and finally get accurate results.

After the query is processed, the vector will usually be recalled along the way to do Rerank. At the beginning of the Rerank model, we used open source Bge-reranker, which also played a great role in the overall effect.

Recently, we have developed a new Rerank model based on the Qwen model, which has been improved in all aspects. We used it in Aliyun's Elasticsearch AI search solution and found that the overall effect was improved by 30%.Compared with open source Bge-reranker, the Rerank effect based on LLM is significantly improved. After finishing the Rerank, the recall link has been completed.

After the Recall link is completed, it enters the large model generation. When we first used the first version of the Qwen large model, the various capabilities of the large model were actually not perfect, so we were more to optimize the capabilities of the large model. For example, when using NL2SQL, you need to use a lot of data to fine-tune the ability of large models NL2SQL.With the rapid iteration of large models, the ability becomes stronger and stronger.

At this point we shift our energy to optimizing the illusion rate of the big model, so that the illusion rate keeps decreasing. We fine-tune the model based on Qwen 14b, and after fine-tuning, we have been able to approach the GPT-4O model effect in customer scenarios. Why fine-tune it in a 14b model?Because the 14b Qwen model will be much smaller than the 72b Qwen model, it will bring great performance improvement. In the case of a flat effect, there is a great performance improvement, in fact, there is a good landing advantage.

The solution on the above link can help us deal with some simple question-and-answer scenarios, but it still cannot solve complex question-and-answer scenarios. 

For example, like the following two examples, this is a problem that can only be solved by multi-step reasoning and multiple searches. Let's take the second example and ask, "What is Riemann's zodiac?", The first search would come out: Riemann was born in 1826.Then the big model will think and launch a second search: What is the corresponding zodiac sign in 1826 at this time? After getting the 1826 Zodiac is a dog, the big model will finally make a summary. Riemann was born in 1826 and the zodiac is a dog. Of course, some big models can match this year with the zodiac,You can answer directly without a second search. The example on the left also requires the big model to think about it and retrieve it twice to get the result. This is an example of how we use agents to solve complex problems.

Our Aliyun team conducted a test on a specific scenario. Using native RAG, 78% of the problems can be solved, and the average number of searches is 1. This is better understood, that is, RAG usually searches once and then generates an answer. After using ReAct, 85% of the questions can be answered,An average of 1.7 searches. Then we made some improvements to ReAct. Search-First ReAct is to Search First and then let the big model think about it. In this way, 90% of the problems can be solved and the average number of times of speed will be reduced to 1.2. So you can see that after using the Agent,Can effectively reduce the number of searches, and can improve the answer rate, the overall effect has been significantly improved.

Of course, the Agent is also facing some challenges. For example, it is impossible to solve all the problems: for some complex problems, only 70% of the problems can be solved for the time being, and 30% of the problems cannot be solved, which requires us to continue to study. There is also a performance degradation: due to the need to interact with the large model multiple times after using the Agent,So query performance will degrade. In addition, when the large model performs Agent reasoning, if the first step of reasoning is wrong, then when the reasoning continues later, the error will be added, so the illusion rate may become very high. Of course, these problems are not unsolvable, but need to be optimized iteratively.

In the earliest days, we were able to achieve a 48% problem resolution rate using the first generation of Qwen plus Vector search. Then do Prompt Engineering, multi-channel recall and hierarchical slicing, which can achieve 61%. Later, Qwen SFT increased to 72%. And later added Rerank,The optimization of the vector model and the slice of multi-granularity are done. Up to now, we have done a lot of optimization in the field of Document parsing, plus Agent optimization, CPU optimization and a series of optimization overlays such as certain semantic slicing, and the problem solving rate has increased to 95%. Because the customer scenario is very complex,This journey has not been easy either.

Effect optimization The next step is performance optimization. In terms of performance, we first need to look at vector retrieval. For vector retrieval, we have a VectorStore CPU algorithm and a VectorStore GPU algorithm.

The CPU algorithm uses the HNSW algorithm. Based on this algorithm, we have optimized both Graph construction and retrieval, as well as a large number of engineering optimizations. After the optimization is completed, the performance of the CPU algorithm can be about 2 times that of similar products. You can directly Search the Vector Search version of our Open Search on the cloud,Then go and test its performance.

GPU graph algorithm uses Nvidia's algorithm. After implementing this algorithm, the benefits we bring are 3 to 6 times of performance improvement on Nvidia T4 cards and 30 to 60 times of performance improvement on Nvidia's A100/A800/H100 high-performance cards.However, such a performance improvement, due to the use of GPU, also brings a cost increase.

For this scenario, we have done some tests, and the conclusion is that when QPS is very high, or when it reaches a certain threshold, the cost performance of using GPU will be higher than that of using CPU, and the approximate pre-value is about 3000 QPS. If our QPS is high,When we use GPU for thousands or tens of thousands of years, we will have a cost-effective advantage. However, if our QPS is very low, GPU algorithm has no cost-effective advantage. The above is the work we have done in vector retrieval.

We use a variety of different methods such as caching, large model quantization, and multi-card parallelism to accelerate inference on large models.

What can be done now is that on the Qwen model of 14b, an answer 200 token can be generated in 1 to 3 seconds, and then on the Qwen model of 72b, an answer 200 token can be generated in about 4 seconds. Because as the number of tokens increases,Time also increases. If the average answer length is 200 token, the answer can be generated within 3 to 4 seconds, which is the benefit of using large model reasoning to accelerate.

In order to reduce the cost of large model fine-tuning, we developed a large model fine-tuning based on Lora.

When fine-tuning a customer model, if a card is given to a customer, the customer needs to bear the cost of the card independently, but if we fine-tune the model of multiple customers on one card, we can save costs. We now put 40 to 50 clients' model tweaks on one card, reducing the cost of tweaks from the original monthly 4000 to 100 per month,This reduces the cost to 1/40 of the original.

There are two ways to implement Lora, one is single-card Lora and the other is multi-card Lora. Single-card Lora is a model of 40-50 customers for each card, and multiple customers share a single card. Multi-card Lora means to cut all the models and put the model slices on multiple different cards.This is a difference in the way it is implemented.

The enterprise-class AI search open platform exposes the various technical capabilities described above in a service plaza in the form of microservices.

First of all, it has many microservices, such as document parsing, vectorization, NL2SQL, LLM Agent, LLM evaluation, LLM training, LLM reasoning, etc. are exposed in the form of microservices. Users can use the API to call. In addition to using API to call a single service,Users can also use the SDK to connect microservices in series and then connect a scene in series.

In addition to the Alibaba Cloud SDK, we also support the OpenAI SDK, LangChain SDK, and Llamalndex SDK. This is the open source ecosystem we mentioned earlier. This platform is designed to allow customers to use these SDKs or use API calls to connect these microservices in series,To develop a variety of different scenarios, such as multimodal search, RAG question and answer, and a variety of AI search-related scenarios.

We now support the Havenask engine and the Elasticserach engine. In the future, we will also support graph engines such as GraphCompute and vector engines such as Milvus.

There will also be a unified multi-modal data management at the bottom. This data management will support unstructured documents such as PDF, Word, and PPT, as well as data Lake and database docking, as well as OSS and HDFS storage docking. So why the data layer? This is because being a platform,If users are allowed to move their data to it, the relocation cost is very high. If there is a unified data management layer, customers can directly connect their own databases and data sources to the platform, without migration, and directly develop application scenarios on the platform.

We have also developed multi-modal search and multi-modal RAG scenarios on the platform. We need to connect several services on the platform, such as vectorization and Image Understanding, and then connect a multi-modal search and multi-modal RAG scene.

If there is a complex RAG problem, in the offline link, a PDF will be processed into a Markdown first, then the Markdown will be cut into several slices, and finally these slices will be vectorized, which is the offline process of searching the open platform RAG.

If there is an online link, the first retrieval will be carried out, the problem will be searched out in two slices, then summarized, and then reasoning will be carried out to generate sub-problems for secondary retrieval, and the slices will be carried out for secondary summary. After two agent searches, we will get a final summary.

In addition to the search open platform for developers, we also have OpenSearch LLM edition. This product can set up a RAG service in three minutes. Basically, you only need users to upload data for testing. This product has the ability to answer questions based on NL2SQL,Output in tabular form, recommend, and so on.

Finally, we rely on the implementation of the AI search open platform, Elasticsearch Inference API, and Ingest API frameworks. Search open platforms can also be introduced into offline and online links of ES. AI search using Elasticsearch is used in the same way as the native one,There is no difference, this is compatible with user habits. You can see these capabilities in the 8.13 version of Alibaba Cloud Elasticsearch and the 8.16 open-source version of Elasticsearch.

In addition, we have launched the latest Alibaba Cloud Elasticsearch vector enhanced version, and its vector performance is improved by 5 times! 75% lower memory costs! It can flexibly connect a variety of products, provide multi-scenario solutions, seamlessly integrate with the AI search open platform, and have a cloud-native control and operation and maintenance platform,At the same time, we have also prepared a mature data migration and synchronization scheme. Welcome to experience it.

Alibaba Cloud Native Community - September 9, 2025

Alibaba Cloud Native Community - October 15, 2025

Alibaba Cloud Native Community - September 29, 2025

Alibaba Cloud Native Community - December 11, 2025

Alibaba Cloud Native Community - June 13, 2025

ApsaraDB - January 15, 2026

Alibaba Cloud Elasticsearch helps users easy to build AI-powered search applications seamlessly integrated with large language models, and featuring for the enterprise: robust access control, security monitoring, and automatic updates.

Apsara Stack is a full-stack cloud solution created by Alibaba Cloud for medium- and large-size enterprise-class customers.

A cloud-native vector search engine that is 100% compatible with open-source Milvus, extensively optimized in performance, stability, availability, and management capabilities.

ApsaraDB for HBase is a NoSQL database engine that is highly optimized and 100% compatible with the community edition of HBase.
