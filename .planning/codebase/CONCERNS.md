# Codebase Concerns

**Analysis Date:** 2026-04-14

## Tech Debt

**Parallel model layers (legacy-style agents + CrewAI agents):**
- Issue: Two agent abstractions are maintained (`BaseAgent` subclasses with `execute()` stubs and CrewAI `Agent` factory functions), creating duplicate behavior contracts and drift risk.
- Files: `src/agents/base_agent.py`, `src/agents/research_agent.py`, `src/agents/copywriter_agent.py`, `src/agents/art_director_agent.py`, `src/agents/manager_agent.py`, `tests/test_agents.py`, `tests/conftest.py`
- Impact: Tests can pass against lightweight stub classes while production runs CrewAI agent objects, masking production regressions.
- Fix approach: Converge on one public agent interface. Either remove stub classes and update tests to validate factory-created CrewAI agents, or fully route runtime through tested wrapper classes.

**Documentation drift around implemented retry behavior:**
- Issue: Contribution guidance still lists rate-limit retry logic as an enhancement even though retry/backoff is implemented in workflow.
- Files: `CONTRIBUTING.md`, `src/workflow/crew_workflow.py`
- Impact: Misleads contributors and can lead to duplicate or conflicting work.
- Fix approach: Update contribution roadmap to current state and replace completed items with next-gap items.

## Known Bugs

**Time-bounded trend query hard-coded to 2025:**
- Symptoms: Live trend research uses a static year in search query, causing stale query framing as calendar time advances.
- Files: `src/tools/trend_research_tool.py`
- Trigger: Any call to `TrendResearchTool._live_search()`.
- Workaround: Replace fixed year with current year (or remove year constraint) and optionally allow configurable recency windows.

## Security Considerations

**Broad exception handling with full traceback printing in CLI path:**
- Risk: Runtime errors dump full traceback directly to terminal, which can expose stack internals and third-party error payload details in shared logs/screenshots.
- Files: `src/main.py`, `src/workflow/crew_workflow.py`
- Current mitigation: User-friendly error panel is shown before traceback output.
- Recommendations: Gate traceback behind a debug flag, default to sanitized error messages, and avoid printing raw provider exceptions in normal mode.

**Environment loading from local file without runtime secret-source abstraction:**
- Risk: Secrets are expected in `.env` for local runs, which is fine for dev but fragile for production hardening and rotation workflows.
- Files: `src/config.py`, `.env.example`, `README.md`
- Current mitigation: Required-key validation for `GROQ_API_KEY` at startup.
- Recommendations: Add support for external secret providers (CI/CD secret store, cloud secret manager) and document secure deployment path.

## Performance Bottlenecks

**Single-threaded, sequential multi-agent pipeline with verbose output:**
- Problem: Workflow executes all four agents serially (`Process.sequential`) and each agent allows multiple iterations, increasing wall-clock latency.
- Files: `src/workflow/crew_workflow.py`, `src/agents/research_agent.py`, `src/agents/copywriter_agent.py`, `src/agents/art_director_agent.py`, `src/agents/manager_agent.py`
- Cause: No concurrency strategy for independent sub-steps, no execution budgeting, and high verbosity in runtime path.
- Improvement path: Add optional parallelizable phases where dependencies allow, cap iteration budgets by request size, and disable verbose mode by default in non-debug runs.

**No caching or deduplication for external trend lookups:**
- Problem: Repeated similar live trend queries can re-hit network/API each run.
- Files: `src/tools/trend_research_tool.py`
- Cause: Stateless tool execution and no memoization/persistence layer.
- Improvement path: Add short-lived cache keyed by normalized query+industry and optional persisted cache for repeat campaign exploration.

## Fragile Areas

**Workflow retry classification relies on string matching:**
- Files: `src/workflow/crew_workflow.py`
- Why fragile: Rate-limit detection checks message substrings (`"rate limit"`, `"429"`, etc.), which is brittle across SDK/provider message changes and localization.
- Safe modification: Prefer typed exception/status-code checks from provider/client libraries first, keep string parsing as fallback only.
- Test coverage: Retry success and exhaustion branches are tested, but message-format variants are not broadly covered (`tests/test_workflow.py`).

**Test monkeypatching against dynamic crew class internals:**
- Files: `tests/test_workflow.py`
- Why fragile: Tests patch `type(crew.crew).kickoff`, coupling tests to CrewAI object internals and making upgrades brittle.
- Safe modification: Introduce a thin kickoff adapter method in `CampaignCrew` and patch that boundary instead.
- Test coverage: Existing tests validate happy-path retry behavior but not structural compatibility across CrewAI versions.

## Scaling Limits

**CLI-only execution model with no job queue or persistence:**
- Current capacity: One foreground campaign run per process invocation.
- Limit: Throughput and observability degrade when running multiple campaigns; no task queue, state store, or resumability.
- Scaling path: Add a service layer with queued jobs, persisted run metadata, and asynchronous worker execution.

## Dependencies at Risk

**Loosely bounded dependency versions in runtime-critical libraries:**
- Risk: `>=` constraints (no upper bounds) can pull in breaking behavior from rapidly evolving orchestration/LLM stacks.
- Impact: Runtime failures or subtle behavior shifts in agent orchestration, model client integration, or task execution.
- Migration plan: Pin tested ranges in `pyproject.toml`, add periodic dependency update workflow with compatibility smoke tests.

## Missing Critical Features

**No structured persistence for campaign history and auditability:**
- Problem: Outputs are written as files only; no indexed history, status tracking, or searchable metadata.
- Blocks: Reliable reporting, multi-run comparisons, and production-style observability.

**No provider failover strategy:**
- Problem: Runtime assumes single LLM provider path.
- Blocks: High-availability operation during provider outage, quota exhaustion, or model-level incidents.

## Test Coverage Gaps

**Configuration validation paths are untested:**
- What's not tested: `Settings.__post_init__` failure branches for invalid or missing environment values.
- Files: `src/config.py`, `tests/`
- Risk: Startup behavior can regress unnoticed when env parsing or defaults change.
- Priority: High

**CLI interaction and error-mode behavior are untested:**
- What's not tested: `argparse` branches (`--demo` vs interactive), prompt parsing, and sanitized failure output behavior.
- Files: `src/main.py`, `tests/`
- Risk: User-facing run path can break without test signal.
- Priority: High

**Live network path for trend research is untested:**
- What's not tested: `TrendResearchTool._live_search()` success/failure handling with real/ mocked `httpx.post` responses.
- Files: `src/tools/trend_research_tool.py`, `tests/test_tools.py`
- Risk: External integration failures surface only in runtime.
- Priority: Medium

---

*Concerns audit: 2026-04-14*
