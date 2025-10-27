"""Admin endpoints for content management."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_current_active_user
from app.models.user import User, UserRole
from app.models.profile import Profile
from app.models.listing import Listing, ListingStatus
from app.schemas.user import UserResponse
from app.schemas.profile import ProfileResponse
from app.schemas.listing import ListingResponse

router = APIRouter(prefix="/admin", tags=["admin"])


def require_admin(current_user: User = Depends(get_current_active_user)) -> User:
    """Dependency to ensure user is admin."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return current_user


# User Management


@router.get("/users", response_model=List[UserResponse])
async def get_all_users(
    skip: int = 0,
    limit: int = 50,
    role: Optional[str] = Query(None, description="Filter by role"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Get all users (admin only)."""
    query = db.query(User)

    if role:
        try:
            user_role = UserRole(role)
            query = query.filter(User.role == user_role)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid role. Must be one of: {[e.value for e in UserRole]}",
            )

    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    users = query.offset(skip).limit(limit).all()

    return [UserResponse.model_validate(u) for u in users]


@router.put("/users/{user_id}/activate")
async def activate_user(
    user_id: int, current_user: User = Depends(require_admin), db: Session = Depends(get_db)
):
    """Activate a user (admin only)."""
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.is_active = True
    db.commit()

    return {"message": "User activated successfully", "user_id": user_id}


@router.put("/users/{user_id}/deactivate")
async def deactivate_user(
    user_id: int, current_user: User = Depends(require_admin), db: Session = Depends(get_db)
):
    """Deactivate a user (admin only)."""
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.is_active = False
    db.commit()

    return {"message": "User deactivated successfully", "user_id": user_id}


@router.put("/users/{user_id}/role")
async def change_user_role(
    user_id: int,
    new_role: str = Query(..., description="New role"),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Change user role (admin only)."""
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    try:
        user_role = UserRole(new_role)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid role. Must be one of: {[e.value for e in UserRole]}",
        )

    user.role = user_role
    db.commit()

    return {"message": "User role updated successfully", "user_id": user_id, "new_role": new_role}


# Profile Management


@router.get("/profiles", response_model=List[ProfileResponse])
async def get_all_profiles(
    skip: int = 0,
    limit: int = 50,
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Get all profiles (admin only)."""
    query = db.query(Profile)

    if is_active is not None:
        query = query.filter(Profile.is_active == is_active)

    profiles = query.offset(skip).limit(limit).all()

    return [ProfileResponse.model_validate(p) for p in profiles]


@router.put("/profiles/{profile_id}/activate")
async def activate_profile(
    profile_id: int, current_user: User = Depends(require_admin), db: Session = Depends(get_db)
):
    """Activate a profile (admin only)."""
    profile = db.query(Profile).filter(Profile.id == profile_id).first()

    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

    profile.is_active = True
    db.commit()

    return {"message": "Profile activated successfully", "profile_id": profile_id}


@router.put("/profiles/{profile_id}/deactivate")
async def deactivate_profile(
    profile_id: int, current_user: User = Depends(require_admin), db: Session = Depends(get_db)
):
    """Deactivate a profile (admin only)."""
    profile = db.query(Profile).filter(Profile.id == profile_id).first()

    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

    profile.is_active = False
    db.commit()

    return {"message": "Profile deactivated successfully", "profile_id": profile_id}


# Listing Management


@router.get("/listings", response_model=List[ListingResponse])
async def get_all_listings(
    skip: int = 0,
    limit: int = 50,
    status: Optional[str] = Query(None, description="Filter by status"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    flagged: Optional[bool] = Query(None, description="Filter by flagged status"),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Get all listings (admin only)."""
    query = db.query(Listing)

    if status:
        try:
            listing_status = ListingStatus(status)
            query = query.filter(Listing.status == listing_status)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status. Must be one of: {[e.value for e in ListingStatus]}",
            )

    if is_active is not None:
        query = query.filter(Listing.is_active == is_active)

    if flagged is not None:
        query = query.filter(Listing.flagged == flagged)

    listings = query.offset(skip).limit(limit).all()

    return [ListingResponse.model_validate(l) for l in listings]


@router.put("/listings/{listing_id}/publish")
async def publish_listing(
    listing_id: int, current_user: User = Depends(require_admin), db: Session = Depends(get_db)
):
    """Publish a listing (admin only)."""
    listing = db.query(Listing).filter(Listing.id == listing_id).first()

    if not listing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing not found")

    listing.status = ListingStatus.ACTIVE
    listing.is_active = True
    db.commit()

    return {"message": "Listing published successfully", "listing_id": listing_id}


@router.put("/listings/{listing_id}/unpublish")
async def unpublish_listing(
    listing_id: int, current_user: User = Depends(require_admin), db: Session = Depends(get_db)
):
    """Unpublish a listing (admin only)."""
    listing = db.query(Listing).filter(Listing.id == listing_id).first()

    if not listing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing not found")

    listing.status = ListingStatus.DRAFT
    listing.is_active = False
    db.commit()

    return {"message": "Listing unpublished successfully", "listing_id": listing_id}


@router.put("/listings/{listing_id}/flag")
async def flag_listing(
    listing_id: int,
    flag_reason: str = Query(..., description="Reason for flagging"),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Flag a listing for review (admin only)."""
    listing = db.query(Listing).filter(Listing.id == listing_id).first()

    if not listing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing not found")

    listing.flagged = True
    listing.flag_reason = flag_reason
    db.commit()

    return {"message": "Listing flagged successfully", "listing_id": listing_id}


@router.put("/listings/{listing_id}/unflag")
async def unflag_listing(
    listing_id: int, current_user: User = Depends(require_admin), db: Session = Depends(get_db)
):
    """Unflag a listing (admin only)."""
    listing = db.query(Listing).filter(Listing.id == listing_id).first()

    if not listing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing not found")

    listing.flagged = False
    listing.flag_reason = None
    db.commit()

    return {"message": "Listing unflagged successfully", "listing_id": listing_id}


@router.delete("/listings/{listing_id}")
async def delete_listing(
    listing_id: int, current_user: User = Depends(require_admin), db: Session = Depends(get_db)
):
    """Delete a listing permanently (admin only)."""
    listing = db.query(Listing).filter(Listing.id == listing_id).first()

    if not listing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing not found")

    db.delete(listing)
    db.commit()

    return {"message": "Listing deleted successfully", "listing_id": listing_id}


# Statistics


@router.get("/stats/overview")
async def get_admin_stats(
    current_user: User = Depends(require_admin), db: Session = Depends(get_db)
):
    """Get platform statistics (admin only)."""
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    total_profiles = db.query(Profile).count()
    active_profiles = db.query(Profile).filter(Profile.is_active == True).count()
    total_listings = db.query(Listing).count()
    active_listings = db.query(Listing).filter(Listing.is_active == True).count()
    flagged_listings = db.query(Listing).filter(Listing.flagged == True).count()

    return {
        "users": {"total": total_users, "active": active_users},
        "profiles": {"total": total_profiles, "active": active_profiles},
        "listings": {
            "total": total_listings,
            "active": active_listings,
            "flagged": flagged_listings,
        },
    }
