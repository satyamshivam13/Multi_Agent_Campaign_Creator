# Project Roadmap: Multi-Agent Campaign Creator

**Version:** v1
**Created:** 2026-04-14
**Milestone:** 1.0
**Granularity:** coarse (4 phases)

---

## Project Focus

**Core Value:** Generate a coherent, usable campaign brief from one product input in minutes, not days.

**Scope:** Python CLI delivering CrewAI-orchestrated campaign generation with production-grade reliability, structured output quality, and safe user-facing operations.

---

## Phases

- [ ] **Phase 1: Run Reliability & Determinism** - Establish run identity, reproducibility, and basic persistence foundation
- [ ] **Phase 2: Orchestration & State Management** - Robust multi-stage workflow execution with resume and validation
- [ ] **Phase 3: Output Quality Assurance** - Structured output enforcement and measurable quality gates
- [ ] **Phase 4: CLI Production Readiness** - Safe error handling, user-configurable profiles, comprehensive test coverage

---

## Phase Details

### Phase 1: Run Reliability & Determinism

**Goal:** Every campaign run has deterministic identity, reproducible state, and captured execution context (retry attempts, failures, provider details) so users can rerun failed campaigns and operators can diagnose issues.

**Depends on:** Nothing (foundation phase)

**Requirements Mapped:** RELY-01, RELY-02, RELY-03, RELY-04, DATA-01, DATA-03

**Success Criteria (what must be TRUE):**
1. Every campaign run is assigned a unique `run_id` with UTC start/end timestamps that persist across restarts
2. User can rerun a failed campaign by replaying the same request and config snapshot
3. System records all retry attempts per stage with timestamps and terminal failure reason
4. Run metadata (start time, end time, provider/model, retry attempt count) is accessible and auditable

**Plans:** TBD

---

### Phase 2: Orchestration & State Management

**Goal:** Campaign workflow executes stages in deterministic order, validates outputs before downstream use, can resume from last successful stage after interruption, and accurately reports partial vs full success.

**Depends on:** Phase 1

**Requirements Mapped:** ORCH-01, ORCH-02, ORCH-03, ORCH-04, DATA-02

**Success Criteria (what must be TRUE):**
1. Workflow executes research → copy → art → strategy stages in explicit order with visible stage status (`pending`, `running`, `failed`, `completed`)
2. User can resume a run from the last successful stage after an unexpected interruption
3. Each stage output is validated against its schema before becoming context for the next stage; validation failures block progression
4. Workflow completion status accurately distinguishes partial failure (some stages done, some failed) from full success

**Plans:** TBD

---

### Phase 3: Output Quality Assurance

**Goal:** Final campaign output enforces structured sections, schema completeness, channel awareness, brand consistency, and explicit KPI definitions so users receive reliably usable briefs.

**Depends on:** Phase 1, Phase 2

**Requirements Mapped:** QUAL-01, QUAL-02, QUAL-03, QUAL-04, QUAL-05

**Success Criteria (what must be TRUE):**
1. Final output includes distinct structured sections for market research insights, copy package (headlines/body), visual direction (mood, style, constraints), and executive strategy
2. Campaign output fails reproducibly if any required schema field is missing; user sees which fields failed
3. Copy is generated only for channels explicitly selected in the campaign request; unused channels are omitted
4. Brand voice and tone constraints are applied consistently across all copy sections (headlines, body, CTAs); user can verify voice adherence
5. Campaign output explicitly defines KPIs (metrics, success targets) aligned with stated campaign goals

**Plans:** TBD

---

### Phase 4: CLI Production Readiness

**Goal:** CLI is production-safe with user-friendly errors, observable retries, profile-based configurability, early validation, and comprehensive test coverage validating reliability, config parsing, and output contracts.

**Depends on:** Phase 1, Phase 2, Phase 3

**Requirements Mapped:** CLI-01, CLI-02, CLI-03, TEST-01, TEST-02, TEST-03

**Success Criteria (what must be TRUE):**
1. CLI normal mode shows actionable, sanitized error messages to users; debug mode (`--debug`) shows full exception tracebacks
2. CLI exposes profile flags (`--profile fast|balanced|strict`) that users can see and control, affecting retry limits and token behavior
3. Configuration loading fails fast with specific, actionable error messages before any campaign run begins (e.g., "GROQ_API_KEY not set", "Config file uses deprecated field blah")
4. Automated test suite verifies transient retry success/exhaustion, config parsing for required and optional settings, and campaign output schema compliance

**Plans:** TBD

---

## Progress

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Run Reliability & Determinism | 0/? | Not started | - |
| 2. Orchestration & State Management | 0/? | Not started | - |
| 3. Output Quality Assurance | 0/? | Not started | - |
| 4. CLI Production Readiness | 0/? | Not started | - |

---

## Requirement Traceability

**Coverage:** 22 v1 requirements mapped to 4 phases

| Category | Total | Phase 1 | Phase 2 | Phase 3 | Phase 4 |
|----------|-------|---------|---------|---------|---------|
| Reliability | 4 | RELY-01, RELY-02, RELY-03, RELY-04 | — | — | — |
| Orchestration | 4 | — | ORCH-01, ORCH-02, ORCH-03, ORCH-04 | — | — |
| Output Quality | 5 | — | — | QUAL-01, QUAL-02, QUAL-03, QUAL-04, QUAL-05 | — |
| Persistence | 3 | DATA-01, DATA-03 | DATA-02 | — | — |
| CLI / DX | 3 | — | — | — | CLI-01, CLI-02, CLI-03 |
| Testing | 3 | — | — | — | TEST-01, TEST-02, TEST-03 |
| **TOTAL** | **22** | **6** | **5** | **5** | **6** |

---

## Roadmap Evolution

This roadmap captures v1 scope. At each phase transition:
1. Validate scope hasn't shifted (PROJECT.md still accurate?)
2. Update REQUIREMENTS.md traceability with phase completion status
3. Log any emerging requirements or constraints to the phase commit

V2 scope (deferred):
- **DIFF-01, DIFF-02, DIFF-03:** Manager QA critique cycle, variant generation, evidence ledger
- **OPS-01, OPS-02, OPS-03:** Telemetry/traces, provider fallback, persistent campaign history

---

*Roadmap created: 2026-04-14*
*Ready for phase planning: yes*
