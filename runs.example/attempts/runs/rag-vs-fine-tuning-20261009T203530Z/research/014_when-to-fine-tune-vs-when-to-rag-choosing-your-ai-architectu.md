---
source_id: S-14
url: https://jamesm.blog/ai/fine-tune-vs-rag
title: 'When to Fine-Tune vs When to RAG: Choosing Your AI Architecture'
author: James M
published: '2026-04-29T08:00:00+01:00'
fetched: '2026-10-09T20:35:52Z'
word_count: 2085
---
# When to Fine-Tune vs When to RAG: Choosing Your AI Architecture

## TL;DR[#](https://jamesm.blog#tldr)

- The default choice for most teams should be **RAG** - it is reversible in days, whereas a bad fine-tuning decision is an expensive sunk cost that requires retraining to fix
- RAG fails when the question requires reasoning across an entire knowledge domain rather than extracting a specific answer from a passage; **fine-tuning** handles that case better
- Fine-tuning fails silently when underlying facts change - it produces confidently wrong, stale answers with no warning; RAG automatically picks up changes at query time
- A practical decision framework: use RAG for volatile facts and cited answers, use fine-tuning for stable style, voice, and cross-domain reasoning
- The best production systems use **both** : a fine-tuned base model for stable domain knowledge, augmented with retrieval for current and specific information

The question I get asked most often by engineers starting to build with language models is some variation of: “should we fine-tune or should we do RAG?” It is almost always the wrong question, but it is the wrong question in an instructive way. The reason it gets asked so much is that the choice feels architectural, and architectural choices feel like the kind of thing you commit to once and live with. In practice, the choice is closer to “should I use a database or a cache” - the answer is usually some of both, applied to different problems, and the ratio shifts as the system matures.

This post is the answer I now give. It is opinionated, it draws on patterns I have seen succeed and fail repeatedly, and it tries to be honest about the cases where the conventional wisdom is wrong.

## The two techniques in one paragraph each[#](https://jamesm.blog#the-two-techniques-in-one-paragraph-each)

