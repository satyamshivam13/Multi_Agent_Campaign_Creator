# Testing Patterns

**Analysis Date:** 2026-04-14

## Test Framework

**Runner:**
- `pytest` (declared in optional dev dependencies in `pyproject.toml`).
- Config: No dedicated `pytest.ini`/`tox.ini` detected; defaults plus CLI flags are used.

**Assertion Library:**
- Built-in `pytest` assertions (`assert ...`) with optional `pytest.raises`.

**Run Commands:**
```bash
pytest tests/ -v                          # Run all tests
pytest tests/test_agents.py -v            # Run one test module
pytest tests/ --cov=src --cov-report=html # Coverage report
```
- CI also uses `pytest tests/ -v --tb=short` in `.github/workflows/tests.yml`.

## Test File Organization

**Location:**
- Centralized test suite under `tests/` (not co-located with source files).

**Naming:**
- File naming uses `test_*.py`.
- Test classes use `Test*` naming (`TestCampaignCrew`, `TestImagePromptGeneratorTool`).
- Test functions use `test_*` naming throughout `tests/`.

**Structure:**
```
tests/
├── conftest.py
├── test_agents.py
├── test_tools.py
└── test_workflow.py
```

## Test Structure

**Suite Organization:**
```python
class TestCampaignCrew:
    def test_run_retries_rate_limit_then_succeeds(self, monkeypatch):
        ...
```
- Group tests by feature/module class in `tests/test_agents.py`, `tests/test_tools.py`, and `tests/test_workflow.py`.

**Patterns:**
- Shared fixtures are defined in `tests/conftest.py` for agent instances and sample request objects.
- Per-class setup uses `setup_method` for tool instances in `tests/test_tools.py`.
- Assertions verify both shape and behavior (examples: JSON keys, retry-call counts, sleep durations).

## Mocking

**Framework:**
- `pytest` `monkeypatch` fixture.

**Patterns:**
```python
monkeypatch.setattr(crew_workflow, "settings", _Settings())
monkeypatch.setattr(crew_workflow.time, "sleep", lambda s: sleeps.append(s))
monkeypatch.setattr(type(crew.crew), "kickoff", lambda _self: _kickoff())
```
- Use monkeypatch to isolate external effects and make retries deterministic (`tests/test_workflow.py`).

**What to Mock:**
- External or side-effect boundaries: provider settings, network-like workflow kickoff, `time.sleep`, output persistence hooks.

**What NOT to Mock:**
- Deterministic pure logic inside tools and model composition paths (these are exercised directly in `tests/test_tools.py`).

## Fixtures and Factories

**Test Data:**
```python
@pytest.fixture
def sample_request() -> CampaignRequest:
    return CampaignRequest(...)
```
- Fixtures in `tests/conftest.py` provide reusable domain objects and agent instances.

**Location:**
- Shared fixtures live in `tests/conftest.py`.
- Inline fixture-like setup (`setup_method`) is used where object creation is lightweight.

## Coverage

**Requirements:**
- No minimum coverage threshold enforced in config.
- Coverage generation exists in CI and local docs but is non-blocking in CI workflow.

**View Coverage:**
```bash
pytest tests/ --cov=src --cov-report=xml --cov-report=term
pytest tests/ --cov=src --cov-report=html
```

## Test Types

**Unit Tests:**
- Primary testing mode.
- Agent tests validate initialization and simple execute stubs (`tests/test_agents.py`).
- Tool tests validate deterministic JSON outputs and scoring behavior (`tests/test_tools.py`).

**Integration Tests:**
- Lightweight orchestration integration is covered by `CampaignCrew` tests with monkeypatched execution boundaries (`tests/test_workflow.py`).

**E2E Tests:**
- Not detected.

## Common Patterns

**Async Testing:**
```python
# Not detected in current suite.
# pytest-asyncio is listed in dependencies but no async tests are present.
```

**Error Testing:**
```python
with pytest.raises(Exception, match="429 Too Many Requests"):
    crew.run()
```
- Explicitly test retry exhaustion and exception propagation in workflow tests.

---

*Testing analysis: 2026-04-14*
