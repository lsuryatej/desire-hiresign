"""Match model for mutual connections."""

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Match(Base):
    """Match model for mutual connections between users."""

    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)

    # Two users in the match
    user1_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user2_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # Match metadata
    match_type = Column(String(20), nullable=False, index=True)  # "like", "apply", "super_like"

    # Status
    is_active = Column(Boolean, default=True, index=True)
    unmatched = Column(Boolean, default=False)
    unmatched_at = Column(DateTime(timezone=True), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user1 = relationship("User", foreign_keys=[user1_id])
    user2 = relationship("User", foreign_keys=[user2_id])

    # Composite unique constraint
    __table_args__ = {"schema": "public"}

    def __repr__(self):
        return f"<Match {self.id}: {self.user1_id} <-> {self.user2_id}>"
