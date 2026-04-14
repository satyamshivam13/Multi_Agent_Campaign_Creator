# Technology Stack

**Project:** Multi-Agent Campaign Creator (brownfield Python CLI)
**Researched:** 2026-04-14
**Scope:** Next-milestone stack direction for reliability and production hardening

## Recommended 2026 Stack Direction (Opinionated)

### Core Runtime
| Technology | Version Direction | Purpose | Why This Fits This Codebase | Confidence |
|---|---|---|---|---|
| Python | 3.12 primary, 3.11 compatible | Runtime baseline | You already require >=3.11; moving CI/dev default to 3.12 improves ecosystem compatibility while avoiding risky jump to newer interpreter semantics in a reliability milestone. | HIGH |
| CrewAI | Pin to stable 1.14.x line (exact minor pin) | Multi-agent orchestration | Current app is CrewAI-first. CrewAI changelog shows active reliability/security fixes, checkpointing, and telemetry improvements in 2026; pinning avoids accidental regressions from wide ranges. | HIGH |
| Pydantic | v2.x (pinned minor) | Typed request/output contracts | Already central to your models; keep as core schema layer for deterministic CLI I/O contracts. | HIGH |

### Dependency and Environment Management
| Technology | Version Direction | Purpose | Why This Fits This Codebase | Confidence |
|---|---|---|---|---|
| uv | Current stable (project-managed) | Fast env/dependency/project management | Standard direction in modern Python projects; gives lock/sync workflows and reproducible installs for contributors and CI. | HIGH |
| pyproject.toml + lockfile | Commit lockfile to repo | Reproducible builds | Your current dependency spec uses broad lower-bounds only; lockfile is the single biggest reliability gain against drift. | HIGH |
| pip-audit | Latest stable in CI | Vulnerability scan for dependencies | CrewAI ecosystem has frequent security-related transitive updates; automated audit prevents stale vulnerable pins in release paths. | HIGH |

### Config, Retries, and Network Reliability
| Technology | Version Direction | Purpose | Why This Fits This Codebase | Confidence |
|---|---|---|---|---|
| pydantic-settings | 2.13.x line | Strongly validated settings | Replace ad-hoc dataclass+os.getenv parsing in src/config.py with typed settings, better env parsing, and less startup surprise. | HIGH |
| tenacity | Latest stable | Retry/backoff policies with jitter | Current retry loop in src/workflow/crew_workflow.py is custom and only message-matches errors; tenacity gives typed retry policies, jitter, and hooks for logging/metrics. | HIGH |
| httpx Client/AsyncClient with explicit transport limits/timeouts | Keep current httpx, add shared client wrappers | Harden outbound calls | You already depend on httpx. Standardize one configured client (timeouts, retries for connect errors, pooling) for tools/provider adapters to reduce flaky behavior. | HIGH |

### Observability and Diagnostics
| Technology | Version Direction | Purpose | Why This Fits This Codebase | Confidence |
|---|---|---|---|---|
| OpenTelemetry Python SDK + OTLP exporter | Current stable | Traces/metrics/log correlation | CrewAI docs emphasize observability and token/latency monitoring; OTel is the ecosystem standard and tool-neutral backend choice. | HIGH |
| Structured JSON logging (stdlib logging + json formatter, or structlog) | Current stable | Parseable production logs | Rich console output is good for local UX, but production hardening needs machine-parseable events with request/run IDs. | MEDIUM |

### Quality Gates and Developer Tooling
| Technology | Version Direction | Purpose | Why This Fits This Codebase | Confidence |
|---|---|---|---|---|
| Ruff (lint + format) | 0.15.x+ | Unified fast lint/format | Replace fragmented style/tooling setup with one fast tool and pre-commit integration. | HIGH |
| mypy | 1.20.x+ | Static typing checks | Mature and stable for brownfield strictness ramp-up; aligns with your Pydantic-heavy typed models. | HIGH |
| pre-commit | 4.5.x+ | Local quality enforcement | Enforce Ruff, mypy (targeted), tests/lint hooks before commits to stop drift early. | HIGH |
| pytest + pytest-cov + pytest-xdist | Keep pytest, add xdist | Test speed + confidence | Existing tests are already meaningful; xdist and stricter coverage thresholds improve release confidence with minimal rewrite. | HIGH |

