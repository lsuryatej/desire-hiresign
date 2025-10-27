"""Report schemas."""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ReportCreate(BaseModel):
    """Schema for creating a report."""

    report_type: str = Field(..., description="Type of report (profile, listing, message, media)")
    target_id: int = Field(..., description="ID of the content being reported")
    reason: str = Field(..., min_length=1, max_length=50, description="Reason for report")
    description: Optional[str] = Field(None, max_length=1000, description="Additional details")


class ReportResponse(BaseModel):
    """Response schema for report."""

    id: int
    reporter_id: int
    report_type: str
    target_id: int
    reason: str
    description: Optional[str]
    status: str
    reviewed_by: Optional[int]
    review_notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    reviewed_at: Optional[datetime]

    class Config:
        from_attributes = True


class ReportUpdate(BaseModel):
    """Schema for updating report status (admin only)."""

    status: str = Field(..., description="New status (pending, reviewed, resolved, dismissed)")
    review_notes: Optional[str] = Field(None, max_length=1000, description="Admin review notes")
