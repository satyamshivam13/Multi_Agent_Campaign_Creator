"""Tests for agent functionality"""

import pytest
from src.agents import ResearchAgent, CopywriterAgent, ArtDirectorAgent, ManagerAgent


class TestResearchAgent:
    """Test Research Agent"""
    
    def test_research_agent_initialization(self, research_agent):
        """Test that research agent initializes correctly"""
        assert research_agent.name == "Market Research Expert"
        assert research_agent.role == "Market Researcher"
    
    def test_research_agent_execute(self, research_agent):
        """Test research agent execution"""
        result = research_agent.execute("test task")
        assert "Research completed" in result


class TestCopywriterAgent:
    """Test Copywriter Agent"""
    
    def test_copywriter_agent_initialization(self, copywriter_agent):
        """Test that copywriter agent initializes correctly"""
        assert copywriter_agent.name == "Creative Copywriter"
        assert copywriter_agent.role == "Copywriter"
    
    def test_copywriter_agent_execute(self, copywriter_agent):
        """Test copywriter agent execution"""
        result = copywriter_agent.execute("test task")
        assert "Copy created" in result


class TestArtDirectorAgent:
    """Test Art Director Agent"""
    
    def test_art_director_agent_initialization(self, art_director_agent):
        """Test that art director agent initializes correctly"""
        assert art_director_agent.name == "Senior Art Director"
        assert art_director_agent.role == "Art Director"


class TestManagerAgent:
    """Test Manager Agent"""
    
    def test_manager_agent_initialization(self, manager_agent):
        """Test that manager agent initializes correctly"""
        assert manager_agent.name == "Campaign Manager"
        assert manager_agent.role == "Campaign Manager"