## Practical Recommendations For This Exact Repo

1. Replace src/config.py dataclass settings with pydantic-settings BaseSettings and explicit field validators.
2. Replace manual while+sleep retry in src/workflow/crew_workflow.py with tenacity policies:
   - Retry on explicit provider/network exception classes first, string-match fallback second.
   - Add full jittered exponential backoff to reduce synchronized retry storms.
   - Emit retry attempt metadata into logs/traces.
3. Pin core runtime dependencies to tested ranges instead of open-ended lower bounds.
4. Add uv-managed lockfile and CI `uv sync --frozen` path.
5. Add OTel tracing around one campaign run:
   - span per crew kickoff
   - span per agent/task stage
   - attributes for model, token usage, latency, retry count
6. Keep file outputs for user-facing artifacts, but add a lightweight run-metadata store (SQLite) for history/search/debug in future milestone phases.

## What To Avoid (And Why)

| Avoid | Why It Hurts This Project | Better Choice | Confidence |
|---|---|---|---|
| Broad unpinned dependency specs (only `>=`) | Increases breakage risk from transitive updates, especially in fast-moving AI stacks | Pin tested ranges + lockfile in repo | HIGH |
| Expanding LangChain dependencies unless used | Your runtime path uses CrewAI LLM directly; extra langchain packages add dependency surface and CVE churn without clear value | Keep only dependencies actively used in src/ | MEDIUM |
| String-only error detection for rate limits as primary strategy | Fragile to provider message changes; misses other transient failures | Typed exception matching + policy-based retries (tenacity) | HIGH |
| Console-only human logs as production telemetry | Hard to aggregate, alert, or debug across runs | Structured logs + OTel traces | HIGH |
| Adopting ty as sole production type checker right now | ty is promising but still 0.x; not the conservative choice for hardening milestone | Keep mypy as gate; trial ty in non-blocking mode only | MEDIUM |
| Introducing heavyweight workflow platforms now (Airflow/Prefect) | Overkill for a single CLI sequential pipeline and slows delivery | Keep CLI-first; add reliability/telemetry first | MEDIUM |

## Suggested Dependency Set (Next Milestone)

### Runtime
- crewai (pinned tested minor)
- pydantic
- pydantic-settings
- python-dotenv (optional during migration; can be removed once settings strategy is finalized)
- httpx
- tenacity
- rich
- jinja2
- opentelemetry-api
- opentelemetry-sdk
- opentelemetry-exporter-otlp

### Dev/Test
- pytest
- pytest-cov
- pytest-xdist
- ruff
- mypy
- pre-commit
- pip-audit

## Confidence Notes

| Area | Level | Reason |
|---|---|---|
| Core Python tooling direction (uv, ruff, mypy, pre-commit) | HIGH | Verified in official docs and broad ecosystem adoption patterns. |
| CrewAI production direction | HIGH | Official CrewAI docs/changelog show active 2026 production features, fixes, and observability/checkpoint evolution. |
| Config/retry recommendations for this repo | HIGH | Directly maps to observed current code in src/config.py and src/workflow/crew_workflow.py. |
| LangChain pruning recommendation | MEDIUM | Repo signals low/no direct runtime use, but full dependency-usage audit should confirm before removal. |
| Type checker future direction (ty) | MEDIUM | Official docs show rapid progress, but 0.x maturity implies caution for blocking production gate. |

## Sources

- CrewAI docs and changelog: https://docs.crewai.com/ , https://docs.crewai.com/en/changelog
- uv docs: https://docs.astral.sh/uv/
- Ruff docs: https://docs.astral.sh/ruff/
- ty docs (maturity context): https://docs.astral.sh/ty/
- OpenTelemetry Python docs: https://opentelemetry.io/docs/languages/python/
- httpx transport/retry guidance: https://www.python-httpx.org/advanced/transports/
- Tenacity docs: https://tenacity.readthedocs.io/en/latest/
- mypy docs: https://mypy.readthedocs.io/en/stable/getting_started.html
- pre-commit docs: https://pre-commit.com/
- pip-audit docs/repo: https://github.com/pypa/pip-audit
- pydantic-settings package: https://pypi.org/project/pydantic-settings/
