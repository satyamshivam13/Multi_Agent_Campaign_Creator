"""
Workflow integration tests.

These test the CampaignCrew wiring (task graph, agent assignment)
without actually calling the LLM. For a full end-to-end test
set GROQ_API_KEY to a real key and run with `pytest -m e2e`.
"""

from __future__ import annotations

import pytest

from src.models import CampaignRequest
from src.tasks import CampaignTaskFactory
from src.workflow import CampaignCrew


class TestCampaignTaskFactory:
    def test_creates_four_tasks(self, sample_request: CampaignRequest):
        factory = CampaignTaskFactory(sample_request)
        from src.agents import (
            create_art_director_agent,
            create_copywriter_agent,
            create_manager_agent,
            create_research_agent,
        )

        r = create_research_agent()
        c = create_copywriter_agent()
        a = create_art_director_agent()
        m = create_manager_agent()

        t1 = factory.research_task(r)
        t2 = factory.copywriting_task(c, t1)
        t3 = factory.art_direction_task(a, t1, t2)
        t4 = factory.manager_task(m, t1, t2, t3)

        assert t1.agent == r
        assert t2.agent == c
        assert t3.agent == a
        assert t4.agent == m

    def test_copy_task_depends_on_research(self, sample_request: CampaignRequest):
        factory = CampaignTaskFactory(sample_request)
        from src.agents import create_copywriter_agent, create_research_agent

        r = create_research_agent()
        c = create_copywriter_agent()

        t1 = factory.research_task(r)
        t2 = factory.copywriting_task(c, t1)

        assert t1 in t2.context


class TestCampaignCrew:
    def test_crew_has_four_agents(self, sample_request: CampaignRequest):
        crew = CampaignCrew(sample_request)
        assert len(crew.crew.agents) == 4

    def test_crew_has_four_tasks(self, sample_request: CampaignRequest):
        crew = CampaignCrew(sample_request)
        assert len(crew.crew.tasks) == 4

    def test_crew_uses_sequential_process(self, sample_request: CampaignRequest):
        from crewai import Process
        crew = CampaignCrew(sample_request)
        assert crew.crew.process == Process.sequential
