# Phase 1: Run Reliability & Determinism - Context

**Gathered:** 2026-04-14
**Status:** Ready for planning

<domain>
## Phase Boundary

Establish deterministic run identity, reproducible reruns, and execution-context capture for each campaign run, including retry attempts and provider metadata. This phase does not redesign orchestration flow, output quality logic, or introduce new user features beyond reliability controls.

</domain>

<decisions>
## Implementation Decisions

### Run Identity Contract
- **D-01:** Generate `run_id` at campaign start using `UTC timestamp + short random suffix` and keep it immutable for the full run.
- **D-02:** Attach `run_id` to all persisted artifacts, runtime status updates, and retry/error events.

### Persistence Backbone
- **D-03:** Use SQLite as the source of truth for run metadata and status transitions in Phase 1.
- **D-04:** Keep markdown/json campaign outputs as filesystem artifacts, linked from SQLite records by artifact path and hash.

### Retry Policy
- **D-05:** Treat only typed transient classes as retryable (`rate_limit`, network timeout, temporary upstream unavailability); all others fail fast.
- **D-06:** Use bounded exponential backoff with provider hint override (`retry-after`/"try again in") and hard retry budget per stage.

### Rerun Experience
- **D-07:** Add rerun entrypoint via CLI flag `--rerun <run_id>` that reuses stored request and config snapshot.
- **D-08:** Rerun creates a new child `run_id` while preserving parent linkage for audit trail.

### Error Surface Policy
- **D-09:** Normal mode surfaces sanitized user-safe failures with stable error codes and suggested recovery action.
- **D-10:** Debug mode enables full traceback and provider payload details for diagnosis.

### the agent's Discretion
- Exact `run_id` delimiter and suffix length
- SQLite table/index names and migration strategy
- Internal retry utility organization (helper module vs workflow-local utility)

</decisions>

<specifics>
## Specific Ideas

No specific requirements beyond the locked defaults above; use standard Python CLI and workflow patterns already established in the repository.

</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase scope and success criteria
- `.planning/ROADMAP.md` - Phase 1 goal, mapped requirements, and success criteria
- `.planning/STATE.md` - Current project position and milestone context

### Requirement contracts
- `.planning/REQUIREMENTS.md` - `RELY-01..04` and `DATA-01`, `DATA-03` requirement definitions
- `.planning/PROJECT.md` - Core value, constraints, and active priorities

### Existing implementation anchors
- `src/workflow/crew_workflow.py` - Current run execution path and retry behavior
- `src/main.py` - CLI entrypoint and error presentation behavior
- `src/config.py` - environment/config model and validation conventions

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `CampaignCrew.run` in `src/workflow/crew_workflow.py` is the central place to attach run lifecycle state transitions.
- `settings` in `src/config.py` already centralizes retry/token env controls and can be extended for run-store settings.
- Existing workflow retry helpers (`_is_rate_limit_error`, `_compute_retry_delay`) provide a base to migrate to typed retry classes.

### Established Patterns
- Absolute imports via `src.*`, typed helper methods, and pydantic model usage should be preserved.
- Rich-based status messaging in CLI/workflow is the existing user feedback pattern.
- Tests in `tests/test_workflow.py` already mock retry behavior and can be extended for run identity/persistence checks.

### Integration Points
- Add run lifecycle initialization in `src/main.py`/`CampaignCrew` boundary.
- Add persistence layer module under `src/` (for example `src/runtime/run_store.py`) and invoke it from workflow.
- Extend output saving logic in `CampaignCrew._save_outputs` to register artifacts in run metadata.

</code_context>

<deferred>
## Deferred Ideas

- Multi-provider fallback routing (tracked for later phases)
- Full telemetry dashboards and distributed tracing instrumentation (v2 / later milestone)
- Web UI or history browser for run management (out of current phase scope)

</deferred>

---

*Phase: 01-run-reliability-determinism*
*Context gathered: 2026-04-14*
