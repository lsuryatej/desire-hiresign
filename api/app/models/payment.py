"""Payment model for transactions and boosts."""

from sqlalchemy import Column, Integer, ForeignKey, String, Float, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class PaymentStatus(enum.Enum):
    """Payment status enum."""

    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class PaymentType(enum.Enum):
    """Payment type enum."""

    BOOST = "boost"
    SUBSCRIPTION = "subscription"
    FEATURE = "feature"


class Payment(Base):
    """Payment model for transactions."""

    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    payment_type = Column(Enum(PaymentType, native_enum=False), nullable=False, index=True)

    # Stripe fields
    stripe_payment_intent_id = Column(String(255), nullable=True, unique=True, index=True)
    stripe_checkout_session_id = Column(String(255), nullable=True, unique=True, index=True)

    # Payment details
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="usd")
    status = Column(
        Enum(PaymentStatus, native_enum=False), default=PaymentStatus.PENDING, index=True
    )

    # Associated listing (for boosts)
    listing_id = Column(Integer, ForeignKey("listings.id", ondelete="SET NULL"), nullable=True)

    # Payment metadata
    payment_metadata = Column(String, nullable=True)  # JSON string for additional data

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    user = relationship("User", foreign_keys=[user_id])
    listing = relationship("Listing", foreign_keys=[listing_id])

    def __repr__(self):
        return f"<Payment {self.id}: {self.user_id} - {self.amount} {self.currency}>"
