"""Pytest configuration and shared fixtures"""

import pytest
from src.agents import ResearchAgent, CopywriterAgent, ArtDirectorAgent, ManagerAgent
from src.models import CampaignBrief, CampaignRequest


@pytest.fixture
def research_agent():
    """Fixture for research agent"""
    return ResearchAgent()


@pytest.fixture
def copywriter_agent():
    """Fixture for copywriter agent"""
    return CopywriterAgent()


@pytest.fixture
def art_director_agent():
    """Fixture for art director agent"""
    return ArtDirectorAgent()


@pytest.fixture
def manager_agent():
    """Fixture for manager agent"""
    return ManagerAgent()


@pytest.fixture
def sample_campaign_brief():
    """Fixture for sample campaign brief"""
    return CampaignBrief(
        client_name="TechCorp Inc",
        campaign_name="Innovation Launch 2024",
        objective="Launch a new AI-powered product",
        target_audience="Tech-savvy professionals aged 25-45",
        key_messages=["Revolutionary", "User-friendly", "Enterprise-grade"],
    )


@pytest.fixture
def sample_request() -> CampaignRequest:
    return CampaignRequest(
        product_name="AeroFlow Pro",
        target_audience=(
            "Health-conscious millennials and Gen-Z professionals (25-38) "
            "living in urban apartments"
        ),
        campaign_goals=(
            "Drive 10,000 pre-orders in 60 days, build brand awareness"
        ),
        channels=["social_media", "email", "display_ads", "influencer"],
        tone="professional",
    )
