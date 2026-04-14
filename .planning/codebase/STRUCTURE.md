# Codebase Structure

**Analysis Date:** 2026-04-14

## Directory Layout

```
multi_agent_campaign_creator/
├── src/                    # Application package and runtime code
│   ├── agents/             # Agent factories and shared LLM helper
│   ├── models/             # Pydantic data contracts and enums
│   ├── tasks/              # CrewAI task templates and dependency wiring
│   ├── tools/              # Custom CrewAI tools used by specialist agents
│   ├── workflow/           # Campaign orchestration facade
│   ├── output/             # Generated markdown/json campaign artifacts
│   ├── config.py           # Environment-backed immutable settings singleton
│   └── main.py             # CLI entry module
├── tests/                  # Pytest suite for agents, tools, and workflow
├── .github/workflows/      # CI workflow definitions
├── .planning/codebase/     # Generated mapping docs for planning workflow
├── .env.example            # Environment variable template
├── pyproject.toml          # Package metadata and dependency declarations
└── README.md               # User/developer documentation
```

## Directory Purposes

**src/agents:**
- Purpose: Define specialist campaign roles and instantiate CrewAI `Agent` objects.
- Contains: `base_agent.py`, `research_agent.py`, `copywriter_agent.py`, `art_director_agent.py`, `manager_agent.py`, `__init__.py`.
- Key files: `src/agents/base_agent.py`, `src/agents/research_agent.py`.

**src/models:**
- Purpose: Shared typed domain models used throughout runtime and tests.
- Contains: `campaign_models.py`, `__init__.py`.
- Key files: `src/models/campaign_models.py`.

**src/tasks:**
- Purpose: Build CrewAI tasks and context dependencies from a campaign request.
- Contains: `campaign_tasks.py`, `__init__.py`.
- Key files: `src/tasks/campaign_tasks.py`.

**src/tools:**
- Purpose: Agent-usable helpers for trend, competitor, copy, and image prompt analysis.
- Contains: `trend_research_tool.py`, `competitor_analysis_tool.py`, `copy_evaluation_tool.py`, `image_prompt_tool.py`, `__init__.py`.
- Key files: `src/tools/trend_research_tool.py`, `src/tools/copy_evaluation_tool.py`.

**src/workflow:**
- Purpose: Assemble and execute the end-to-end sequential crew.
- Contains: `crew_workflow.py`, `__init__.py`.
- Key files: `src/workflow/crew_workflow.py`.

**tests:**
- Purpose: Validate wiring, deterministic tool behavior, and retry semantics.
- Contains: `test_agents.py`, `test_tools.py`, `test_workflow.py`, `conftest.py`.
- Key files: `tests/test_workflow.py`, `tests/test_tools.py`.

## Key File Locations

**Entry Points:**
- `src/main.py`: Process CLI arguments, gather campaign input, start workflow execution.

**Configuration:**
- `src/config.py`: Load `.env`, validate required keys/ranges, expose module-level `settings`.
- `pyproject.toml`: Define runtime/dev dependencies and Python version compatibility.

**Core Logic:**
- `src/workflow/crew_workflow.py`: Crew construction, rate-limit retries, brief formatting, file output.
- `src/tasks/campaign_tasks.py`: Task text templates and dependency graph.

**Testing:**
- `tests/test_workflow.py`: Orchestration and retry behavior checks.
- `tests/test_agents.py`: Base agent class behavior checks.
- `tests/test_tools.py`: JSON structure/scoring/prompt output checks.

## Naming Conventions

**Files:**
- Python modules use `snake_case.py` naming: `crew_workflow.py`, `campaign_tasks.py`.

**Directories:**
- Layer directories use concise lowercase names: `agents`, `models`, `tasks`, `tools`, `workflow`.

## Where to Add New Code

**New Feature:**
- Primary code: add orchestration updates in `src/workflow/crew_workflow.py` and supporting task definitions in `src/tasks/campaign_tasks.py`.
- Tests: add or extend tests in `tests/test_workflow.py` (workflow behavior) and `tests/test_tools.py` / `tests/test_agents.py` as needed.

**New Component/Module:**
- Implementation: place new domain models in `src/models/campaign_models.py`, new agent factories under `src/agents/`, and new tools under `src/tools/`.

**Utilities:**
- Shared helpers: place runtime-wide helpers in `src/config.py` (only for configuration) or create a new dedicated module under `src/` if not agent/tool specific.

## Special Directories

**src/output:**
- Purpose: Stores generated campaign output files (`*.md`, `*.json`).
- Generated: Yes.
- Committed: No (runtime artifacts; ignored in normal workflows).

**.planning/codebase:**
- Purpose: Stores codebase mapping documents used by GSD planning/execution commands.
- Generated: Yes.
- Committed: Yes, when documentation refresh is part of planning workflow.

**.env file present at repository root:**
- Purpose: Local environment configuration values.
- Generated: No.
- Committed: No.

---

*Structure analysis: 2026-04-14*
