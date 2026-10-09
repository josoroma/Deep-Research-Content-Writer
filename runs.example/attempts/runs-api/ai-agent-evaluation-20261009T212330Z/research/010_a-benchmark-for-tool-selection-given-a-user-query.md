---
source_id: S-10
url: https://community.openai.com/t/a-benchmark-for-tool-selection-given-a-user-query/730307
title: A Benchmark for tool selection given a user query
author: null
published: '2024-04-28T14:18:20+00:00'
fetched: '2026-10-09T21:23:43Z'
word_count: 393
---
# A Benchmark for tool selection given a user query

[janekzimoch](https://community.openai.com/u/janekzimoch)

April 28, 2024, 2:18pm

1

OpenAI provides the ability to enhance user’s prompt with a set of function descriptions to let the GPT model decide which tool to use.

I am looking for a benchmark dataset which would allow me to evaluate how well GPT matches uesr intent with those functions (as a baseline). And then compare my onw system to this baseline on the same evaluation set.

Does anyone know of such benchmark dataset?

**Context:**  
In dialogue systems, accurately mapping a user’s query to an appropriate action from a set of possible options is crucial. Given a user prompt `p`, the goal is to select an action `a` from a set of actions `A` such that the probability of choosing the correct action is maximized, i.e., `argmax_i(p(a_i | p))`.

I spent this past weekend searching for a benchmark dataset to evaluate and potentially expand the training dataset for the system I developed, but I couldn’t find anything relevant. It seems strange that such a dataset wouldn’t be publicly available.

Closest Available Datasets I found are:

- **ATIS:** Airline travel specific with only 26 categories.
- **Intent Classification from Amazon Alexa and IoT:** Limited to Amazon-specific contexts.
- **CLINC150**: Only includes 7 classes.

[janekzimoch](https://community.openai.com/u/janekzimoch)

April 28, 2024, 4:48pm

2

I think I found it. Related field is “task-oriented dialogue systems” and the related task is “intent state tracking”. Although, I don’t need to consider a full dialogue, my problem seems to be a problem of identifying “intent state” within a single turn of a dialogue.

Related dataset would be MultiWOZ.

If someone is an expert in this field and could correct me if I am wrong or recommend some additional datasets/papers that would be great. Additionaly,

I am now interested in understadning:

1. how “task-oriented dialogue systems” have evolved in the era of LLMs?
2. and why “AI agent” community talks so little about this field of research? It seems like a lot of work “AI agent” developers are trying to do now with LLMs has been already done (or at least started) with “task-oriented dialogue systems”

[janekzimoch](https://community.openai.com/u/janekzimoch)

April 30, 2024, 1:53pm

3

Aparently, in the era of LLMs and RAGs learnign made with TOD are no longer relevant.

Could anybody point me to relevant papers which show how TOD has evolved in the era of LLMs and RAG?
