# External Integrations

**Analysis Date:** 2026-04-14

## APIs & External Services

**LLM Provider:**
- Groq - primary model inference backend for all CrewAI agents
  - SDK/Client: CrewAI `LLM` wrapper from `crewai.llm` configured with `model="groq/{model}"` in `src/agents/base_agent.py`
  - Auth: `GROQ_API_KEY` from environment (`src/config.py`, `.env.example`)

**Web Search / Trend Data:**
- Serper.dev Google Search API - optional live trend lookup used by research tool
  - SDK/Client: direct `httpx.post()` call in `src/tools/trend_research_tool.py`
  - Endpoint: `https://google.serper.dev/search` (`src/tools/trend_research_tool.py`)
  - Auth: `SERPER_API_KEY` sent as `X-API-KEY` header (`src/tools/trend_research_tool.py`)
  - Fallback behavior: deterministic simulated JSON when no key or when HTTP error occurs (`src/tools/trend_research_tool.py`)

## Data Storage

**Databases:**
- Not detected
  - Connection: Not applicable
  - Client: Not applicable

**File Storage:**
- Local filesystem output only
  - Markdown and JSON campaign artifacts written to `settings.output_dir` (default `src/output`) in `src/workflow/crew_workflow.py`

**Caching:**
- None detected

## Authentication & Identity

**Auth Provider:**
- API-key based service authentication (no user identity provider)
  - Implementation: environment variables loaded via `dotenv` and validated in `src/config.py`

## Monitoring & Observability

**Error Tracking:**
- None detected (no Sentry/New Relic/Bugsnag integrations in `src/`)

**Logs:**
- Console-first logging using Rich panels/messages (`src/main.py`, `src/workflow/crew_workflow.py`)
- Retry diagnostics for rate limits printed in workflow loop (`src/workflow/crew_workflow.py`)

## CI/CD & Deployment

**Hosting:**
- Not detected (no app hosting manifests; local CLI execution path in `src/main.py`)

**CI Pipeline:**
- GitHub Actions workflow executes install, optional flake8, tests, and coverage (`.github/workflows/tests.yml`)

## Environment Configuration

**Required env vars:**
- `GROQ_API_KEY` (required to initialize settings and run agents)
- `GROQ_MODEL` (optional model selection)
- `GROQ_TEMPERATURE` or `TEMPERATURE` (optional generation temperature)
- `GROQ_MAX_TOKENS` (optional token cap)
- `GROQ_RATE_LIMIT_RETRIES` (optional retry count)
- `GROQ_RETRY_BASE_SECONDS` (optional backoff base)
- `GROQ_RETRY_MAX_SECONDS` (optional backoff ceiling)
- `SERPER_API_KEY` (optional live search)
- `OUTPUT_DIR` (optional output location)

**Secrets location:**
- Local `.env` file loaded by `load_dotenv()` in `src/config.py`
- Template/non-secret defaults documented in `.env.example`

## Webhooks & Callbacks

**Incoming:**
- None detected (no HTTP server/endpoints in `src/`)

**Outgoing:**
- HTTPS POST to Serper search API from `src/tools/trend_research_tool.py`
- Outbound Groq model requests via CrewAI LLM backend from `src/agents/base_agent.py`

---

*Integration audit: 2026-04-14*
