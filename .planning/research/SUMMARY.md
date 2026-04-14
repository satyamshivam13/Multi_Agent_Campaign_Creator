# Project Research Summary

**Project:** Multi-Agent Campaign Creator
**Domain:** Multi-agent AI campaign generation (Python CLI)
**Researched:** 2026-04-14
**Confidence:** MEDIUM-HIGH

## Executive Summary

This project is a CrewAI-based, CLI-first campaign generator that already has a workable sequential pipeline but lacks production-grade reliability controls. The strongest near-term strategy is incremental hardening, not a platform rewrite: keep the existing crew execution path, add deterministic run identity/state, and enforce typed contracts plus strict output validation. Experts build systems like this by separating orchestration concerns (state, retries, persistence, telemetry) from content-generation concerns (agents, tools, prompts).

The recommended stack direction is conservative and reliability-oriented: Python 3.12 baseline (3.11 compatible), pinned CrewAI and Pydantic versions, uv lock/sync workflows, tenacity-based retry policy, pydantic-settings for config validation, and OpenTelemetry for end-to-end traces. This aligns with the current repository shape (`src/main.py`, `src/workflow/crew_workflow.py`, `src/config.py`) and avoids overexpanding scope into GUI work, multi-provider complexity, or heavyweight workflow engines too early.

Primary risk is hidden quality and reliability drift: brittle string-matched rate-limit logic, quiet fallback to simulated trend data, and incomplete structured outputs that appear successful. Mitigation is to enforce explicit failure semantics (typed error classes, retry budgets, fail-on-missing schema fields), add run metadata and artifact manifests, and gate production outputs with scorecards and provenance flags.

## Key Findings

### Recommended Stack

The stack should optimize for reproducibility, controlled upgrades, and diagnosability. Keep CrewAI as core orchestration runtime but wrap with stronger state and persistence boundaries. Use lockfile-driven environments and policy-based retries to reduce nondeterministic failures.

**Core technologies:**
- Python 3.12 (3.11 compatible): runtime baseline - stable ecosystem and low migration risk.
- CrewAI 1.14.x pinned: multi-agent orchestration - preserves current architecture while reducing upgrade regressions.
- Pydantic v2 + pydantic-settings: typed schemas/config - deterministic contracts and safer env parsing.
- uv + committed lockfile: dependency management - reproducible installs in dev/CI.
- tenacity + httpx client policy: retry/backoff and network control - robust transient-failure handling.
- OpenTelemetry + structured logs: observability - run/stage/retry diagnostics and SLO tracking.
- Ruff + mypy + pre-commit + pytest stack: quality gates - faster feedback and reduced drift.

### Expected Features

Near-term feature work should cluster around reliability + quality gates, not UI breadth.

**Must have (table stakes):**
- Deterministic run metadata (run_id, config snapshot, timestamps, model details).
- Guardrailed schema validation before final save.
- Task-level retry with bounded backoff and transient vs hard-failure classification.
- Channel-aware copy constraints and consistent brand voice controls.
- Basic human review gates with non-interactive automation mode.
- Reproducible rerun mode (seed/input hash/config lock).

**Should have (competitive):**
- Two-pass manager QA (draft, critique, revision).
- Campaign quality scorecard with explicit failure reasons.
- KPI realism checker linked to budget/objective/channel constraints.
- Resumable stage execution after partial failure.
- Variant generation with winner recommendation.
- Evidence ledger mapping claims to tool outputs.

**Defer (v2+):**
- Full GUI/dashboard buildout.
- Multi-provider routing expansion.
- One-click publish integrations.
- Heavy external workflow platform migration unless scale triggers are met.

### Architecture Approach

Use a Flow-first wrapper around the current crew implementation: introduce `CampaignRunFlow` for lifecycle and retry control, `RunStore` for durable run state (SQLite-first), artifact manifests for traceable outputs, and telemetry spans keyed by `run_id`. Keep `CampaignCrew` as the execution engine initially to avoid risky rewrites. This architecture preserves current behavior while adding checkpointability, replayability, and operational visibility.

**Major components:**
1. CLI adapter (`src/main.py`) - request intake, run start, user-facing status.
2. Flow orchestrator (`CampaignRunFlow`) - state transitions, retries, resume logic.
3. Crew execution unit (`src/workflow/crew_workflow.py`) - research/copy/art/manager stage execution.
4. Typed state contracts (Pydantic models) - strict inter-stage payload guarantees.
5. RunStore (SQLite first) - status, attempts, errors, artifact references.
6. ArtifactStore (filesystem + manifest) - atomic output persistence and provenance.
7. Telemetry (OpenTelemetry) - correlated traces, latency, and retry diagnostics.

### Critical Pitfalls

