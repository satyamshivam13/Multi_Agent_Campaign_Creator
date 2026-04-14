# Architecture

**Analysis Date:** 2026-04-14

## Pattern Overview

**Overall:** Sequential pipeline architecture around a CrewAI orchestration facade.

**Key Characteristics:**
- Single orchestration class (`src/workflow/crew_workflow.py`) composes all runtime collaborators.
- Layered package boundaries under `src/` (`agents`, `tools`, `tasks`, `models`, `workflow`).
- Typed domain contracts with Pydantic models in `src/models/campaign_models.py`.

## Layers

**CLI / Presentation Layer:**
- Purpose: Collect campaign input, render progress/errors, trigger workflow execution.
- Location: `src/main.py`
- Contains: Argument parsing, interactive prompts, request summary rendering, exception-to-exit handling.
- Depends on: `src/models/campaign_models.py`, `src/workflow/crew_workflow.py`, Rich console components.
- Used by: End users invoking `python -m src.main`.

**Workflow / Orchestration Layer:**
- Purpose: Build agents/tasks, execute CrewAI workflow, apply retry logic, persist outputs.
- Location: `src/workflow/crew_workflow.py`
- Contains: `CampaignCrew`, rate-limit detection/backoff logic, brief construction, markdown/json saving.
- Depends on: `src/agents/__init__.py`, `src/tasks/campaign_tasks.py`, `src/models/campaign_models.py`, `src/config.py`.
- Used by: `src/main.py` and workflow tests in `tests/test_workflow.py`.

**Agent Definition Layer:**
- Purpose: Define specialist agent personas and bind tools + LLM configuration.
- Location: `src/agents/*.py`
- Contains: `create_research_agent`, `create_copywriter_agent`, `create_art_director_agent`, `create_manager_agent`, and shared `get_llm` in `src/agents/base_agent.py`.
- Depends on: `src/tools/__init__.py` and `src/config.py`.
- Used by: `CampaignCrew` in `src/workflow/crew_workflow.py`.

**Task Composition Layer:**
- Purpose: Generate CrewAI `Task` objects with explicit context dependencies.
- Location: `src/tasks/campaign_tasks.py`
- Contains: `CampaignTaskFactory` and task templates for research, copywriting, art direction, and manager synthesis.
- Depends on: `src/models/__init__.py` and CrewAI `Task`.
- Used by: `CampaignCrew` during initialization.

**Tooling Layer:**
- Purpose: Provide deterministic or live external-analysis helpers exposed to agents.
- Location: `src/tools/*.py`
- Contains: Serper-backed trend lookup (`src/tools/trend_research_tool.py`) and deterministic analysis tools (`src/tools/competitor_analysis_tool.py`, `src/tools/copy_evaluation_tool.py`, `src/tools/image_prompt_tool.py`).
- Depends on: `src/config.py` for feature flags/API keys and Pydantic input schemas per tool.
- Used by: Agent factories in `src/agents/*.py`.

**Domain Model Layer:**
- Purpose: Define request/response schemas and enum vocabularies shared across layers.
- Location: `src/models/campaign_models.py`
- Contains: `CampaignRequest`, `CampaignBrief`, `MarketResearch`, `CopyPackage`, `VisualDirection`, enums like `CampaignChannel` and `CopyTone`.
- Depends on: Pydantic and Python stdlib types.
- Used by: CLI, task factory, workflow, tests.

## Data Flow

**Campaign Generation Flow:**

1. `src/main.py` collects CLI/demo input and builds a `CampaignRequest`.
2. `CampaignCrew.__init__` in `src/workflow/crew_workflow.py` creates agents and ordered tasks via `CampaignTaskFactory`.
3. `CampaignCrew.run` calls `self.crew.kickoff()` with retry/backoff around throttling errors.
4. Raw CrewAI output is wrapped into a typed `CampaignBrief` in `_build_brief`.
5. `_save_outputs` writes markdown and json campaign artifacts to `settings.output_dir`.

**State Management:**
- Runtime state is object-local (`CampaignCrew` instance fields) and immutable global config in `src/config.py` via module singleton `settings`.

## Key Abstractions

**CampaignCrew:**
- Purpose: Facade that hides CrewAI wiring details from CLI and tests.
- Examples: `src/workflow/crew_workflow.py`, `tests/test_workflow.py`.
- Pattern: Composition root plus orchestration service.

**CampaignTaskFactory:**
- Purpose: Encapsulate task descriptions and dependency chaining.
- Examples: `src/tasks/campaign_tasks.py`.
- Pattern: Factory with explicit upstream `context` linking.

**get_llm():**
- Purpose: Centralize LLM model/temperature/max token configuration.
- Examples: `src/agents/base_agent.py`, calls from each `src/agents/*_agent.py` file.
- Pattern: Shared configuration factory.

## Entry Points

**CLI Module Entry Point:**
- Location: `src/main.py`
- Triggers: `python -m src.main` (interactive) and `python -m src.main --demo`.
- Responsibilities: Build request, instantiate workflow, render success/failure output.

**Workflow Facade Entry Point:**
- Location: `src/workflow/crew_workflow.py`
- Triggers: `run_campaign()` in `src/main.py`.
- Responsibilities: Build and execute crew, retry on provider limits, persist outputs.

## Error Handling

**Strategy:** Raise early for invalid environment config, handle execution failures at boundary layers (CLI + workflow retry loop).

**Patterns:**
- Config validation in `Settings.__post_init__` (`src/config.py`) raises `EnvironmentError` for missing/invalid values.
- Runtime retry in `CampaignCrew.run` (`src/workflow/crew_workflow.py`) catches provider throttling signatures and sleeps with bounded backoff.

## Cross-Cutting Concerns

**Logging:** Console-oriented status reporting through Rich `Console` in `src/main.py` and `src/workflow/crew_workflow.py`.
**Validation:** Pydantic schema validation in `src/models/campaign_models.py` and tool arg schemas in `src/tools/*.py`.
**Authentication:** Environment-provided API keys loaded in `src/config.py` and consumed by `get_llm` / tool implementations.

---

*Architecture analysis: 2026-04-14*
