---
source_id: S-27
url: https://ai-de.net/projects/enterprise-rag
title: Enterprise RAG — retrieval-quality build — EXPERT AI & vectors project | AI-DE
author: AI-DE
published: null
fetched: '2026-10-09T20:53:24Z'
word_count: 1238
---
# Enterprise RAG — retrieval-quality build — EXPERT AI & vectors project | AI-DE

# Build a

*retrieval-quality*

RAG platform — that survives a relevance review

Ship a production RAG platform anchored on retrieval quality: 4 chunking strategies with measured 62/78/85% accuracy A/B, hybrid BM25 + dense + RRF retrieval, cross-encoder reranking, RAGAS 4-metric eval harness, and a multi-provider LLM gateway. Module 01 unlocks with PRO; the retrieval stack unlocks with EXPERT.

The **retrieval-quality portfolio piece** for staff AI / ML platform roles — 5 committed ADRs, a runnable cost-model CSV, a chunking-A/B benchmark with cited numbers, and a hybrid + reranker pipeline you can defend in a relevance-review.

- Multi-format parsers (PDF / DOCX / Markdown / Text) + 4-strategy ChunkingFactory
- Pinecone HNSW index over text-embedding-3-small (1536-dim) with namespace per tenant
- Hybrid retriever — BM25 + dense fused via Reciprocal Rank Fusion (k=60)
- Cross-encoder reranker (top-50 → top-10) with disable-able score floor
- RAGAS 4-metric harness (faithfulness / answer_relevancy / context_precision / context_recall)
- LLM gateway with fallback chain, response cache (1h TTL), per-tenant cost tracker
- 5 ADRs (one Deprecated) committed alongside the code, plus a runnable cost-model CSV

*Not a “hello LangChain” tutorial.*

*4-strategy*chunker

*BM25 + dense*+ reranker

*fallback*chain + streaming

*SLA*guardrails

## Module 01 unlocks with *PRO*. The retrieval stack with EXPERT.

Module 01 (~3h) ships multi-format parsers, the 4-strategy ChunkingFactory, the FastAPI upload API, and a React drag-and-drop uploader — included with PRO. Modules 02–05 (~13.5h) layer the Pinecone HNSW index, hybrid retriever, cross-encoder reranker, RAGAS harness, multi-provider LLM gateway, and multi-tenant blueprint — and unlock with EXPERT.

