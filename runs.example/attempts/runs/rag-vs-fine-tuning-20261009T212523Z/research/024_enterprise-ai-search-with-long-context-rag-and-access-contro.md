---
source_id: S-24
url: https://intl.cloud.tencent.com/techpedia/148026?lang=en
title: Enterprise AI Search with Long Context, RAG, and Access Control
author: V Cloudbuilder
published: null
fetched: '2026-10-09T21:25:38Z'
word_count: 2019
---
# Enterprise AI Search with Long Context, RAG, and Access Control

Enterprise AI search is not a choice between RAG and a large context window. It is a governed retrieval system that must find the right version of permitted evidence before a model sees any content. Buyers should therefore evaluate source ingestion, parsing, lexical and vector retrieval, authorization, reranking, evidence controls, and deletion as one architecture. The language model is an important component, but it is not the search product.

Want to evaluate Hy4 Preview and other models for synthesizing authorized evidence through one API? Visit [Tencent Cloud TokenHub](https://www.tencentcloud.com/act/pro/tokenhub?lang=en&pg=) to review current models, integration options, and trial information.

## Frame the search jobs before choosing components

An internal search service usually handles at least three jobs. Navigational search finds a known policy, ticket, repository, or account record. Discovery search helps a person explore material related to a concept. Answer search combines evidence from several sources into a response. Each job has a different success condition: an exact document at rank one, broad but relevant coverage, or a grounded answer with traceable citations.

Start a selection project with representative queries rather than a vector-database shortlist. Record entity names, acronyms, identifiers, dates, languages, and expected filters. State whether the user needs a document, a passage, or a synthesized conclusion, and define an acceptable latency envelope. A system that performs well on broad questions may still fail on an error code or contract number.

Create a source registry in parallel. For each wiki, drive, ticket system, code repository, CRM, and archive, identify the tenant, owner, authoritative version, update mechanism, retention rule, and source of permissions. This inventory exposes the real integration problem: different systems use different identities, ACL semantics, and deletion events.

## Treat parsing and indexing as a fidelity layer

Ingestion should preserve a stable source ID, version, content hash, modification time, and tombstone state. Parsing should retain headings, page locations, table headers, list structure, attachments, and code paths. A passage is not operationally useful if its citation cannot take an authorized user back to the exact source location.

Chunking should follow content structure instead of a universal token count. A policy clause should remain attached to its exceptions. A support incident should keep the symptom near the resolution. A table row needs its headers, while code requires the repository path and symbol boundaries. Every chunk should inherit tenant, document ACL, classification, effective dates, version, and provenance.

The inverted and vector indexes need common document and chunk identifiers. That makes it possible to update one version, investigate a result, or delete every derived representation. Changing an embedding model requires a new index and re-embedding; equal dimensions do not imply that vectors from two models share a comparable space.

## Use lexical and vector retrieval for different failure modes

Lexical retrieval is strong for exact phrases, product names, identifiers, and error strings. Dense retrieval is useful when the query and the relevant passage express the same concept with different vocabulary. The original [dense passage retrieval research](https://aclanthology.org/2020.emnlp-main.550/) illustrates why semantic representations can complement traditional sparse retrieval, but results from one public benchmark do not establish performance on a company's own content.

A practical hybrid design runs both paths, merges their candidate lists with a documented fusion method, and then applies a reranker. The reranker can consider query-passage relevance, source authority, version, freshness, and result diversity. It should avoid filling the result page with adjacent chunks from one document.

Query understanding can detect language, entities, dates, document types, and whether the user wants navigation or an answer. Rewriting may expand synonyms or an internal acronym, but it must preserve the original query for audit and must never expand the user's authorization scope. For a known-item query, returning the source directly may be more useful and faster than generating prose.

## Make authorization a pre-retrieval constraint

Access control is application logic, not a model instruction. Authenticate the user and session, resolve tenant membership and groups, and evaluate role, document ACL, attributes, and time-sensitive policy before searching. The [NIST ABAC guide](https://csrc.nist.gov/pubs/sp/800/162/upd2/final) describes authorization in terms of subject, object, requested operation, environmental attributes, and policy. That provides a useful design vocabulary even when an enterprise uses a mixture of RBAC, ACLs, and attribute rules.

Push the allowed scope into both lexical and vector queries. Retrieving a global top-k and removing forbidden items afterward is unsafe and degrades recall: titles, snippets, counts, or timing can leak, while permitted passages may never enter the initial candidate set. Strong tenant partitioning or separate indexes can reduce the blast radius further; a tenant ID written into a prompt is not isolation.

Document-level ACLs are sometimes too coarse. A board package may contain a broadly visible agenda and restricted attachments. A spreadsheet may impose row or field constraints. In those cases, split content only within a common permission boundary and carry chunk-, row-, or field-level policies into the index. Search snippets, citations, result caches, conversation summaries, query logs, and offline evaluation copies must respect the same rules.

Authorization is also dynamic. A group removal or document restriction needs to invalidate cached results and summaries promptly. Citation links should reauthorize at click time rather than assume that access at answer-generation time remains valid.

## Build RAG as an evidence pipeline

RAG should add provenance to search, not disguise weak retrieval. A controlled sequence is: authorized candidate generation, fusion and deduplication, reranking, evidence packaging, response generation, and citation verification. The generator receives only permitted candidates. Each material claim should map to a source ID, document version, and locatable passage; the presentation layer can then render links that the user can open after a fresh permission check.

Keep system instructions separate from retrieved text. OWASP notes that files and websites can contain [indirect prompt injections](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) and that RAG does not fully remove that risk. Text such as “ignore previous instructions” inside a document remains untrusted evidence, not an executable command. Any write, message, or privileged lookup must pass deterministic parameter validation and authorization, with human approval where the action is consequential.

## Route between long context and compressed evidence

Long context is valuable after retrieval when the permitted candidate set is coherent and relationships across sections matter. Comparing three policy editions may require full clauses, revision notes, definitions, and appendices. Keeping those pieces together can preserve dependencies that aggressive chunking would lose.

However, context capacity is not a reason to send every accessible document. Irrelevant and duplicate material consumes latency and budget, competes with critical evidence, and makes failures harder to diagnose. If the corpus is large or the question asks for a narrow fact, retrieve and rerank first. Then deduplicate, merge neighboring chunks, or apply extractive compression.

Compression must remain reversible. Store the source ID and original span for every retained statement; never promote a model-written summary without provenance into a new authoritative source. For high-risk questions, include both the compressed view and selected original windows so the model can compare them.

The routing decision can use the post-authorization token count, query type, cross-document dependency, risk level, and latency budget. A small RAG packet is often right for precise lookup. A larger context can help synthesis across an already narrowed evidence set. In both routes, authorization occurs before content enters the model.

## Define behavior for conflicts, staleness, and insufficient evidence

An index should distinguish effective, superseded, withdrawn, and draft material. Ranking can favor a current authoritative source, but it should not hide a conflict between two active policies. When sources disagree, the answer should show both documents, their dates, and the disputed point, then route the question to the content owner. The model should not silently choose a winner.

A post-generation verifier should ask four separate questions: Does each cited passage exist? Is the user still authorized? Is the version current? Does the passage directly support the associated claim? Missing citations, low-relevance evidence, an all-stale result set, or a question beyond the permitted corpus should produce a qualified answer or refusal that explains the gap.

Refusal rate should not be minimized in isolation. In finance, legal, HR, and security workflows, revealing insufficient evidence is safer than generating a confident completion. Teams should label “should answer,” “may answer partially,” and “should refuse” examples before comparing models.

## Evaluate retrieval, answers, security, and latency separately

At the retrieval layer, measure Recall@k: among relevant and permitted chunks, how many appear in the first k results? Break the result down by exact identifiers, acronym expansion, natural-language questions, multilingual queries, date filters, and source. Add decoy documents that are highly relevant but forbidden, and confirm that they never appear in candidates, snippets, citations, caches, or model context.

At the answer layer, evaluate groundedness at the claim level. A fluent response can still cite a passage that does not support it. Track citation correctness, coverage of material claims, conflict disclosure, stale-source use, and behavior on questions that should be refused. Human reviewers should adjudicate high-risk slices rather than rely only on another model's score.

For the system, measure end-to-end latency and the contribution from identity resolution, policy evaluation, lexical and vector search, reranking, time to first model token, and full generation. Use tail percentiles, not only averages. Test cold indexes, a slow policy service, a stale cache, and a degraded model endpoint so the fallback path is visible.

A useful PoC draws samples from real query logs after appropriate privacy handling. Business owners label expected sources, acceptable claims, and permission conditions. Teams should declare launch thresholds before the test and inspect the worst department or source slice. A good overall score cannot compensate for an authorization breach or near-zero recall on a critical collection.

## Design audit and deletion as product capabilities

For each query, retain enough metadata to reconstruct the decision: user and tenant identifiers, policy version, original and rewritten query, candidate document IDs, filtering reasons, ranker version, model and prompt template version, citations, and final disposition. Do not copy sensitive documents wholesale into logs by default. IDs, hashes, and minimal protected excerpts are usually more appropriate, with separate access controls and retention rules for the audit store.

Deletion has to reach every derivative. A connector tombstone or retention event should remove or invalidate the source copy, parsed text, inverted postings, vectors, reranking cache, answer cache, conversation summaries, and evaluation samples. Use a deletion queue with retries, completion receipts, and sampling checks. Versioned citations must fail closed or reauthorize if a user opens an old answer. “No longer appears in a normal search” is not proof of deletion.

## Place Hy4 Preview at the correct layer

Tencent describes Hy4 Preview as an early version in the Hy4 iteration. Official model information lists a 1M context window and 960k maximum input. Those specifications make it a candidate for a PoC involving authorized multi-document evidence, structured synthesis, and citation formatting. They do not prove retrieval recall, access isolation, groundedness, or production readiness. Preview behavior, long-input recall, latency, cost, error handling, and fallback still require workload-specific tests.

TokenHub can provide a unified model-access path for evaluation. The cited official materials do not establish it as an out-of-the-box enterprise search product with source connectors, ACL synchronization, hybrid indexes, a reranker, or deletion governance. A buying decision should therefore list the search engine, identity and policy service, model gateway, and generation model as separate responsibilities with explicit interfaces and exit plans.

## Frequently asked questions

**Can a long context window replace vector retrieval?** Not for a changing enterprise corpus. Retrieval locates current evidence inside the user's permitted scope; long context is better used to preserve full sections and relationships after that evidence set has been narrowed.

**Why not retrieve globally and remove forbidden results afterward?** Post-filtering can expose titles, snippets, counts, or timing, and permitted evidence may never enter the global top-k. Authorization needs to constrain both candidate generators.

## A practical decision rule

Select the architecture that can first prove: the right current version is retrievable, forbidden evidence cannot enter any candidate set, claims return to authorized sources, weak evidence triggers a controlled response, and deletion reaches every derivative. Use RAG to narrow and locate evidence; use long context to reason over a larger but already authorized evidence set. Enterprise AI search becomes deployable only when every answer remains permission-aware, traceable, measurable, and deletable.
