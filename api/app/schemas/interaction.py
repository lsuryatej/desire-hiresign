"""Interaction schemas."""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.interaction import InteractionType


class InteractionCreate(BaseModel):
    """Schema for creating an interaction."""
    target_type: str = Field(..., pattern="^(profile|listing)$", description="Target type: profile or listing")
    target_id: int = Field(..., description="ID of the target profile or listing")
    action: InteractionType = Field(..., description="Action type: like, skip, apply, or super_like")


class InteractionResponse(BaseModel):
    """Response schema for interaction."""
    id: int
    user_id: int
    target_type: str
    target_id: int
    action: InteractionType
    created_at: datetime
    
    class Config:
        from_attributes = True


class InteractionFilter(BaseModel):
    """Schema for filtering interactions."""
    target_type: Optional[str] = Field(None, pattern="^(profile|listing)$")
    action: Optional[InteractionType] = None
    limit: int = Field(50, ge=1, le=100)
    skip: int = Field(0, ge=0)