[Unlock with PRO →](https://ai-de.net#unlock)

[Unlock with EXPERT →](https://ai-de.net#unlock)

[Unlock with EXPERT →](https://ai-de.net#unlock)

[Unlock with EXPERT →](https://ai-de.net#unlock)

[Unlock with EXPERT →](https://ai-de.net#unlock)

[Backed by curriculumRAG Learning PathOpen curriculum](https://ai-de.net/learn/rag) 

*foundation*for the project — same stack you build here, taught from chunking and retrieval-quality first principles. EXPERT subscribers get full access to all modules.

## Foundation. Retrieval quality. *Platform.*

Each phase ends with a tagged release, a passing RAGAS canary on the 4-metric harness, and a measurable retrieval-quality delta on the seed corpus. No ambiguity about where you are.

Multi-format ingest live locally. ChunkingFactory routing by document tag; recursive default benchmarked at +16pp over fixed-size.

- ✓PDF + DOCX + Markdown + Text parsers with page-marker / table-aware extraction
- ✓ChunkingFactory with 4 strategies + measured A/B vs golden set
- ✓FastAPI upload + React uploader + background processing with status polling

Hybrid retrieval + cross-encoder reranker live. RAGAS 4-metric canary green; faithfulness > 0.85 enforced as quality floor.

- ✓Pinecone HNSW (1536-dim) + BM25 + RRF merge with k=60 fusion constant
- ✓Cross-encoder rerank (top-50 → top-10) with disable-able score floor
- ✓RAGAS canary in CI on the 40-question golden set + Prometheus metrics

LLM Gateway with fallback chain + per-tenant cost tracker. Multi-tenant namespace isolation, SLA + circuit breaker, runbook drilled.

- ✓LLM gateway library with response cache (1h TTL) + per-tenant rate limit
- ✓TenantManager with namespace-per-tenant + defense-in-depth filtering
- ✓Failure-mode runbook + circuit-breaker degraded mode in M05 capstone

## One command. Local *FastAPI* + Qdrant + Redis (no API key needed).

### What lives in the repo

You get the unified production code on day one — FastAPI as the gateway, Qdrant for local vector storage (Pinecone-compatible interface), Redis for caching + rate-limit fallback, sentence-transformers cross-encoder for reranking, plus the lazy-init OpenAI/Anthropic clients so imports stay clean even without keys.

- **docker-compose.yml** — Qdrant + Redis + API container with health checks
- **app/services/document_parser.py + chunking.py** — pypdf + python-docx + 4-strategy ChunkingFactory
- **app/services/vector_store.py + rag_service.py** — Pinecone/Qdrant + hybrid retrieve + cross-encoder reranker
- **scripts/ragas_eval.py** — RAGAS canary harness with 4-metric scoring
- **gateway/llm_gateway.py + tenant/tenant_manager.py** — fallback chain + response cache + per-tenant quota
- **docs/adr/ + docs/cost-model/** — 5 ADRs (one Deprecated) + the runnable cost-model CSV

#### Enterprise RAG Starter Kit

Pre-built RAG platform with parsers, ChunkingFactory, hybrid retriever, RAGAS harness, LLM gateway, and the 4-document seed corpus that powered the chunking A/B benchmark. Now bundled: 5 committed ADR markdown files (docs/adr/) and the runnable cost-model CSV (docs/cost-model/) — unzip and read them straight from the repo.

## The same RAG demo — but built for the *relevance-review* case.

Most RAG tutorials stop at vector search + a prompt template. This shows what changes when retrieval failures land in your inbox, not the LLM’s — and a relevance reviewer wants to see the chunking-A/B numbers behind your defaults.

`ChunkingFactory` routes by tag; recursive default (78%), semantic opt-in for legal/medical (85%) — ADR-003`BM25 + Pinecone HNSW` fused via `RRF k=60` — ADR-001`ms-marco-MiniLM-L-6-v2`) over top-50 → top-10 with disable-able score floor — ADR-002`> 0.85` from `sla.yaml``LLMGateway` with `gpt-4o → gpt-4o-mini` fallback + 1h response cache — ADR-004
## Write the *ADRs* staff retrieval engineers actually get judged on.

Five ADRs ship inside the starter-kit zip at `docs/adr/`, one per major decision in the build, including a real *Deprecated* ADR documenting the fixed-size-chunking → recursive reversal that the chunking-A/B benchmark forced. [Preview ADR-001 →](https://ai-de.net/downloads/enterprise-rag/docs/adr/001-hybrid-retrieval-rrf.md)

#### Hybrid retrieval (BM25 + dense) with Reciprocal Rank Fusion

`RRF k=60`; feed top-50 to the reranker
#### Cross-encoder reranking (top-50 → top-10) precision lever

`ms-marco-MiniLM-L-6-v2` cross-encoder on dedicated CPU pool; rerank top-50 → top-10 with score floor
#### Recursive chunking default; semantic for high-value docs only

`ChunkingFactory.from_metadata` — recursive default; semantic for `legal/medical/contract` tags; paragraph for clean Markdown
#### LLM Gateway with fallback chain (gpt-4o → gpt-4o-mini)

`LLMGateway` singleton — fallback chain, 1h response cache, per-tenant rate-limit + cost cap, in-process v1
## Read the *per-query* story, not just the latency one.

Module 04 ships a runnable cost-model CSV inside the starter-kit zip at `docs/cost-model/`. 5-tenant reference load (10k qpd · 300k req/mo), real OpenAI + Pinecone serverless + AWS list prices, with the model-cascade and 20%-cache-hit levers wired up. The version you defend to a CFO. [Preview the CSV →](https://ai-de.net/downloads/enterprise-rag/docs/cost-model/enterprise-rag-cost-model.csv)

#### Optimization levers

## Async architecture review with a *staff-level* reviewer (cohort beta).

Submit your repo, your ADR draft, or your RAGAS canary numbers. A staff or principal-level reviewer who has shipped this exact stack responds within 7 days with line-by-line comments. Cohort capped at 12 members.

### Bring a *diff*, an ADR draft, or a RAGAS regression report.

The cohort beta runs as async architecture review — pick a reviewer by topic, send the artifact, get inline comments + a Loom walkthrough back. No back-and-forth scheduling. No 30-minute slot pressure.

## PRO unlocks Module 01. EXPERT unlocks the *full* retrieval stack.

PRO is the entry point — Module 01 (multi-format parsers + 4-strategy chunker + upload API + uploader UI) plus the rest of the PRO catalog. EXPERT unlocks Modules 02–05 of this build, the 5 ADRs, the cost-model CSV, and the cohort-beta async architecture review.

## Pick this if you *own retrieval quality*, not just the prompt.

#### AI engineers shipping RAG to staff/principal

You debug retrieval failures, you tune reranker thresholds, and your manager asks 'what's our hit-rate@10?' on review day. The chunking A/B + RAGAS harness is the answer.

#### ML platform leads building retrieval infra

You absorb retrieval as a platform service. Pinecone + BM25 + reranker + LLM gateway as a single library that the rest of the org calls — that's the playbook.

#### Founding engineers · AI startups

Your first paying customer will ask 'why did the bot say that?' before they ask about scale. Citations + explainability + RAGAS faithfulness is the answer in one repo.

#### Engineering managers · AI

You need a relevance-review rubric for the AI roadmap your VP will ask about. The 5 ADRs (one Deprecated) are exactly the artifacts a panel actually opens.

## Going deeper? Four *tracks* back this project.

The RAG curriculum is the foundation for the project. These four tracks let you go deeper on the parts that matter most for your role.

## Quick answers.

## Ready to ship a *retrieval-quality* RAG platform?

Start with PRO ($29/mo) for Module 01 — multi-format parsers + 4-strategy ChunkingFactory. Or unlock the full 5-module retrieval stack plus 5 ADRs, the cost-model CSV, and cohort-beta architecture review with EXPERT ($79/mo).
