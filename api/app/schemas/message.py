"""Message schemas."""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class MessageCreate(BaseModel):
    """Schema for creating a message."""

    content: str = Field(..., min_length=1, max_length=5000, description="Message content")
    match_id: int = Field(..., description="Match ID")


class MessageResponse(BaseModel):
    """Response schema for message."""

    id: int
    match_id: int
    sender_id: int
    content: str
    read: bool
    read_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class MessageUpdate(BaseModel):
    """Schema for updating a message (mark as read)."""

    read: Optional[bool] = None
