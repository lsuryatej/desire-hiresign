"""Report model for content moderation."""

from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class ReportStatus(enum.Enum):
    """Report status enum."""

    PENDING = "pending"
    REVIEWED = "reviewed"
    RESOLVED = "resolved"
    DISMISSED = "dismissed"


class ReportType(enum.Enum):
    """Report type enum."""

    PROFILE = "profile"
    LISTING = "listing"
    MESSAGE = "message"
    MEDIA = "media"


class Report(Base):
    """Report model for content moderation."""

    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    reporter_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    report_type = Column(Enum(ReportType, native_enum=False), nullable=False, index=True)
    target_id = Column(Integer, nullable=False, index=True)
    reason = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(ReportStatus, native_enum=False), default=ReportStatus.PENDING, index=True)
    reviewed_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    review_notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    reviewed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    reporter = relationship("User", foreign_keys=[reporter_id])
    reviewer = relationship("User", foreign_keys=[reviewed_by])

    def __repr__(self):
        return f"<Report {self.id}: {self.report_type.value} {self.target_id}>"