1. **Brittle rate-limit detection** - replace message matching with typed/status-based classification and table-driven tests.
2. **Runtime/test abstraction drift** - converge to one agent boundary and test real CrewAI-built execution paths.
3. **Silent fallback quality degradation** - label or block fallback-sourced insight sections in strict production mode.
4. **Incomplete structured brief fields** - enforce strict acceptance schema and fail outputs with missing required fields.
5. **Verbose exception leakage in CLI** - default to sanitized error surfaces; keep full traces in debug mode only.

## Implications for Roadmap

Based on combined research, suggested phase structure:

### Phase 1: Reliability Foundation and Deterministic Runs
**Rationale:** This is the dependency base for all later quality and scale work.
**Delivers:** run_id lifecycle, RunStore baseline, config snapshots, pinned deps/lockfile, sanitized error codes.
**Addresses:** run metadata, reproducible reruns, basic reliability table stakes.
**Avoids:** dependency drift, non-atomic run ambiguity, verbose error leakage.

### Phase 2: Orchestration Hardening with Typed Retry and Persistence
**Rationale:** Add robust control boundaries before expanding feature complexity.
**Delivers:** Flow wrapper around current crew, typed state contracts, tenacity retry policies, artifact manifest with atomic writes.
**Uses:** CrewAI + Pydantic + tenacity + httpx policy.
**Implements:** orchestrator/run-store/artifact-store boundaries.
**Avoids:** brittle string retries, partial artifact corruption, opaque kickoff-only execution.

### Phase 3: Output Quality Guardrails
**Rationale:** Once runs are stable, enforce quality deterministically.
**Delivers:** strict schema validation/repair loop, channel/brand rule gates, KPI realism checker, campaign scorecard.
**Addresses:** must-have quality controls and measurable acceptance criteria.
**Avoids:** null/shallow structured briefs and low-trust outputs.

### Phase 4: Differentiator Layer and Controlled Throughput
**Rationale:** Add competitive value after baseline reliability and quality are proven.
**Delivers:** two-pass manager QA, resumable stages, variant ranking, evidence ledger, reliability profiles (fast/balanced/strict).
**Addresses:** core differentiator cluster from features research.
**Avoids:** premature multi-provider/GUI complexity.

### Phase 5: Observability and Scale Triggers
**Rationale:** Operationalize before considering platform migration.
**Delivers:** OTel traces, SLO dashboards, failure taxonomy, trigger-based evaluation for Postgres/Temporal migration.
**Addresses:** long-term maintainability and team-scale operations.
**Avoids:** premature architecture jumps without measured need.

### Phase Ordering Rationale

- Run determinism and persistence must precede resume, scoring, and quality analytics.
- Flow/state hardening should wrap existing crew behavior before adding new generation branches.
- Quality gates require stable schemas/metadata and repeatable runs to be meaningful.
- Differentiators are safest after failure handling and provenance are trustworthy.
- Scale-platform migration should be gated by observed workload triggers, not roadmap speculation.

### Research Flags

Phases likely needing deeper research during planning:
- **Phase 4:** evidence-ledger schema design and citation UX semantics.
- **Phase 5:** concrete SLO targets and backend migration trigger thresholds.

Phases with standard patterns (skip deep research-phase):
- **Phase 1:** lockfile/pinning, sanitized error handling, run metadata patterns are mature.
- **Phase 2:** Flow wrapper + typed retry + atomic writes have established implementation patterns.
- **Phase 3:** schema validation and deterministic quality-rule enforcement are well documented.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Strong official-doc backing (CrewAI, uv, Ruff, mypy, OTel, tenacity). |
| Features | MEDIUM | Table-stakes mapping is solid; broad market prevalence data is less rigorous. |
| Architecture | HIGH | Incremental Flow + RunStore pattern maps directly to current repo structure. |
| Pitfalls | HIGH | Risks are directly evidenced in current implementation paths. |

**Overall confidence:** MEDIUM-HIGH

### Gaps to Address

- Provider-specific exception taxonomy still needs empirical validation against actual Groq/client error payloads in this repo.
- Scorecard thresholds and KPI realism limits need calibration from real campaign run samples.
- SQLite-to-Postgres/Temporal trigger values should be formalized after initial telemetry baseline is collected.

## Sources

### Primary (HIGH confidence)
- `.planning/research/STACK.md`
- `.planning/research/FEATURES.md`
- `.planning/research/ARCHITECTURE.md`
- `.planning/research/PITFALLS.md`
- CrewAI docs/changelog: https://docs.crewai.com/
- OpenTelemetry Python docs: https://opentelemetry.io/docs/languages/python/
- uv docs: https://docs.astral.sh/uv/

### Secondary (MEDIUM confidence)
- httpx advanced transport guidance: https://www.python-httpx.org/advanced/transports/
- Tenacity docs: https://tenacity.readthedocs.io/en/latest/
- pydantic-settings package docs: https://pypi.org/project/pydantic-settings/

### Tertiary (LOW confidence)
- Market expectation signal pages referenced in FEATURES research (anti-bot constrained retrieval in places).

---
*Research completed: 2026-04-14*
*Ready for roadmap: yes*
