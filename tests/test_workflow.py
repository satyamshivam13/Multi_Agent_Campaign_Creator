"""Tests for workflow orchestration"""

import pytest
from src.workflow import CampaignCrew
from src.models import CampaignRequest, CampaignChannel, CopyTone


class TestCampaignCrew:
    """Test Campaign Crew orchestration"""
    
    def test_crew_initialization_with_request(self):
        """Test that crew initializes with a campaign request"""
        request = CampaignRequest(
            product_name="Test Product",
            product_description="Test description",
            target_audience="Test audience",
            campaign_goals="Test goals",
            channels=[CampaignChannel.SOCIAL_MEDIA],
            brand_voice=CopyTone.PROFESSIONAL,
        )
        crew = CampaignCrew(request)
        assert crew.request is not None
        assert crew.researcher is not None
        assert crew.copywriter is not None
        assert crew.art_director is not None
        assert crew.manager is not None
    
    def test_crew_has_all_agents(self):
        """Test that crew initializes with all four agents"""
        request = CampaignRequest(
            product_name="Test Product",
            product_description="Test description",
            target_audience="Test audience",
            campaign_goals="Test goals",
            channels=[CampaignChannel.SOCIAL_MEDIA],
            brand_voice=CopyTone.PROFESSIONAL,
        )
        crew = CampaignCrew(request)
        
        assert crew.researcher is not None
        assert crew.copywriter is not None
        assert crew.art_director is not None
        assert crew.manager is not None
    
    def test_crew_builds_tasks(self):
        """Test that crew properly builds tasks"""
        request = CampaignRequest(
            product_name="Test Product",
            product_description="Test description",
            target_audience="Test audience",
            campaign_goals="Test goals",
            channels=[CampaignChannel.SOCIAL_MEDIA],
            brand_voice=CopyTone.PROFESSIONAL,
        )
        crew = CampaignCrew(request)
        
        assert crew.research_task is not None
        assert crew.copy_task is not None
        assert crew.art_task is not None
        assert crew.manager_task is not None

