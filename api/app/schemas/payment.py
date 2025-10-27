"""Payment schemas."""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PaymentCreate(BaseModel):
    """Schema for creating a payment."""

    listing_id: int = Field(..., description="Listing ID to boost")
    payment_type: str = Field(..., description="Payment type (boost)")


class PaymentResponse(BaseModel):
    """Response schema for payment."""

    id: int
    user_id: int
    payment_type: str
    amount: float
    currency: str
    status: str
    listing_id: Optional[int]
    stripe_checkout_session_id: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True


class CheckoutSessionResponse(BaseModel):
    """Response schema for checkout session."""

    session_id: str
    session_url: str
    payment_id: int


class WebhookPayload(BaseModel):
    """Schema for Stripe webhook payload."""

    event_type: str
    data: dict