[Retrieval-augmented generation](https://en.wikipedia.org/wiki/Retrieval-augmented_generation) is the practice of fetching relevant context at query time and putting it directly into the model’s prompt. The model is unchanged. What changes is what it gets to read before it answers. RAG is a runtime architecture, not a model modification. Its quality depends entirely on the quality of the retrieval step and the discipline of the prompt that consumes the retrieved chunks.

[Fine-tuning](https://en.wikipedia.org/wiki/Fine-tuning_%28deep_learning%29) is the practice of continuing the training of a base model on a curated dataset, so that the resulting weights produce different outputs than the base would have. Fine-tuning is a build-time architecture. The cost is paid up front, the artifact is a new model, and the behaviour is baked into the parameters rather than supplied by a prompt. It is also where [small language models](https://jamesm.blog/ai/small-language-models/) earn their keep - a fine-tuned 7B model on a narrow domain can outperform a frontier model on the same task at a fraction of the cost, and is what makes [local-first AI deployments](https://jamesm.blog/ai/local-vs-cloud-ai-2026/) feasible.

Those two definitions sound symmetric. They are not. The asymmetry is the whole point of this post.

## The default should be RAG[#](https://jamesm.blog#the-default-should-be-rag)

If you are starting a new project and you are not sure which to use, start with RAG. Not because RAG is universally better, but because the reversibility profile is wildly different.

A RAG system you do not like can be torn down and rebuilt in days. The model is unchanged, the corpus is unchanged, the retrieval index is the only thing that took real effort, and you can swap out the retriever, the embedding model, the chunking strategy, the reranker, the prompt, and even the foundation model behind it without re-running a training job. You can also make changes incrementally and observe their effect in production with very little risk.

A fine-tuned model you do not like is a sunk cost. The dataset took weeks to curate, the training run cost real money, the resulting weights are a frozen artifact that needs to be re-evaluated, re-versioned, and re-deployed. You cannot easily un-bake an undesirable behaviour. You can only train again on different data and hope.

This is not a small difference. The default architectural choice should favour the option that lets you change your mind cheaply, especially in a domain where your intuitions about what works will improve faster than your engineering can keep up with.

## Where RAG quietly fails[#](https://jamesm.blog#where-rag-quietly-fails)

RAG has a very specific failure mode that the marketing literature is curiously silent about. It fails when the question requires the model to reason over the entire retrieved context as a unified whole, rather than extracting an answer from a specific passage.

Consider three queries against the same knowledge base of internal engineering documents:

1. “What is the timeout value for the payment service?”
2. “Summarise the architectural decisions we made about the payment service this quarter.”
3. “Given our existing payment service architecture, what tradeoffs would we hit if we moved to event-driven settlement?”

The first query is what RAG was designed for. There is one passage that contains the answer, the retriever finds it, the model reads it, the answer comes out clean.

The second query requires the model to fuse multiple passages into a coherent narrative. RAG can sort of do this, but performance degrades as the number of relevant chunks grows. The model is being asked to synthesise across pieces it has no global view of, and it will often miss connections, double-count claims, or invent transitions.

The third query requires the model to reason from internalised understanding of how your architecture actually works. RAG is fundamentally not designed for this. You can shove a hundred documents into the context and ask the question, but the model is still doing reading comprehension, not architectural reasoning. It does not have your system in its head. It has fragments of it in its working memory.

This is where fine-tuning earns its keep. A model fine-tuned on a corpus of your engineering decisions has those decisions encoded in its weights. It can reason from them the same way it reasons from anything else in its training distribution. It does not need to retrieve them, and it does not have a context window limit on how much it knows.

## Where fine-tuning quietly fails[#](https://jamesm.blog#where-fine-tuning-quietly-fails)

The mirror failure is just as common, and more expensive. Fine-tuning fails when the underlying facts change.

If you fine-tune a model on your product documentation as of January, and your documentation changes in March, the model is now wrong. It will confidently produce outputs that were correct three months ago and are not correct any more. There is no error message, no warning, no indication that the answer is stale. The model has forgotten that the world is a moving target.

You can solve this with re-training, but re-training is a discrete event that happens on the cadence of your training pipeline, not the cadence of reality. RAG, by contrast, picks up changes the moment the underlying source is updated, because it reads the source at query time.

Anything that changes - prices, policies, schemas, names of people in your organisation, current state of any system - is a poor candidate for fine-tuning and a natural candidate for RAG. Anything that is stable - core domain concepts, your house writing style, a body of historical reasoning - is a poor candidate for RAG and a natural candidate for fine-tuning.

## The decision framework I actually use[#](https://jamesm.blog#the-decision-framework-i-actually-use)

When someone asks me which to choose, I run through a short series of questions in my head. They are not perfect, but they sort the cases quickly.

**Does the answer change frequently?** If yes, lean RAG. The cost of stale fine-tuned knowledge is high and silent.

**Is the question answerable from a small number of identifiable passages?** If yes, lean RAG. This is exactly the regime retrieval was built for.

**Does the model need to produce output in a specific style, voice, or format that is hard to specify in a prompt?** If yes, lean fine-tuning. Style transfer is one of the things fine-tuning is genuinely good at, and prompts trying to specify the same style tend to bloat over time.

**Does the task require reasoning across the entire body of knowledge, not retrieval from it?** If yes, lean fine-tuning. RAG cannot fit a whole domain in a context window.

**Do you have less than a few thousand high-quality examples?** If yes, do not fine-tune. You will not have enough signal to move the model meaningfully, and you will overfit on idiosyncrasies of your dataset. Use RAG and a strong prompt instead - and structure that prompt so it [caches well](https://jamesm.blog/ai/prompt-caching/), because RAG prompts are exactly the workload caching is shaped for.

**Is the cost of being wrong high, and do you need to cite sources?** If yes, lean RAG. RAG gives you a natural attribution path - the chunk the model used. Fine-tuning gives you opaque parameters that produced the answer somehow, and that opacity is one of the [common roots of hallucinations](https://jamesm.blog/ai/ai-hallucinations-understanding-and-mitigating/).

**Is latency critical, and is the retrieval step expensive?** If yes, lean fine-tuning. A fine-tuned model that already knows the answer is faster than one that has to query a vector database, rerank, and digest a prompt.

These pull in different directions for any non-trivial system. That is the point. Real systems use both.

## Hybrid is the actual answer[#](https://jamesm.blog#hybrid-is-the-actual-answer)

The architecture I see succeed most often in production is not pure RAG and not pure fine-tuning. It is a fine-tuned base model that has internalised the domain’s vocabulary, voice, and stable patterns, augmented with retrieval over the parts of the domain that change.

The fine-tuning handles the things that are stable and cross-cutting. The way your company describes itself. The terminology your customers use. The tone of voice the brand expects. The structural patterns the system always follows.

The retrieval handles the things that are specific and current. This week’s product catalogue. The customer’s account state. The most recent decision the architecture council made.

This split has another quiet benefit. It lets you size each piece appropriately. You do not need to fine-tune on a giant dataset, because the fine-tuning is only carrying the stable parts. You do not need to retrieve a giant context, because the retrieval is only filling in the volatile parts. The system stays small and fast where it can, and brings out the heavy machinery only where it must.

## What this looks like in practice[#](https://jamesm.blog#what-this-looks-like-in-practice)

A support assistant for a SaaS product is a clean example. The fine-tuning teaches the model your support voice, your product’s mental model, the kinds of distinctions you draw between features, the boilerplate it should always use when escalating. The retrieval pulls in the customer’s account state, the latest documentation for the feature they are asking about, and any open known-issue notes. The model is good at the conversation because of the fine-tuning and correct about the facts because of the retrieval. The same hybrid pattern is what I leaned on when [giving a home AI agent durable memory](https://jamesm.blog/ai/home-ai-agent-memory-that-lasts/).

A code assistant inside an engineering organisation is another clean example. The fine-tuning teaches the model your house style, your internal naming conventions, your preferred patterns for error handling and testing. The retrieval pulls in the relevant files from the repository the developer is currently editing, the latest API documentation, and recent discussions in the relevant pull request. Neither piece is sufficient on its own. Together they produce something that reads like a colleague rather than a generic assistant.

In both cases the engineering question is not “which technique” but “which technique for which slice of the problem”. The architecture is the answer to that question, not the answer to a binary one.

## What I would tell a team starting today[#](https://jamesm.blog#what-i-would-tell-a-team-starting-today)

If you are building your first AI feature, start with RAG. Use a strong base model, focus on retrieval quality, write clear prompts, and ship. You will learn more about what your users actually need from the first month in production than you will from any amount of architectural deliberation.

Once you have something running, watch where it consistently disappoints. If it is getting facts wrong because the underlying source changed, your retrieval needs work. If it is getting voice and structure wrong, or struggling to reason across the domain, fine-tuning is starting to earn its keep. Layer it in, but only over the slices where you have real evidence the prompt and retrieval cannot carry the load.

Avoid the mistake of treating this as a one-time choice. Treat it the way you treat caching: a thing you add when it earns its place, scoped narrowly, removed when it stops earning. The systems that age well are not the ones that picked the right architecture on day one. They are the ones that kept the cost of changing their minds low.
