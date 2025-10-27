"""Message model for in-app chat."""
from sqlalchemy import Column, Integer, ForeignKey, Text, Boolean, DateTime, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Message(Base):
    """Message model for chat between matched users."""
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("matches.id", ondelete="CASCADE"), nullable=False, index=True)
    sender_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    read = Column(Boolean, default=False)
    read_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Relationships
    match = relationship("Match", back_populates="messages")
    sender = relationship("User", foreign_keys=[sender_id])
    
    # Composite index for efficient queries
    __table_args__ = (
        Index('idx_match_created', 'match_id', 'created_at'),
    )
    
    def __repr__(self):
        return f"<Message {self.id}: {self.sender_id} -> {self.match_id}>"

