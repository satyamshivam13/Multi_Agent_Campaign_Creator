# Technology Stack

**Analysis Date:** 2026-04-14

## Languages

**Primary:**
- Python 3.11+ - application and tests in `src/` and `tests/` (`pyproject.toml`, `src/main.py`, `tests/test_workflow.py`)

**Secondary:**
- Markdown - user/developer docs in `README.md` and `CONTRIBUTING.md`
- YAML - CI workflow config in `.github/workflows/tests.yml`

## Runtime

**Environment:**
- CPython 3.11+ required by project metadata (`pyproject.toml`) and CI matrix uses 3.11 and 3.12 (`.github/workflows/tests.yml`)

**Package Manager:**
- pip with editable install workflow (`pip install -e ".[dev]"`) documented in `README.md` and used in `.github/workflows/tests.yml`
- Build backend: setuptools (`pyproject.toml`)
- Lockfile: missing (no `poetry.lock`, `uv.lock`, or `requirements.txt` detected)

## Frameworks

**Core:**
- CrewAI >=0.86.0 - multi-agent orchestration (`src/workflow/crew_workflow.py`, `src/agents/*.py`)
- LangChain Groq integration (`langchain-groq`) - declared provider dependency in `pyproject.toml`
- Pydantic >=2.10.0 - request/response data models and tool schemas (`src/models/campaign_models.py`, `src/tools/*.py`)

**Testing:**
- pytest >=9.0 - unit/integration-style tests (`tests/`)
- pytest-asyncio >=0.24.0 - async test support declared in `pyproject.toml`
- pytest-cov >=4.0 - coverage reporting (`README.md`, `.github/workflows/tests.yml`)

**Build/Dev:**
- python-dotenv >=1.0.0 - `.env` loading in `src/config.py`
- rich >=13.0.0 - CLI rendering/progress panels in `src/main.py` and `src/workflow/crew_workflow.py`
- flake8 - optional CI lint gate in `.github/workflows/tests.yml`

## Key Dependencies

**Critical:**
- `crewai` - defines `Crew`, `Process`, `Agent`, and `Task` abstractions used by the whole workflow (`src/workflow/crew_workflow.py`, `src/tasks/campaign_tasks.py`)
- `crewai.llm.LLM` - Groq model client wrapper built in `src/agents/base_agent.py`
- `pydantic` - strict schema definitions for campaign domain and tools (`src/models/campaign_models.py`, `src/tools/trend_research_tool.py`)

**Infrastructure:**
- `httpx` - outbound HTTPS calls to Serper search endpoint in `src/tools/trend_research_tool.py`
- `python-dotenv` - environment bootstrapping in `src/config.py`
- `Jinja2` - declared dependency in `pyproject.toml` (no direct use detected in `src/`)

## Configuration

**Environment:**
- Environment loaded at import time via `load_dotenv()` in `src/config.py`
- Required key: `GROQ_API_KEY` validated in `Settings.__post_init__` (`src/config.py`)
- Optional Groq controls: `GROQ_MODEL`, `GROQ_TEMPERATURE`, `GROQ_MAX_TOKENS`, `GROQ_RATE_LIMIT_RETRIES`, `GROQ_RETRY_BASE_SECONDS`, `GROQ_RETRY_MAX_SECONDS` (`src/config.py`, `.env.example`)
- Optional research key: `SERPER_API_KEY`; absence triggers simulated trend output (`src/tools/trend_research_tool.py`)
- Output path control: `OUTPUT_DIR` with default `src/output` (`src/config.py`, `.env.example`)

**Build:**
- Packaging metadata and dependency declarations in `pyproject.toml`
- CI test workflow in `.github/workflows/tests.yml`

## Platform Requirements

**Development:**
- Windows/macOS/Linux shell with Python 3.11+ and pip (`README.md`)
- Network access required for live Groq and optional Serper requests (`src/agents/base_agent.py`, `src/tools/trend_research_tool.py`)
- Local `.env` file required for runtime configuration (`src/config.py`, `.env.example`)

**Production:**
- Deployment target: Not detected (project currently operates as a local CLI via `python -m src.main` in `src/main.py`)
- Runtime outputs persisted as local Markdown/JSON files under `src/output` (`src/workflow/crew_workflow.py`)

---

*Stack analysis: 2026-04-14*
