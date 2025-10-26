from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ProfileBase(BaseModel):
    headline: Optional[str] = None
    bio: Optional[str] = None
    skills: List[str] = []
    portfolio_links: List[Dict[str, str]] = []
    availability: Optional[str] = None
    hourly_rate: Optional[float] = None
    media_refs: Dict[str, Any] = {}
    location: Optional[str] = None
    remote_preference: Optional[str] = None


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(BaseModel):
    headline: Optional[str] = None
    bio: Optional[str] = None
    skills: Optional[List[str]] = None
    portfolio_links: Optional[List[Dict[str, str]]] = None
    availability: Optional[str] = None
    hourly_rate: Optional[float] = None
    media_refs: Optional[Dict[str, Any]] = None
    location: Optional[str] = None
    remote_preference: Optional[str] = None


class ProfileResponse(ProfileBase):
    id: int
    user_id: int
    is_active: bool
    completeness_score: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ProfileCard(BaseModel):
    """Minimal profile data for card feed"""
    id: int
    user_id: int
    headline: Optional[str]
    bio: Optional[str]
    skills: List[str]
    location: Optional[str]
    thumbnail_url: Optional[str]
    availability: Optional[str]
    
    class Config:
        from_attributes = True
