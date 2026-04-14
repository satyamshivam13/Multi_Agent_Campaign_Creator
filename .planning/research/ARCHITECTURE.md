# Architecture Patterns

**Domain:** Multi-agent campaign generation (Python CLI, CrewAI)
**Researched:** 2026-04-14
**Overall recommendation confidence:** MEDIUM-HIGH

## Recommended Architecture (2026, incremental)

Adopt a **Flow-first orchestrator with typed state and durable run records**, while keeping the existing sequential crew as the execution core.

Target shape:

1. `CampaignRunFlow` (new): orchestration shell
2. `CampaignCrew` (existing): specialized multi-agent unit-of-work
3. `RunStore` (new): durable run state and artifacts metadata
4. `ArtifactStore` (existing files + manifest): markdown/json outputs and provenance
5. `Telemetry` (new): span-level tracing for each stage and retry

This preserves current behavior and adds reliability and replayability in layers.

## Component Boundaries

| Component | Responsibility | Communicates With |
|-----------|----------------|-------------------|
| CLI Adapter (`src/main.py`) | Collect request, start run, present status | Flow Orchestrator |
| Flow Orchestrator (`CampaignRunFlow`) | Start/listen/route lifecycle, retries, resume points, state transitions | CampaignCrew, RunStore, ArtifactStore, Telemetry |
| Crew Unit (`src/workflow/crew_workflow.py`) | Executes research -> copy -> art -> manager sequence | Tools, LLM provider, Flow Orchestrator |
| State Schema (`pydantic` models) | Typed run state and contracts between flow steps | Flow Orchestrator, RunStore |
| RunStore (SQLite first) | Persist run id, status, checkpoints, errors, attempt counts | Flow Orchestrator, CLI status commands |
| ArtifactStore (filesystem + manifest) | Persist md/json artifacts and checksums per run | Flow Orchestrator, RunStore |
| Telemetry (OpenTelemetry) | Trace run/task retries, latency, failure classes | Flow Orchestrator, Crew Unit |

## Data Flow

1. CLI validates `CampaignRequest`.
2. Orchestrator creates `run_id`, writes `RUNNING` state to RunStore.
3. Orchestrator invokes existing `CampaignCrew` as a unit-of-work.
4. Crew returns structured output (`raw`, plus typed brief projection).
5. Orchestrator writes artifacts atomically:
   - markdown brief
   - json brief
   - manifest (run_id, timestamps, model, retry stats, checksums, source file paths)
6. Orchestrator transitions run state to `SUCCEEDED` (or `FAILED` with error metadata).
7. CLI prints deterministic run summary and locations.

Retry path:
- Provider-throttle retries remain in Crew logic.
- Orchestrator adds outer retry/circuit behavior for infra/transient failures and records each attempt in RunStore.

## Patterns To Follow

### Pattern 1: Flow-First Orchestration Around Existing Crew
**What:** Wrap current sequential crew in a CrewAI Flow for explicit control, typed state, routing, and persistence hooks.
**When:** Immediately; minimal behavior change required.
**Why now:** CrewAI production guidance favors Flow-first for robustness and observability.

### Pattern 2: Typed State Contract (Pydantic, stricter boundaries)
**What:** Use a dedicated run state model (request, stage, retry metadata, artifact references, error envelope).
**When:** Introduce with Flow migration.
**Why now:** Reduces string parsing fragility and supports deterministic resume and audit.

### Pattern 3: Durable Run Ledger + Artifact Manifest
**What:** Keep files as primary artifacts, but add a durable run ledger and manifest pointer model.
**When:** Same phase as Flow migration or immediately after.
**Why now:** Brownfield-safe; no need to replace file outputs while enabling history/search/replay.

Suggested SQLite schema (minimal):
- `runs(run_id, created_at, status, request_json, started_at, finished_at, error_code, error_message)`
- `run_attempts(id, run_id, stage, attempt_no, started_at, ended_at, outcome, error_type)`
- `artifacts(id, run_id, kind, path, sha256, bytes, created_at)`

### Pattern 4: Idempotent Persistence Boundary
**What:** Write artifacts to temp paths, fsync, then atomic rename; only then mark run `SUCCEEDED`.
**When:** Same phase as RunStore.
**Why now:** Prevents partial-success states and corrupted provenance.

### Pattern 5: End-to-End Tracing with Stable IDs
**What:** Emit a root span per `run_id`, child spans per stage/task/retry/provider call.
**When:** After RunStore baseline (or in parallel if low effort).
**Why now:** Fastest path to diagnosing throttling, latency regressions, and failure hot spots.

