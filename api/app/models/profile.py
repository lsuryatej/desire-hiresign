from sqlalchemy import Column, Integer, String, Text, JSON, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False, index=True)
    
    # Basic info
    headline = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    
    # Skills and links
    skills = Column(JSON, default=list)  # ["UI Design", "Figma", "Prototyping"]
    portfolio_links = Column(JSON, default=list)  # [{"url": "...", "title": "..."}]
    
    # Availability and rates
    availability = Column(String, nullable=True)  # "available", "busy", "unavailable"
    hourly_rate = Column(Float, nullable=True)
    
    # Media references
    media_refs = Column(JSON, default=dict)  # {"profile_image": "...", "gallery": [...]}
    
    # Location
    location = Column(String, nullable=True)
    remote_preference = Column(String, nullable=True)  # "remote", "onsite", "hybrid"
    
    # Metadata
    is_active = Column(Boolean, default=True)
    completeness_score = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="profile")
