# Domain Pitfalls

**Domain:** Multi-agent campaign generation CLI (CrewAI + Groq)
**Researched:** 2026-04-14

## Critical Pitfalls

### Pitfall 1: Brittle rate-limit detection by string matching
**What goes wrong:** Retry logic misses real throttling errors (or retries on non-throttling errors) because detection depends on message substrings.
**Why it happens:** Error classification is tied to provider wording and status text instead of typed/status-code signals.
**Early warning signs:**
- Spikes in first-attempt failures after SDK/provider updates.
- Same incident alternates between "retried" and "hard failed" behavior.
- Logs show unfamiliar throttle message formats not matching markers.
**Consequences:** Reliability regressions, noisy incidents, and fragile behavior across provider/client upgrades.
**Prevention:** Introduce structured error classification (status code + provider exception classes), keep string markers only as fallback, and add table-driven tests for message variants.
**Likely phase(s):** Reliability hardening phase.

### Pitfall 2: Test/runtime drift from dual agent abstractions
**What goes wrong:** Tests stay green while production behavior breaks because test stubs and CrewAI runtime paths diverge.
**Why it happens:** Lightweight BaseAgent-style classes and CrewAI factories represent two behavior contracts.
**Early warning signs:**
- Production-only failures not reproducible in unit tests.
- Frequent monkeypatching of Crew internals to keep tests passing.
- Refactors in agent creation break runtime but not tests.
**Consequences:** False confidence, slower incident triage, and regression leaks.
**Prevention:** Converge to one agent interface boundary, test the actual CrewAI-built agents, and patch a local adapter method (not dynamic Crew internals).
**Likely phase(s):** Reliability hardening + test modernization phase.

### Pitfall 3: Silent quality downgrade when live trend search fails
**What goes wrong:** Campaigns look plausible but are based on simulated/fallback trend data after external search failure.
**Why it happens:** Live-search failure path quietly falls back and continues generation.
**Early warning signs:**
- Output repeatedly contains generic trends across unrelated products.
- Rising count of "falling back to analysis" messages.
- Users report stale/boilerplate market insight quality.
**Consequences:** Lower output trust, hidden data freshness issues, and weak production credibility.
**Prevention:** Add quality gates that label fallback-sourced sections, emit run-level quality flags, and optionally fail-fast for production mode when live data is required.
**Likely phase(s):** Output quality expansion + production readiness phase.

### Pitfall 4: Incomplete structured brief while claiming production readiness
**What goes wrong:** JSON/brief fields like budget, timeline, and KPI detail remain null or shallow despite roadmap promises.
**Why it happens:** Raw LLM output is wrapped into placeholders instead of reliably extracted/validated structured sections.
**Early warning signs:**
- Frequent null/default values in persisted JSON artifacts.
- Manual post-processing required before handoff.
- KPI/timeline detail varies wildly run to run.
**Consequences:** Unreliable downstream use, brittle integrations, and diminished perceived quality.
**Prevention:** Define strict acceptance schema for expanded sections, add extraction + validation + repair loops, and fail output checks when required fields are missing.
**Likely phase(s):** Output quality expansion phase.

### Pitfall 5: Verbose exception disclosure in normal CLI runs
**What goes wrong:** Full tracebacks and raw provider errors are shown by default, exposing internals in shared terminal logs/screenshots.
**Why it happens:** Error paths print traceback unconditionally in user-facing flow.
**Early warning signs:**
- Incident screenshots include stack traces and provider payload fragments.
- Support requests copy sensitive internals from console output.
- Team hesitates to share logs externally.
**Consequences:** Security/compliance risk and poor production UX.
**Prevention:** Default to sanitized user messages, gate full traceback behind debug mode, and standardize error codes for support workflows.
**Likely phase(s):** Production readiness and security hardening phase.

## Moderate Pitfalls

### Pitfall 6: Dependency drift from open-ended version constraints
**What goes wrong:** New upstream releases subtly alter CrewAI/provider behavior and break retries, task wiring, or response parsing.
**Early warning signs:**
- Failures appear immediately after fresh environment setup.
- CI instability without local code changes.
- Different behavior across developer machines.
**Prevention:** Pin tested version ranges, introduce scheduled upgrade windows, and run compatibility smoke tests before bumping.
**Likely phase(s):** Production readiness phase.

### Pitfall 7: Non-atomic output writes and weak run metadata
**What goes wrong:** Partial artifacts or hard-to-trace outputs appear when runs fail mid-write or runs are compared later.
**Early warning signs:**
- Missing JSON/Markdown pair for some runs.
- Duplicate/ambiguous output files for repeated campaigns.
- Hard to answer "which config produced this artifact?"
**Prevention:** Use atomic write pattern (temp + rename), add run IDs and config snapshot metadata, and persist run status lifecycle.
**Likely phase(s):** Production readiness + observability phase.

### Pitfall 8: Retry policy that amplifies quota pressure
**What goes wrong:** Multiple retries with high token budgets increase load during provider stress, extending outage impact.
**Early warning signs:**
- Retry storms during 429 windows.
- Growing completion latency under burst traffic.
- Token usage spikes with little increase in success rate.
**Prevention:** Add jitter/circuit-breaker behavior, cap total attempt budget by request size, and reduce model/token profile on retries.
**Likely phase(s):** Reliability hardening + cost-control phase.

## Minor Pitfalls

### Pitfall 9: Calendar-stale trend query framing
**What goes wrong:** Live trend query includes a fixed year, degrading freshness as time advances.
**Early warning signs:**
- Search results skew to older yearly roundups.
- New-year relevance dip in research sections.
**Prevention:** Use current year dynamically or recency filters configurable by run mode.
**Likely phase(s):** Output quality polish phase.

### Pitfall 10: CLI path under-tested relative to user impact
**What goes wrong:** Interactive argument/input paths regress without early detection.
**Early warning signs:**
- `--demo` works but interactive mode fails unexpectedly.
- Parsing/validation bugs appear after minor CLI changes.
**Prevention:** Add CLI contract tests for interactive/demo/error modes and snapshot key user-facing panels/messages.
**Likely phase(s):** Production readiness phase.

## Phase-Specific Warnings

| Phase Topic | Likely Pitfall | Mitigation |
|-------------|---------------|------------|
| Reliability hardening | Brittle throttle detection and retry storms | Typed error classification, jitter/circuit breaker, retry-budget tests |
| Output quality expansion | Simulated-data contamination + null structured fields | Provenance flags, strict schema validation, fail-on-missing required sections |
| Production readiness | Verbose tracebacks, dependency drift, non-atomic artifacts | Sanitized errors, pinned deps with upgrade cadence, atomic writes + run metadata |
| Testing modernization | Runtime/test divergence and fragile monkeypatching | Unify agent interface and test at stable local adapter boundaries |

## Sources

- Repository inspection: `src/workflow/crew_workflow.py`, `src/tools/trend_research_tool.py`, `src/main.py`, `src/config.py`, `tests/test_workflow.py`, `.planning/codebase/CONCERNS.md`
- Confidence: HIGH for identified pitfalls (direct codebase evidence)
