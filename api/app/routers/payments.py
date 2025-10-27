"""Payment endpoints for Stripe integration."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request, status, Header
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.auth import get_current_active_user
from app.core.config import settings
from app.models.user import User
from app.models.listing import Listing, ListingStatus
from app.models.payment import Payment, PaymentStatus, PaymentType
from app.schemas.payment import PaymentResponse, CheckoutSessionResponse, PaymentCreate

router = APIRouter(prefix="/payments", tags=["payments"])

# Stripe integration (stub for MVP)
STRIPE_API_KEY = getattr(settings, "stripe_secret_key", "sk_test_stub")


@router.post("/boost/create-checkout", response_model=CheckoutSessionResponse)
async def create_boost_checkout(
    payment_data: PaymentCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Create a Stripe checkout session for listing boost.

    In production, this would create an actual Stripe checkout session.
    For MVP, we'll create a stub payment record.
    """
    # Verify listing exists and user owns it
    listing = db.query(Listing).filter(Listing.id == payment_data.listing_id).first()

    if not listing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing not found")

    if listing.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You don't own this listing"
        )

    # Create payment record
    payment = Payment(
        user_id=current_user.id,
        payment_type=PaymentType.BOOST,
        amount=10.00,  # Boost price
        currency="usd",
        listing_id=listing.id,
        stripe_checkout_session_id=f"checkout_{current_user.id}_{datetime.utcnow().timestamp()}",
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    # In production, create actual Stripe checkout session
    # For MVP, return stub session URL
    session_id = f"cs_test_{payment.id}"
    session_url = f"https://checkout.stripe.com/pay/{session_id}"

    return CheckoutSessionResponse(
        session_id=session_id, session_url=session_url, payment_id=payment.id
    )


@router.post("/boost/confirm")
async def confirm_boost(
    payment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Confirm a boost payment (stub for MVP)."""
    payment = db.query(Payment).filter(Payment.id == payment_id).first()

    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")

    if payment.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your payment")

    listing = db.query(Listing).filter(Listing.id == payment.listing_id).first()
    if listing:
        # Activate boost for 7 days
        listing.is_boosted = True
        listing.boosted_until = datetime.utcnow() + timedelta(days=7)

    # Mark payment as completed
    payment.status = PaymentStatus.COMPLETED
    payment.completed_at = datetime.utcnow()

    db.commit()

    return {"message": "Boost activated successfully", "boosted_until": listing.boosted_until}


@router.get("/my-payments", response_model=List[PaymentResponse])
async def get_my_payments(
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get current user's payment history."""
    payments = (
        db.query(Payment)
        .filter(Payment.user_id == current_user.id)
        .order_by(Payment.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return [PaymentResponse.model_validate(p) for p in payments]


@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(None),
    db: Session = Depends(get_db),
):
    """
    Handle Stripe webhook events.

    For MVP, this is a stub. In production:
    - Verify webhook signature
    - Handle checkout.session.completed event
    - Mark payment as completed
    - Activate boost
    """
    # Webhook handling stub
    return {"received": True}
