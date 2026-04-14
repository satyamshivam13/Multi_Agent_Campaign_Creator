# Multi-Agent Campaign Creator

## What This Is

A Python CLI that generates end-to-end marketing campaigns using a sequential CrewAI workflow with four specialist agents: research, copywriting, art direction, and strategy management. It takes a structured campaign brief and produces Markdown and JSON campaign outputs for quick iteration and handoff. The primary users are marketers, founders, and builders who need fast campaign drafts with grounded structure.

## Core Value

Generate a coherent, usable campaign brief from one product input in minutes, not days.

## Requirements

### Validated

- ✓ Run an end-to-end sequential multi-agent campaign pipeline — existing (`src/workflow/crew_workflow.py`)
- ✓ Support interactive and demo CLI flows for campaign request intake — existing (`src/main.py`)
- ✓ Produce campaign artifacts as Markdown and JSON files — existing (`src/workflow/crew_workflow.py`)
- ✓ Use typed campaign schemas and validation via Pydantic models — existing (`src/models/campaign_models.py`)
- ✓ Include deterministic analysis tools for trends, competitors, copy evaluation, and image prompts — existing (`src/tools/`)

### Active

- [ ] Improve execution reliability under provider throttling and transient API failures with stronger retries/fallback behavior
- [ ] Expand campaign output quality with richer structured sections (budget allocation, KPI detail, implementation timeline fidelity)
- [ ] Increase production readiness through better config hardening, observability, and safer error handling paths

### Out of Scope

- Native mobile applications — current product scope is a Python CLI workflow
- Full enterprise orchestration platform (multi-tenant auth, billing, RBAC) — not needed for current single-team usage

## Context

- Codebase is brownfield and already organized by domain layers: `agents`, `tasks`, `tools`, `models`, `workflow`
- CrewAI is the orchestration runtime and Groq is the primary LLM provider (`src/agents/base_agent.py`, `src/config.py`)
- Outputs are currently file-based under `src/output`, which is sufficient for local runs but limited for history/search/reporting
- Existing tests cover core wiring and portions of workflow behavior (`tests/test_agents.py`, `tests/test_tools.py`, `tests/test_workflow.py`)
- Main short-term risks are rate limits, dependency drift, and partial runtime/test mismatches between stubbed and production agent paths

## Constraints

- **Tech stack**: Python + CrewAI + Groq — keep implementation aligned with existing architecture
- **Provider quota**: Groq TPM limits can interrupt runs — guardrails and retries must account for burst usage
- **Compatibility**: Preserve current CLI UX and output contracts for existing users
- **Security**: Avoid leaking raw provider/internal details in normal-mode error output

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Keep CLI-first product surface for now | Fastest path to usable automation and easy local iteration | ✓ Good |
| Treat current implemented capabilities as initial validated requirements | Brownfield repo already has working generation pipeline and tests | ✓ Good |
| Prioritize reliability and production-hardening before adding large new feature surface | Current value depends on successful campaign completion and stable behavior | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-04-14 after initialization*
