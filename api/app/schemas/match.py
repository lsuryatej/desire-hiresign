"""Match schemas."""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MatchResponse(BaseModel):
    """Response schema for match."""

    id: int
    user1_id: int
    user2_id: int
    match_type: str
    is_active: bool
    unmatched: bool
    unmatched_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class MatchCreate(BaseModel):
    """Schema for creating a match."""

    user2_id: int
    match_type: str
