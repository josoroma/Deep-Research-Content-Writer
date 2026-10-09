![Content Writer: evidence-driven research and writing, from search to publish](docs/images/cover.png)

# Deep Research - Content Writer

[Quality gates](https://github.com/josoroma/Deep-Research-Content-Writer/actions/workflows/quality.yml) · [Live walkthrough](https://josoroma.github.io/Deep-Research-Content-Writer) · [Engineering standard](docs/ENGINEERING.md) · [Homepage](https://josoroma.github.io/)

![Content Writer: evidence-first research, writing, and validation](docs/images/content-writer-01-overview.png)

**From a research question to a source-backed document.** Content Writer collects web evidence, chooses a format suited to the topic and reader, and records whether the final document passed its checks. The writing target is **2,000–5,000 words**, with length handled as a soft runtime quality condition.

## Guide the result

![Provide a topic and reader goal; select an evidence-based document format](docs/images/content-writer-02-goals-and-formats.png)

```bash
uv run content-writer "Agent framework deployment options" \
  --goal "Help a small team choose a deployment approach"
```

A successful full run prints this summary shape; replace `<run_id>` with the generated ID:

```text
run_id: <run_id>
workspace: runs/<run_id>
status: completed
blog_path: runs/<run_id>/output/{yyyy-mm-dd-hh-mm-ss}-content.md
blog_exists: True
```

`--goal` is optional on the CLI; the API accepts the optional JSON field `goal`. A resumed run keeps its original topic, goal, and evidence. To change the goal, start a new run. The [CLI walkthrough](https://josoroma.github.io/Deep-Research-Content-Writer/docs/pages/running-a-run.html#cli) includes captured output for Search, Collect, and Author.

The CLI prints `completed` for success; the final report and API job use `succeeded`. Each finished document starts with a table of contents and ends with References and a cited **Why this format** explanation. Diagrams are included when they help explain the evidence.

## Follow the research pipeline

![The Search, Collect, Author, and Report stages](docs/images/content-writer-03-pipeline.png)

Use the full command above for an end-to-end run, or inspect intermediate artifacts by running stages separately:

```bash
uv run content-writer "Python LangChain Deep Agents Startup Ideas" \
  --search-only --pages 3 --per-page 10 --max-urls 30

RUN="runs/<run_id>"  # Use the workspace path printed by Search
uv run content-writer --corpus-only --workspace "$RUN"
uv run content-writer --author-only --workspace "$RUN"

# Continue an interrupted full CLI run
uv run content-writer --resume "<run_id>"
```

Run workspaces are local generated data. The [saved live walkthrough](docs/pages/running-a-run.html#live-examples) and [example index](runs.example/README.md) include the exact topics, goals, commands, outputs, and archived workspaces from October 9, 2026:

| Entry point | Document and chosen format | Sources cited | Words | Diagrams |
| --- | --- | --- | --- | --- |
| CLI | [RAG vs fine-tuning: comparative decision brief](runs.example/runs/rag-vs-fine-tuning-20261009T213906Z/output/2026-10-09-21-39-06-content.md) | 18 | 5,402 | 1 |
| API | [AI agent evaluation: implementation guide](runs.example/runs-api/ai-agent-evaluation-20261009T214043Z/output/2026-10-09-21-40-43-content.md) | 22 | 5,160 | 2 |

Both completed all nine phases and passed citation identity, structure, and diagram checks without citation repairs. Their reports remain `degraded`: each exceeded 5,000 words and extracted fewer than 24 sources from 30 clean URLs. The saved commands record temporary timeout and graph-step overrides used for these live runs.

## Get started locally

![Prerequisites, setup commands, and provider configuration](docs/images/content-writer-04-setup.png)

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), Git, and Make. Development setup and Mermaid checks use Node.js 22 with npm; uv installs Python 3.12.

```bash
make setup       # Dependencies, Mermaid renderer, Git hook
make check       # Formatting, types, offline tests, coverage
make demo-api    # End-to-end offline demo, no provider keys
```

For live research, create `.env` and add your credentials:

```bash
cp -n .env.example .env
```

```dotenv
SEARCH_PROVIDER=serpapi
SERPAPI_API_KEY=<your SerpApi key>
OPENROUTER_API_KEY=<your OpenRouter key>
CRAWLER_CONTACT=<your URL or email>
```

The `serper` search provider can be selected instead with its own key. `.env`, `runs/`, and `runs-api/` are Git-ignored; archived copies under `runs.example/` are versionable. If upgrading an existing checkout, run `uv sync --locked`.

## Run as a service

![HTTP API, PostgreSQL queue, worker, artifacts, and endpoints](docs/images/content-writer-05-service-api.png)

The FastAPI service queues jobs for a separate worker and requires PostgreSQL. To use the provided Docker database:

```bash
make api-up
export API_DATABASE=postgresql://research:research@127.0.0.1:5432/research
export API_RUNS_DIR=runs-api
export API_RUN_PROFILE=production
make migrate-api
make run-api

# In another terminal (with the same database and workspace configuration):
make worker-api
```

An existing native PostgreSQL instance also works: skip `make api-up` and set `API_DATABASE` to its connection string. The API and worker must share the database, run profile, and workspace root.

To test without external model, search, or website calls, set `API_RUN_PROFILE=fixture` for both API and worker before starting them. Keep `API_DATABASE` configured so the separate processes share the queue.

Submit a topic and reader goal from another terminal:

```bash
API=http://127.0.0.1:8000
curl -sS -i -H 'Content-Type: application/json' \
  -H 'Idempotency-Key: guide-research-1' \
  -d '{"mode":"research","topic":"Research telemetry quality","goal":"Explain the available telemetry and its limits","pages":1,"per_page":10,"max_urls":3}' \
  "$API/v1/runs"
```

Response shape, with the generated job ID replaced:

```text
HTTP/1.1 202 Accepted
location: /v1/jobs/<job_id>
{"job_id":"<job_id>","status":"queued","operation":"research","run_id":null,"links":{"status":"/v1/jobs/<job_id>"}}
```

Poll until the job reaches a terminal state, then use its `run_id` to read the report and download the document:

```bash
JOB="<job_id>"
curl -fsS "$API/v1/jobs/$JOB" | uv run python -m json.tool

RUN="<run_id>"  # Copy from the finished job
curl -fsS "$API/v1/runs/$RUN/report" | uv run python -m json.tool
CONTENT=$(curl -fsS "$API/v1/runs/$RUN/report" | \
  uv run python -c 'import json,sys; print(json.load(sys.stdin)["report"]["blog_path"])')
curl -fsS -D - -o "$(basename "$CONTENT")" "$API/v1/runs/$RUN/artifacts/$CONTENT"
```

The current 3-source fixture completed with job status `succeeded`, 18 artifacts, and a 33,570-byte Markdown download. Its authoring record reported format `Evidence review`, 2,020 words, 3 checked citations, and no repairs. These are fixture results; live counts and formats vary. The [API walkthrough](https://josoroma.github.io/Deep-Research-Content-Writer/docs/pages/running-a-run.html#api) includes response bodies, artifact listings, logs, and resume commands with outputs.

The [live production API capture](runs.example/README.md#api-run) used real PostgreSQL, OpenRouter, SerpApi, and website extraction. It completed all nine phases with 22 cited sources, 37 downloadable artifacts, and a 38,243-byte Markdown download verified against the workspace. Its terminal status was `degraded`: 5,160 words exceeded the 5,000-word target, and 22 extracted sources fell below the 24-source threshold for 30 requested URLs.

[API docs](http://127.0.0.1:8000/docs) · [OpenAPI schema](http://127.0.0.1:8000/openapi.json) · [Complete walkthrough](https://josoroma.github.io/Deep-Research-Content-Writer/docs/pages/running-a-run.html#api)

## Inspect a run

![Workspace files for research, authoring, logs, and the final report](docs/images/content-writer-06-workspace.png)

Each run has a separate workspace. The finished document is `output/{yyyy-mm-dd-hh-mm-ss}-content.md`, for example `output/2026-10-09-17-30-00-content.md`. The filename uses the run's start time in UTC, with a 24-hour clock and second precision. It is saved as `content_started_at` in `output/authoring_state.json` and retained when the run resumes. CLI outputs live under `runs/<run_id>/`; API outputs live under `runs-api/<run_id>/` by default. The existing `blog_path` report field points to this timestamped file. Authoring checks are recorded in `output/authoring.json`, and full runs also produce `output/run.json`. Research sources and the validated synthesis remain available for inspection.

## Agent architecture

![Coordinator and specialist agents](docs/images/content-writer-07-agents.png)

The application coordinates bounded agent tasks and owns finalization. The implementation uses [DeepAgents](https://docs.langchain.com/oss/python/deepagents/overview) on [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview), with configurable models through OpenRouter. Agent roles and tool boundaries are documented in [architecture](docs/architecture/README.md).

The analyst and orchestrator use the read-only `validate_synthesis` tool to correct schema and exact-excerpt errors before handing off the plan. The application independently validates and commits it before writing begins. Synthesize, Write, and each citation repair use separate checkpoint conversations and exchange validated workspace artifacts.

## Quality and recovery

![Success, degradation, failure, and the citation repair gate](docs/images/content-writer-08-quality-gates.png)

Runs keep their recorded outcomes and available drafts. Citation repairs have a bounded budget, and resumed work preserves existing attempt reservations. A valid citation reference is checked separately from whether the cited passage actually supports a claim; source-aware evaluation addresses that latter question.

## Observability and verification

![Local telemetry, quality commands, and evaluation targets](docs/images/content-writer-09-observability.png)

```bash
make observability-up   # OpenTelemetry, Prometheus, Grafana
make demo-epic-9        # Offline demo that exports metrics

make eval-offline        # Fixture-based evaluation, no API keys
make eval                # Live source-aware evaluation
```

[Grafana dashboard](http://127.0.0.1:3001/d/research-runs) · [LangSmith](https://smith.langchain.com) · [Evaluation runbook](docs/SPECS-LOGS/EVIDENCE-DRIVEN-AUTHORING-RUNBOOK.md)

Verification on October 9, 2026 passed **794 offline tests with 88.27% coverage**, plus lint, formatting, strict typing, the agent boundary check, and the package build. Three live pytest tests were deselected; separate live CLI/API execution is recorded in [the example index](runs.example/README.md).

## Configuration and limits

![Environment variables, known limitations, and documentation links](docs/images/content-writer-10-reference.png)

Configuration loads from `.env`, overridden by environment variables. The system supports Mermaid flowcharts and sequence diagrams when the renderer is installed. The [live example index](runs.example/README.md) records execution outcomes and temporary runtime overrides. These samples do not replace a formal evaluation of editorial quality.

For development and operations, see the [engineering standard](docs/ENGINEERING.md), [architecture decisions](docs/adr/), [authoring runbook](docs/SPECS-LOGS/EVIDENCE-DRIVEN-AUTHORING-RUNBOOK.md), and [API migration runbook](docs/SPECS-LOGS/FASTAPI-MIGRATION-RUNBOOK.md).

The [published walkthrough](https://josoroma.github.io/Deep-Research-Content-Writer/) is served by GitHub Pages from the root of `main`. `index.html` opens the run guide, and `.nojekyll` preserves the static files. The [root homepage](https://josoroma.github.io/) opens the same guide through the separate [`josoroma.github.io` repository](https://github.com/josoroma/josoroma.github.io).
