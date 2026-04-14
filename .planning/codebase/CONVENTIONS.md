# Coding Conventions

**Analysis Date:** 2026-04-14

## Naming Patterns

**Files:**
- Use `snake_case.py` for module names (examples: `src/workflow/crew_workflow.py`, `src/tools/trend_research_tool.py`).
- Keep test files as `test_*.py` under `tests/` (examples: `tests/test_workflow.py`, `tests/test_tools.py`).

**Functions:**
- Use `snake_case` for function and method names (examples: `get_llm` in `src/agents/base_agent.py`, `_compute_retry_delay` in `src/workflow/crew_workflow.py`).
- Use leading underscore for non-public helpers (examples: `_build_brief`, `_simulated_search`, `_run`).

**Variables:**
- Use `snake_case` for locals and attributes (examples: `retry_attempt`, `groq_max_tokens`, `channel_limits`).
- Use uppercase constants for module-level constants (example: `RATE_LIMIT_ERROR_MARKERS` in `src/workflow/crew_workflow.py`).

**Types:**
- Use `PascalCase` for classes and Pydantic models (examples: `CampaignCrew`, `CampaignRequest`, `CopyEvaluationTool`).
- Use enum members in `UPPER_SNAKE_CASE` (examples: `CampaignChannel.SOCIAL_MEDIA`, `CopyTone.PROFESSIONAL` in `src/models/campaign_models.py`).

## Code Style

**Formatting:**
- No formatter configuration detected (`pyproject.toml` does not define Black/Ruff/isort settings).
- Follow existing style: type hints for most public methods and concise module/class/function docstrings.
- Keep line wrapping readable for long strings and constructor calls (patterns visible in `src/main.py` and `src/tasks/campaign_tasks.py`).
- Correct mixed indentation where introduced: tabs are present in `src/config.py` and `src/models/__init__.py`; new edits should use 4 spaces.

**Linting:**
- CI linting is configured in `.github/workflows/tests.yml` using `flake8 src --select=E9,F63,F7,F82`.
- Lint step is non-blocking (`continue-on-error: true`), so local code changes should still be validated before commit.

## Import Organization

**Order:**
1. Standard library imports first (examples: `datetime`, `re`, `time` in `src/workflow/crew_workflow.py`).
2. Third-party packages next (examples: `crewai`, `rich`, `pydantic`, `httpx`).
3. Project-local imports last via `src.*` absolute imports.

**Path Aliases:**
- No custom alias system detected; use absolute package imports rooted at `src` (example: `from src.models import CampaignRequest` in `src/tasks/campaign_tasks.py`).

## Error Handling

**Patterns:**
- Validate critical environment settings at startup and raise `EnvironmentError` for invalid/missing values (`src/config.py`).
- Guard runtime boundaries with `try/except` and user-facing error output (`run_campaign` in `src/main.py`).
- For transient provider failures, detect retryable errors, back off, and re-raise after retry budget is exhausted (`CampaignCrew.run` in `src/workflow/crew_workflow.py`).

## Logging

**Framework:** `rich` console output for runtime messaging (`src/main.py`, `src/workflow/crew_workflow.py`).

**Patterns:**
- Use `console.print` with semantic color/status formatting for progress and errors.
- Avoid raw `print()` in workflow/CLI code.

## Comments

**When to Comment:**
- Use brief section comments for high-level phases (examples: "Build agents", "Save to disk" in `src/workflow/crew_workflow.py`).
- Keep comments focused on behavior intent, not obvious syntax.

**JSDoc/TSDoc:**
- Not applicable.
- Python docstrings are used at module, class, and method level throughout `src/`.

## Function Design

**Size:**
- Keep orchestration methods moderate and split logic into helpers (`run` delegates to `_compute_retry_delay`, `_build_brief`, `_save_outputs` in `src/workflow/crew_workflow.py`).

**Parameters:**
- Prefer explicit typed parameters with defaults for optional behavior (examples: `_run(..., channel: str = "general")` in `src/tools/copy_evaluation_tool.py`).
- Use strongly-typed Pydantic input schemas for CrewAI tool arguments (`args_schema` pattern in `src/tools/*.py`).

**Return Values:**
- Return typed domain models at workflow boundaries (`CampaignBrief` from `CampaignCrew.run`).
- Tool methods return serialized JSON strings for agent interoperability (`_run` in all tool modules under `src/tools/`).

## Module Design

**Exports:**
- Package `__init__.py` files re-export intended public symbols via `__all__` (examples: `src/agents/__init__.py`, `src/tools/__init__.py`, `src/models/__init__.py`).

**Barrel Files:**
- Use package-level barrels for cross-module imports (`from src.agents import ...` and `from src.models import ...`).

---

*Convention analysis: 2026-04-14*
