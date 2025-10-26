from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List

from app.core.database import get_db
from app.core.auth import get_current_active_user
from app.models.user import User
from app.models.profile import Profile
from app.schemas.profile import ProfileCreate, ProfileUpdate, ProfileResponse, ProfileCard

router = APIRouter(prefix="/profiles", tags=["profiles"])


def calculate_completeness_score(profile: Profile) -> int:
    """Calculate profile completeness score (0-100)."""
    score = 0
    total_fields = 10
    
    if profile.headline:
        score += 1
    if profile.bio:
        score += 1
    if profile.skills and len(profile.skills) > 0:
        score += 1
    if profile.portfolio_links and len(profile.portfolio_links) > 0:
        score += 1
    if profile.availability:
        score += 1
    if profile.hourly_rate is not None:
        score += 1
    if profile.location:
        score += 1
    if profile.remote_preference:
        score += 1
    if profile.media_refs and profile.media_refs.get("profile_image"):
        score += 1
    if profile.media_refs and profile.media_refs.get("gallery") and len(profile.media_refs["gallery"]) > 0:
        score += 1
    
    return int((score / total_fields) * 100)


@router.post("", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_profile(
    profile_data: ProfileCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new profile for the current user."""
    # Check if profile already exists
    existing_profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile already exists. Use PUT to update."
        )
    
    # Create profile
    profile_dict = profile_data.model_dump()
    new_profile = Profile(user_id=current_user.id, **profile_dict)
    new_profile.completeness_score = calculate_completeness_score(new_profile)
    
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    
    return ProfileResponse.model_validate(new_profile)


@router.get("/me", response_model=ProfileResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current user's profile."""
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    return ProfileResponse.model_validate(profile)


@router.get("/{profile_id}", response_model=ProfileResponse)
async def get_profile(
    profile_id: int,
    db: Session = Depends(get_db)
):
    """Get a profile by ID."""
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    return ProfileResponse.model_validate(profile)


@router.put("/me", response_model=ProfileResponse)
async def update_profile(
    profile_data: ProfileUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update current user's profile."""
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    # Update fields
    update_data = profile_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if hasattr(profile, field):
            setattr(profile, field, value)
    
    # Recalculate completeness score
    profile.completeness_score = calculate_completeness_score(profile)
    
    db.commit()
    db.refresh(profile)
    
    return ProfileResponse.model_validate(profile)


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete current user's profile."""
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    db.delete(profile)
    db.commit()
    
    return None


@router.get("/feed", response_model=List[ProfileCard])
async def get_profile_feed(
    skip: int = 0,
    limit: int = 20,
    exclude_ids: str = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get a feed of profiles for swiping.
    
    Returns profiles excluding:
    - Current user's own profile
    - Already interacted profiles (optional via exclude_ids)
    - Inactive profiles
    
    Features:
    - Cursor-based pagination
    - Randomized order
    - Minimal payload for fast loading
    """
    from sqlalchemy import func
    
    # Base query for active profiles
    query = db.query(Profile).filter(
        and_(
            Profile.is_active == True,
            Profile.user_id != current_user.id
        )
    )
    
    # Exclude already interacted profiles if provided
    if exclude_ids:
        exclude_list = [int(x) for x in exclude_ids.split(',') if x.strip().isdigit()]
        if exclude_list:
            query = query.filter(~Profile.id.in_(exclude_list))
    
    # Order by randomness and completeness score
    profiles = query.order_by(
        func.random(),
        Profile.completeness_score.desc()
    ).offset(skip).limit(limit).all()
    
    # Convert to ProfileCard format
    result = []
    for profile in profiles:
        # Parse JSON fields
        skills = profile.skills if isinstance(profile.skills, list) else []
        portfolio_links = profile.portfolio_links if isinstance(profile.portfolio_links, list) else []
        media_refs = profile.media_refs if isinstance(profile.media_refs, dict) else {}
        
        # Get thumbnail if available
        thumbnail_url = None
        if media_refs.get("profile_image"):
            # In production, this would generate a fresh presigned URL
            thumbnail_url = media_refs["profile_image"]
        
        card = ProfileCard(
            id=profile.id,
            headline=profile.headline or "",
            skills=skills[:3] if skills else [],  # Top 3 skills
            location=profile.location,
            media_refs=media_refs,
            completeness_score=profile.completeness_score,
            created_at=profile.created_at
        )
        result.append(card)
    
    return result