### Pattern 6: Optional Scale-Up Path via Durable Workflow Engine
**What:** Keep a future seam to move orchestration to Temporal if workload evolves to long-running, high-concurrency, distributed execution.
**When:** Defer; add interface boundary now so migration is low risk later.
**Why now:** Avoid premature platform shift while preserving future durability options.

## Anti-Patterns To Avoid

### Anti-Pattern 1: Monolithic `kickoff()` as only source of truth
**What goes wrong:** One opaque execution call with no durable per-stage state.
**Instead:** Flow state + run ledger checkpoints.

### Anti-Pattern 2: File-only persistence without run index
**What goes wrong:** No reliable history, replay cursor, or status reporting.
**Instead:** RunStore tables plus artifact manifest.

### Anti-Pattern 3: Untyped inter-stage payloads
**What goes wrong:** Silent schema drift and brittle parsing.
**Instead:** Pydantic models for state and output envelopes.

### Anti-Pattern 4: Observability by console logs only
**What goes wrong:** Hard to diagnose retries/throttling across runs.
**Instead:** OpenTelemetry traces correlated by `run_id`.

## Build-Order Implications (Implementation Phases)

1. **Phase A: Introduce Run IDs and RunStore (no orchestration rewrite)**
   - Add `run_id` creation at CLI start.
   - Persist `RUNNING/SUCCEEDED/FAILED` and artifact paths.
   - Keep existing `CampaignCrew.run()` unchanged.
   - Outcome: immediate persistence robustness and run history.

2. **Phase B: Wrap Existing Crew in Flow (behavior-preserving)**
   - Create `CampaignRunFlow` with typed state and single execution lane mirroring current sequence.
   - Move top-level retries/status transitions into Flow layer.
   - Outcome: explicit orchestration graph and cleaner control boundaries.

3. **Phase C: Add Artifact Manifest + Idempotent Writes**
   - Atomic write pattern and checksums.
   - Manifest file per run linked to RunStore.
   - Outcome: consistent output persistence under crashes/retries.

4. **Phase D: Add Telemetry and SLO Signals**
   - OTel spans for run, stages, retries, provider latency.
   - Basic dashboards/alerts around failure rate and p95 duration.
   - Outcome: operational visibility and faster incident triage.

5. **Phase E: Controlled Parallelism and Human Gates (optional)**
   - Use Flow routing/listen primitives for safe branching where dependencies allow.
   - Add optional human approval gates before final manager synthesis if needed.
   - Outcome: quality and throughput improvements without full rewrite.

6. **Phase F: Evaluate Temporal only if triggers are met**
   - Triggers: multi-worker distribution, long-lived waits, strict exactly-once orchestration requirements.
   - Outcome: avoids premature complexity while preserving migration seam.

## Scalability Considerations

| Concern | At current CLI scale | At team scale (10K runs/month) | At platform scale |
|---------|----------------------|----------------------------------|-------------------|
| Orchestration durability | Flow + persist + SQLite | Flow + Postgres RunStore | Temporal or equivalent durable engine |
| Output persistence | Files + manifest | Object storage + DB metadata index | Multi-region object store + indexed metadata |
| Failure handling | Crew retry + outer flow retry | Policy-based retries/circuit logic | Workflow-level compensation and dead-letter queues |
| Observability | Console + basic traces | OTel collector + dashboards | Centralized tracing + SLO/error budgets |

## Confidence Notes

- **HIGH:** Flow-first + typed state + persist are aligned with CrewAI 2026 documentation.
- **HIGH:** Run ledger + manifest approach is incremental and compatible with current file outputs.
- **MEDIUM:** Temporal as future path is strong for durable workflows, but should be trigger-driven for this project size.
- **HIGH:** OTel tracing recommendation is mature and stable for Python.

## Sources

- CrewAI Flows: https://docs.crewai.com/en/concepts/flows
- CrewAI Production Architecture: https://docs.crewai.com/en/concepts/production-architecture
- CrewAI Crews (attributes, output, async, logs): https://docs.crewai.com/en/concepts/crews
- Temporal Workflows (durable execution model): https://docs.temporal.io/workflows
- OpenTelemetry Python docs (status, install, ecosystem): https://opentelemetry.io/docs/languages/python/
- Python sqlite3 transaction guidance: https://docs.python.org/3/library/sqlite3.html
- SQLite WAL behavior and caveats: https://sqlite.org/wal.html
- PostgreSQL JSON/JSONB guidance (for future RunStore scale-up): https://www.postgresql.org/docs/current/datatype-json.html
