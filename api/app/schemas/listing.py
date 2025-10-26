"""Listing schemas."""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from app.models.listing import ListingStatus


class ListingBase(BaseModel):
    """Base listing schema."""
    title: str = Field(..., max_length=255, description="Job title")
    company: str = Field(..., max_length=255, description="Company name")
    description: str = Field(..., description="Job description")
    skills_required: List[str] = Field(..., description="Required skills")
    location: Optional[str] = Field(None, max_length=255, description="Job location")
    remote_preference: Optional[str] = Field(None, pattern="^(remote|onsite|hybrid)$", description="Remote preference")
    salary_min: Optional[Decimal] = Field(None, ge=0, description="Minimum salary")
    salary_max: Optional[Decimal] = Field(None, ge=0, description="Maximum salary")
    hourly_rate: Optional[Decimal] = Field(None, ge=0, description="Hourly rate")
    equity_offered: Optional[bool] = Field(False, description="Equity offered")
    media_refs: Optional[dict] = Field(default={}, description="Media references")


class ListingCreate(ListingBase):
    """Schema for creating a listing."""
    status: ListingStatus = ListingStatus.DRAFT


class ListingUpdate(BaseModel):
    """Schema for updating a listing."""
    title: Optional[str] = Field(None, max_length=255)
    company: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    skills_required: Optional[List[str]] = None
    location: Optional[str] = Field(None, max_length=255)
    remote_preference: Optional[str] = Field(None, pattern="^(remote|onsite|hybrid)$")
    salary_min: Optional[Decimal] = Field(None, ge=0)
    salary_max: Optional[Decimal] = Field(None, ge=0)
    hourly_rate: Optional[Decimal] = Field(None, ge=0)
    equity_offered: Optional[bool] = None
    media_refs: Optional[dict] = None
    status: Optional[ListingStatus] = None


class ListingResponse(ListingBase):
    """Response schema for listing."""
    id: int
    user_id: int
    status: ListingStatus
    is_boosted: bool
    boosted_until: Optional[datetime]
    is_active: bool
    flagged: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ListingCard(BaseModel):
    """Minimal listing card for feed/list views."""
    id: int
    title: str
    company: str
    location: Optional[str]
    remote_preference: Optional[str]
    skills_required: List[str]
    hourly_rate: Optional[Decimal]
    salary_min: Optional[Decimal]
    salary_max: Optional[Decimal]
    created_at: datetime
    is_boosted: bool
    
    class Config:
        from_attributes = True


class ListingFilter(BaseModel):
    """Schema for listing filters."""
    skills: Optional[List[str]] = None
    location: Optional[str] = None
    remote_preference: Optional[str] = None
    min_salary: Optional[Decimal] = None
    max_salary: Optional[Decimal] = None
    status: Optional[ListingStatus] = ListingStatus.ACTIVE
