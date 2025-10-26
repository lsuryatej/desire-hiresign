"""Interaction model for swipe/like/apply actions."""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum as SQLEnum, Index, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base


class InteractionType(str, enum.Enum):
    """Interaction type enum."""
    LIKE = "like"
    SKIP = "skip"
    APPLY = "apply"
    SUPER_LIKE = "super_like"  # Future enhancement


class Interaction(Base):
    """Interaction model for user actions."""
    __tablename__ = "interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # User who performed the action
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Target could be a profile or listing
    target_type = Column(String(20), nullable=False)  # "profile" or "listing"
    target_id = Column(Integer, nullable=False, index=True)
    
    # Action type
    action = Column(SQLEnum(InteractionType, native_enum=False), nullable=False, index=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Relationships - use backref to avoid circular imports
    user = relationship("User", foreign_keys=[user_id])
    
    # Composite unique constraint to prevent duplicates
    __table_args__ = (
        Index('idx_user_target_type_action', 'user_id', 'target_type', 'target_id', 'action'),
    )
    
    def __repr__(self):
        return f"<Interaction {self.id}: {self.user_id} {self.action} {self.target_type} {self.target_id}>"

