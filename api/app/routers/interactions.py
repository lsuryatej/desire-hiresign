"""Interaction endpoints for swipe/like/apply actions."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.core.database import get_db
from app.core.auth import get_current_active_user
from app.models.user import User
from app.models.interaction import Interaction, InteractionType
from app.schemas.interaction import InteractionCreate, InteractionResponse

router = APIRouter(prefix="/interactions", tags=["interactions"])


def check_duplicate_interaction(
    user_id: int, target_type: str, target_id: int, action: str, db: Session
) -> bool:
    """
    Check if a duplicate interaction exists within the last 24 hours.

    Args:
        user_id: User ID
        target_type: Type of target (profile/listing)
        target_id: ID of the target
        action: Action type
        db: Database session

    Returns:
        True if duplicate exists, False otherwise
    """
    from datetime import datetime, timedelta

    # Check for existing interaction within 24 hours
    time_threshold = datetime.utcnow() - timedelta(hours=24)

    existing = (
        db.query(Interaction)
        .filter(
            and_(
                Interaction.user_id == user_id,
                Interaction.target_type == target_type,
                Interaction.target_id == target_id,
                Interaction.action == action,
                Interaction.created_at >= time_threshold,
            )
        )
        .first()
    )

    return existing is not None


@router.post("", response_model=InteractionResponse, status_code=status.HTTP_201_CREATED)
async def create_interaction(
    interaction_data: InteractionCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Create a new interaction (like, skip, apply, etc.).

    Prevents duplicate interactions within 24 hours.
    """
    # Check for duplicate within 24 hours
    if check_duplicate_interaction(
        current_user.id,
        interaction_data.target_type,
        interaction_data.target_id,
        interaction_data.action.value,
        db,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"You have already {interaction_data.action.value}d this {interaction_data.target_type} recently",
        )

    # Validate target exists
    if interaction_data.target_type == "profile":
        from app.models.profile import Profile

        target = db.query(Profile).filter(Profile.id == interaction_data.target_id).first()
    elif interaction_data.target_type == "listing":
        from app.models.listing import Listing

        target = db.query(Listing).filter(Listing.id == interaction_data.target_id).first()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid target_type. Must be 'profile' or 'listing'",
        )

    if not target:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{interaction_data.target_type.capitalize()} not found",
        )

    # Check if user is interacting with their own content
    if interaction_data.target_type == "profile":
        from app.models.profile import Profile

        target = db.query(Profile).filter(Profile.id == interaction_data.target_id).first()
        if target and target.user_id == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You cannot interact with your own profile",
            )
    elif interaction_data.target_type == "listing":
        from app.models.listing import Listing

        target = db.query(Listing).filter(Listing.id == interaction_data.target_id).first()
        if target and target.user_id == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You cannot interact with your own listing",
            )

    # Create interaction
    new_interaction = Interaction(
        user_id=current_user.id,
        target_type=interaction_data.target_type,
        target_id=interaction_data.target_id,
        action=interaction_data.action,
    )

    db.add(new_interaction)
    db.commit()
    db.refresh(new_interaction)

    return InteractionResponse.model_validate(new_interaction)


@router.get("", response_model=List[InteractionResponse])
async def get_interactions(
    target_type: Optional[str] = Query(None, pattern="^(profile|listing)$"),
    action: Optional[InteractionType] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get interactions for the current user."""
    query = db.query(Interaction).filter(Interaction.user_id == current_user.id)

    # Apply filters
    if target_type:
        query = query.filter(Interaction.target_type == target_type)

    if action:
        query = query.filter(Interaction.action == action)

    interactions = query.order_by(Interaction.created_at.desc()).offset(skip).limit(limit).all()

    return [InteractionResponse.model_validate(i) for i in interactions]


@router.get("/stats")
async def get_interaction_stats(
    current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)
):
    """
    Get interaction statistics for the current user.
    """
    # Count by action type
    stats = {}

    for action in InteractionType:
        count = (
            db.query(Interaction)
            .filter(and_(Interaction.user_id == current_user.id, Interaction.action == action))
            .count()
        )
        stats[action.value] = count

    # Total interactions
    total = db.query(Interaction).filter(Interaction.user_id == current_user.id).count()

    return {"total_interactions": total, "by_action": stats}
