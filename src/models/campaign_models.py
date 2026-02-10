"""Pydantic models for campaign data structures"""

from enum import Enum
from typing import Optional, List, Dict
from datetime import datetime
from pydantic import BaseModel, Field


class CampaignChannel(str, Enum):
    """Available campaign channels."""
    SOCIAL_MEDIA = "social_media"
    EMAIL = "email"
    DISPLAY_ADS = "display_ads"
    INFLUENCER = "influencer"
    CONTENT_MARKETING = "content_marketing"
    VIDEO = "video"
    SEARCH_ADS = "search_ads"
    AFFILIATE = "affiliate"


class CopyTone(str, Enum):
    """Available copy tones/brand voices."""
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    PLAYFUL = "playful"
    LUXURY = "luxury"
    EDUCATIONAL = "educational"
    MOTIVATIONAL = "motivational"
    TECHNICAL = "technical"
    FRIENDLY = "friendly"


class CampaignRequest(BaseModel):
    """Structured request used by agents and workflows."""

    product_name: str = ""
    product_description: str = ""
    target_audience: str = ""
    campaign_goals: str = ""
    budget_range: Optional[str] = None
    channels: List[CampaignChannel] = Field(default_factory=list)
    brand_voice: CopyTone = CopyTone.PROFESSIONAL
    additional_context: Optional[str] = None


class CampaignBrief(BaseModel):
    """Input brief for campaign creation"""

    client_name: str = Field(..., description="Name of the client")
    campaign_name: str = Field(..., description="Name of the campaign")
    objective: str = Field(..., description="Primary campaign objective")
    target_audience: str = Field(..., description="Description of target audience")
    budget: Optional[float] = Field(None, description="Campaign budget")
    timeline: Optional[str] = Field(None, description="Campaign timeline")
    key_messages: List[str] = Field(
        default_factory=list, description="Key messages to convey"
    )
    constraints: Optional[str] = Field(
        None, description="Any constraints or limitations"
    )
    created_at: datetime = Field(default_factory=datetime.now)
    request: Optional[CampaignRequest] = None
    research: Optional["MarketResearch"] = None
    copy_package: Optional["CopyPackage"] = None
    visuals: Optional["VisualDirection"] = None
    executive_summary: str = ""
    implementation_timeline: List[str] = Field(default_factory=list)
    success_metrics: List[str] = Field(default_factory=list)
    estimated_budget_allocation: Dict[str, str] = Field(default_factory=dict)
    risk_factors: List[str] = Field(default_factory=list)
    final_recommendations: str = ""


class MarketResearch(BaseModel):
    """Market research output"""
    
    market_summary: str = ""
    trends: List[str] = Field(default_factory=list)
    opportunities: List[str] = Field(default_factory=list)
    audience_insights: Dict = Field(default_factory=dict)
    competitive_landscape: Dict = Field(default_factory=dict)


class CopyPackage(BaseModel):
    """Structured copy package for campaign execution."""

    campaign_tagline: str = ""
    elevator_pitch: str = ""
    channel_copy: Dict[str, Dict[str, str]] = Field(default_factory=dict)
    email_subjects: List[str] = Field(default_factory=list)
    hashtags: List[str] = Field(default_factory=list)


class VisualDirection(BaseModel):
    """Structured visual direction for creative assets."""

    brand_visual_identity: str = ""
    key_visuals: List[str] = Field(default_factory=list)
    image_prompts: List[str] = Field(default_factory=list)


class CreativeOutput(BaseModel):
    """Creative campaign output"""
    
    tagline: str = Field(..., description="Campaign tagline")
    primary_message: str = Field(..., description="Primary campaign message")
    ad_copy_variations: List[str] = Field(default_factory=list)
    visual_concepts: List[str] = Field(default_factory=list)
    image_prompts: List[str] = Field(default_factory=list)


class CampaignOutput(BaseModel):
    """Complete campaign output"""
    
    campaign_id: str = Field(..., description="Unique campaign ID")
    client_name: str = Field(..., description="Client name")
    campaign_name: str = Field(..., description="Campaign name")
    created_at: datetime = Field(default_factory=datetime.now)
    market_research: MarketResearch
    creative_output: CreativeOutput
    overall_strategy: str = Field(..., description="Overall campaign strategy")
    next_steps: List[str] = Field(default_factory=list)


class Campaign(BaseModel):
    """Main campaign model"""
    
    brief: CampaignBrief
    output: Optional[CampaignOutput] = None
    status: str = Field(default="draft", description="Campaign status")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    def mark_completed(self):
        """Mark campaign as completed"""
        self.status = "completed"
        self.updated_at = datetime.now()
