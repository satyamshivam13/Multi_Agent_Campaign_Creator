# Requirements: Multi-Agent Campaign Creator

**Defined:** 2026-04-14
**Core Value:** Generate a coherent, usable campaign brief from one product input in minutes, not days.

## v1 Requirements

### Reliability

- [ ] **RELY-01**: System retries transient provider failures with bounded backoff and stops on non-transient errors.
- [ ] **RELY-02**: Every campaign run is assigned a unique `run_id` and includes start/end timestamps.
- [ ] **RELY-03**: System records retry attempts and terminal failure reason per stage.
- [ ] **RELY-04**: User can rerun a failed campaign using the same request/config snapshot.

### Orchestration

- [ ] **ORCH-01**: Workflow executes stages in deterministic order with explicit stage status (`pending`, `running`, `failed`, `completed`).
- [ ] **ORCH-02**: Workflow can resume from the last successful stage after an interruption.
- [ ] **ORCH-03**: Stage outputs are validated before they become downstream context.
- [ ] **ORCH-04**: Final workflow status reflects partial failure vs full success accurately.

### Output Quality

- [ ] **QUAL-01**: Final campaign output includes structured sections for research, copy package, visual direction, and executive strategy.
- [ ] **QUAL-02**: Final output enforces required schema fields and fails if minimum quality fields are missing.
- [ ] **QUAL-03**: Channel-specific copy is generated only for channels selected in the request.
- [ ] **QUAL-04**: Brand voice constraints are applied consistently across generated copy sections.
- [ ] **QUAL-05**: Campaign output includes explicit KPI definitions aligned with stated campaign goals.

### Persistence and Auditability

- [ ] **DATA-01**: System stores a run manifest linking request input, config snapshot, and produced artifacts.
- [ ] **DATA-02**: Markdown and JSON outputs are written atomically to prevent partial-file corruption.
- [ ] **DATA-03**: Saved output metadata includes provider/model details used for generation.

### CLI and Developer Experience

- [ ] **CLI-01**: CLI normal mode shows user-safe errors while debug mode can show full tracebacks.
- [ ] **CLI-02**: CLI exposes profile controls (`fast`, `balanced`, `strict`) for token and retry behavior.
- [ ] **CLI-03**: Configuration validation fails early with actionable messages for invalid environment values.

### Testing

- [ ] **TEST-01**: Workflow tests cover transient retry success and retry exhaustion for provider throttling.
- [ ] **TEST-02**: Tests validate config parsing and validation branches for required and optional settings.
- [ ] **TEST-03**: Tests verify output schema contract for successful campaign generation.

## v2 Requirements

### Differentiators

- **DIFF-01**: Manager performs a second-pass critique and revision cycle before final brief output.
- **DIFF-02**: System generates multiple campaign variants and recommends a winner with rationale.
- **DIFF-03**: Evidence ledger maps major claims to tool outputs and source provenance.

### Advanced Operations

- **OPS-01**: Structured telemetry exports traces/metrics/logs for run diagnostics.
- **OPS-02**: Provider fallback strategy supports at least one secondary LLM provider.
- **OPS-03**: Persistent campaign history supports searchable run comparisons.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Full web app dashboard | CLI-first scope prioritized for faster delivery and lower complexity |
| Native mobile app | Not needed for initial product value and user workflow |
| Enterprise multi-tenant RBAC and billing | Premature for current single-team use case |
| One-click external publishing integrations | Defer until core reliability and quality are stable |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| RELY-01 | Phase TBD | Pending |
| RELY-02 | Phase TBD | Pending |
| RELY-03 | Phase TBD | Pending |
| RELY-04 | Phase TBD | Pending |
| ORCH-01 | Phase TBD | Pending |
| ORCH-02 | Phase TBD | Pending |
| ORCH-03 | Phase TBD | Pending |
| ORCH-04 | Phase TBD | Pending |
| QUAL-01 | Phase TBD | Pending |
| QUAL-02 | Phase TBD | Pending |
| QUAL-03 | Phase TBD | Pending |
| QUAL-04 | Phase TBD | Pending |
| QUAL-05 | Phase TBD | Pending |
| DATA-01 | Phase TBD | Pending |
| DATA-02 | Phase TBD | Pending |
| DATA-03 | Phase TBD | Pending |
| CLI-01 | Phase TBD | Pending |
| CLI-02 | Phase TBD | Pending |
| CLI-03 | Phase TBD | Pending |
| TEST-01 | Phase TBD | Pending |
| TEST-02 | Phase TBD | Pending |
| TEST-03 | Phase TBD | Pending |

**Coverage:**
- v1 requirements: 22 total
- Mapped to phases: 0
- Unmapped: 22 ⚠️

---
*Requirements defined: 2026-04-14*
*Last updated: 2026-04-14 after initial definition*
