"""Listing model for job postings."""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Numeric,
    ForeignKey,
    Boolean,
    DateTime,
    Enum as SQLEnum,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base


class ListingStatus(str, enum.Enum):
    """Listing status enum."""

    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    CLOSED = "closed"
    ARCHIVED = "archived"


class Listing(Base):
    """Listing model for job postings."""

    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # Job details
    title = Column(String(255), nullable=False, index=True)
    company = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    skills_required = Column(String(255), nullable=False)  # JSON array as string
    location = Column(String(255), nullable=True)
    remote_preference = Column(String(50), nullable=True)  # "remote", "onsite", "hybrid"

    # Compensation
    salary_min = Column(Numeric(10, 2), nullable=True)
    salary_max = Column(Numeric(10, 2), nullable=True)
    hourly_rate = Column(Numeric(10, 2), nullable=True)
    equity_offered = Column(Boolean, default=False)

    # Listing metadata
    status = Column(
        SQLEnum(ListingStatus, native_enum=False), default=ListingStatus.DRAFT, index=True
    )
    media_refs = Column(String(1000), nullable=True)  # JSON array as string

    # Boost/sponsor
    is_boosted = Column(Boolean, default=False, index=True)
    boosted_until = Column(DateTime, nullable=True)

    # Moderation
    is_active = Column(Boolean, default=True, index=True)
    flagged = Column(Boolean, default=False)
    flag_reason = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="listings")
    # interactions handled dynamically based on target_type and target_id

    def __repr__(self):
        return f"<Listing {self.id}: {self.title}>"
