# Live CLI and API research examples

Both full runs finished on October 9, 2026 using real OpenRouter, SerpApi Google search, and website fetching/extraction. Each used a different AI topic and reader goal, three search pages, ten results per page, and a cap of thirty clean URLs. The model was `openrouter:deepseek/deepseek-v4.1-flash`.

## Contents

- [Results](#results)
- [CLI run](#cli-run)
- [API run](#api-run)
- [Runtime and validation](#runtime-and-validation)
- [Earlier attempts](#earlier-attempts)
- [Archive integrity](#archive-integrity)

## Results

| | CLI | API |
| --- | --- | --- |
| Topic | RAG vs fine-tuning | AI agent evaluation |
| Chosen format | Comparative decision brief with per-dimension evidence strength and a staged decision guide | Implementation guide distinguishing documented practice from untested examples |
| Final document | [2026-10-09-21-39-06-content.md](runs/rag-vs-fine-tuning-20261009T213906Z/output/2026-10-09-21-39-06-content.md) | [2026-10-09-21-40-43-content.md](runs-api/ai-agent-evaluation-20261009T214043Z/output/2026-10-09-21-40-43-content.md) |
| Final report | [run.json](runs/rag-vs-fine-tuning-20261009T213906Z/output/run.json) | [run.json](runs-api/ai-agent-evaluation-20261009T214043Z/output/run.json) |
| Authoring checks | [authoring.json](runs/rag-vs-fine-tuning-20261009T213906Z/output/authoring.json) | [authoring.json](runs-api/ai-agent-evaluation-20261009T214043Z/output/authoring.json) |
| Status | `degraded` | `degraded` |
| Words | 5,402 | 5,160 |
| Clean URLs / extracted sources | 30 / 18 | 30 / 22 |
| Distinct citations checked | 18 | 22 |
| Valid Mermaid diagrams | 1 | 2 |
| Synthesis attempts / citation repairs | 1 / 0 | 1 / 0 |
| Full-run duration | 522.22 seconds | 425.68 seconds |

Both documents contain a top table of contents, source citations, References, and a final cited **Why this format** section. Their validated synthesis plans preserve evidence limitations and explain the chosen outline: [CLI plan](runs/rag-vs-fine-tuning-20261009T213906Z/research/synthesis.json), [API plan](runs-api/ai-agent-evaluation-20261009T214043Z/research/synthesis.json).

All nine phases completed. Both reports retain `blog_length` and `too_few_sources`: the soft length target is 2,000–5,000 words, and thirty requested URLs require at least twenty-four extracted sources to avoid the source-count finding. Citation identity, document structure, evidence-plan provenance, and actual diagram rendering passed without repairs. These checks do not establish that every published claim is supported; a formal source-aware editorial evaluation was not run.

## CLI run

**Topic:** RAG vs fine-tuning

**Goal:** Help an engineering team choose between RAG, fine-tuning, and a hybrid approach for enterprise AI assistants by comparing data freshness, evaluation, latency, cost, and security while preserving evidence limits and avoiding unsupported rankings.

Command executed from the repository root:

```bash
LANGSMITH_TRACING=false RECURSION_LIMIT=200 \
SEARCH_TIMEOUT_SECONDS=120 MODEL_TIMEOUT_SECONDS=120 \
uv run --locked content-writer 'RAG vs fine-tuning' \
  --goal 'Help an engineering team choose between RAG, fine-tuning, and a hybrid approach for enterprise AI assistants by comparing data freshness, evaluation, latency, cost, and security while preserving evidence limits and avoiding unsupported rankings.'
```

Captured output ([console transcript](runs/rag-vs-fine-tuning-20261009T213906Z/logs/console.txt)):

```text
run_id: rag-vs-fine-tuning-20261009T213906Z
workspace: runs/rag-vs-fine-tuning-20261009T213906Z
status: degraded
blog_path: runs/rag-vs-fine-tuning-20261009T213906Z/output/2026-10-09-21-39-06-content.md
blog_exists: True
```

Exit status was **3**, the full CLI's degraded outcome. The retained `blog_path` and `blog_exists` compatibility keys refer to the timestamped content file. The filename uses the saved start time in UTC and remains stable on resume.

Original workspace: `runs/rag-vs-fine-tuning-20261009T213906Z/`. Archived copy: [`runs/rag-vs-fine-tuning-20261009T213906Z/`](runs/rag-vs-fine-tuning-20261009T213906Z/).

## API run

**Topic:** AI agent evaluation

**Goal:** Create a practical implementation guide for evaluating tool-using AI agents, covering task datasets, success criteria, failure analysis, observability, and bounded retries; distinguish documented techniques from untested examples.

The API and separate worker used `API_RUN_PROFILE=production`, `API_RUNS_DIR=runs-api`, and an isolated native PostgreSQL **14.22** database on loopback port **55432**. This capture did not use Docker or fixture providers. Migrations, health checks, and OpenAPI returned successfully: [preflight](api-preflight.json), [migration output](verification/api-migrations.txt).

Commands used for the service and worker, in separate terminals:

```bash
export API_DATABASE=postgresql://research@127.0.0.1:55432/research
export API_RUNS_DIR=runs-api
export API_RUN_PROFILE=production
uv run --locked python -m application.migrations
uv run --locked uvicorn api.main:create_app --factory \
  --host 127.0.0.1 --port 8011
```

```bash
API_DATABASE=postgresql://research@127.0.0.1:55432/research \
API_RUNS_DIR=runs-api API_RUN_PROFILE=production \
LANGSMITH_TRACING=false RECURSION_LIMIT=200 \
SEARCH_TIMEOUT_SECONDS=120 MODEL_TIMEOUT_SECONDS=120 \
uv run --locked python -m workers.research_worker --once
```

The following curl request is equivalent to the actual HTTP POST captured in [api-submission.json](api-submission.json); the exact JSON payload is [api-request.json](api-request.json). Use a fresh idempotency key for a new run.

```bash
API=http://127.0.0.1:8011
curl -sS -i -H 'Content-Type: application/json' \
  -H 'Idempotency-Key: live-ai-agent-evaluation-20261009-staged-checkpoints-2' \
  --data-binary @runs.example/api-request.json "$API/v1/runs"
```

Captured submission:

```text
HTTP/1.1 202 Accepted
location: /v1/jobs/532ff862-7d5c-449a-932d-2050fb6961d8
{"job_id":"532ff862-7d5c-449a-932d-2050fb6961d8","status":"queued","operation":"research","run_id":null,"links":{"status":"/v1/jobs/532ff862-7d5c-449a-932d-2050fb6961d8"}}
```

Read the terminal job and report:

```bash
JOB=532ff862-7d5c-449a-932d-2050fb6961d8
RUN=ai-agent-evaluation-20261009T214043Z
curl -fsS "$API/v1/jobs/$JOB" | uv run python -m json.tool
curl -fsS "$API/v1/runs/$RUN/report" | uv run python -m json.tool
curl -fsS "$API/v1/runs/$RUN/artifacts" | uv run python -m json.tool
```

Captured job response:

```json
{
  "job_id": "532ff862-7d5c-449a-932d-2050fb6961d8",
  "status": "degraded",
  "operation": "research",
  "run_id": "ai-agent-evaluation-20261009T214043Z",
  "phase": "report",
  "attempt": 1,
  "status_reasons": [
    "blog_length",
    "too_few_sources"
  ],
  "error": null,
  "created_at": "2026-10-09T15:40:41.520198-06:00",
  "updated_at": "2026-10-09T15:47:48.783752-06:00",
  "links": {
    "status": "/v1/jobs/532ff862-7d5c-449a-932d-2050fb6961d8"
  }
}
```

Selected fields from the captured final report ([complete response](runs-api/ai-agent-evaluation-20261009T214043Z/api-evidence/report.json)):

```json
{
  "status": "degraded",
  "status_reasons": [
    "blog_length",
    "too_few_sources"
  ],
  "urls_clean": 30,
  "urls_extracted": 22,
  "citation_count": 22,
  "blog_path": "output/2026-10-09-21-40-43-content.md"
}
```

The [run status](runs-api/ai-agent-evaluation-20261009T214043Z/api-evidence/run.json) records all nine phases. The [artifact listing](runs-api/ai-agent-evaluation-20261009T214043Z/api-evidence/artifacts.json) contains **37** downloadable files. The one-shot worker exited **0**; the job's actual terminal outcome is `degraded`.

Download command:

```bash
CONTENT=output/2026-10-09-21-40-43-content.md
curl -fsS -D - -o "$(basename "$CONTENT")" \
  "$API/v1/runs/$RUN/artifacts/$CONTENT"
```

Captured response headers:

```text
HTTP/1.1 200 OK
content-type: text/markdown; charset=utf-8
content-disposition: attachment; filename="2026-10-09-21-40-43-content.md"
content-length: 38243
```

Download verification ([metadata](runs-api/ai-agent-evaluation-20261009T214043Z/api-evidence/download.json)):

```json
{
  "http_status": 200,
  "content_type": "text/markdown; charset=utf-8",
  "content_disposition": "attachment; filename=\"2026-10-09-21-40-43-content.md\"",
  "content_length": 38243,
  "sha256": "08e293f2de5b7c254006adfaf9328f43401bf7d003a6eaa123cb5fe488506f95",
  "workspace_bytes_identical": true
}
```

The downloaded response body is also preserved in [api-evidence](runs-api/ai-agent-evaluation-20261009T214043Z/api-evidence/2026-10-09-21-40-43-content.md). Its bytes match the workspace document.

Original workspace: `runs-api/ai-agent-evaluation-20261009T214043Z/`. Archived copy: [`runs-api/ai-agent-evaluation-20261009T214043Z/`](runs-api/ai-agent-evaluation-20261009T214043Z/).

## Runtime and validation

Temporary environment overrides were `LANGSMITH_TRACING=false`, `RECURSION_LIMIT=200`, `SEARCH_TIMEOUT_SECONDS=120`, and `MODEL_TIMEOUT_SECONDS=120`. These allowed long corpus-reading conversations and slower live search responses; `.env` was unchanged. Hosted tracing was disabled for these captures, while local execution logs and run reports remained available.

Live execution exposed and fixed synthesis validation feedback, stale phase selection during resume, and shared authoring checkpoint conversations. The analyst and parent now have a read-only synthesis validator; the application independently validates the plan. Synthesize, Write, and each repair use separate checkpoint threads and exchange validated on-disk artifacts. Each final run used one synthesis attempt, one substantive generation, and no repairs. Existing failed workspaces retained their reservations.

`make check` passed **794 offline tests**, with **3 live pytest tests deselected** and **88.27% coverage**. Ruff formatting/lint, strict mypy over 154 source files, and the dependency lock check passed. `make boundary build` also passed. Logs: [quality checks](verification/make-check.txt), [boundary and package build](verification/boundary-build.txt), [live document checks](verification/document-checks.json).

The temporary API server and private PostgreSQL instance were stopped after response capture. The private database files were retained locally. The API queue/checkpoints lived in PostgreSQL; no database dump is included. CLI SQLite checkpoints are included in its workspace copy.

## Earlier attempts

[Earlier CLI attempts](attempts/runs/) and [earlier API attempts](attempts/runs-api/) preserve provider and authoring failures separately from these completed outputs. Earlier issues included authentication/model access, search timeouts, invalid synthesis, and a shared checkpoint conversation repeating synthesis during Write. Attempt counters were not reset. Each new request has its own run ID; failed jobs were not relabeled as successful.

## Archive integrity

The final workspace copies were made after both processes terminated. [workspace-sha256.json](verification/workspace-sha256.json) records **73** original workspace files and confirms byte-for-byte equality of every copy. Additional HTTP evidence, verification records, and console transcripts are stored alongside those copies. A scan against configured credential values passed; `.env` is excluded. Runtime directories remain ignored, while these nested example directories are versionable.
