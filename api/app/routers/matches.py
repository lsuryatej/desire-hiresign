"""Match endpoints for mutual connections."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.core.database import get_db
from app.core.auth import get_current_active_user
from app.models.user import User
from app.models.interaction import Interaction, InteractionType
from app.models.match import Match
from app.schemas.match import MatchResponse, MatchCreate

router = APIRouter(prefix="/matches", tags=["matches"])


def check_for_mutual_like(user1_id: int, user2_id: int, db: Session) -> bool:
    """
    Check if two users have mutually liked each other.

    Args:
        user1_id: First user ID
        user2_id: Second user ID
        db: Database session

    Returns:
        True if both users have liked each other, False otherwise
    """
    # Check if user1 has liked user2
    user1_liked = (
        db.query(Interaction)
        .filter(
            and_(
                Interaction.user_id == user1_id,
                Interaction.target_type == "profile",
                Interaction.target_id == user2_id,
                Interaction.action == InteractionType.LIKE,
            )
        )
        .first()
    )

    # Check if user2 has liked user1
    user2_liked = (
        db.query(Interaction)
        .filter(
            and_(
                Interaction.user_id == user2_id,
                Interaction.target_type == "profile",
                Interaction.target_id == user1_id,
                Interaction.action == InteractionType.LIKE,
            )
        )
        .first()
    )

    return user1_liked is not None and user2_liked is not None


def check_existing_match(user1_id: int, user2_id: int, db: Session) -> Match:
    """
    Check if a match already exists between two users.

    Args:
        user1_id: First user ID
        user2_id: Second user ID
        db: Database session

    Returns:
        Existing Match or None
    """
    return (
        db.query(Match)
        .filter(
            or_(
                and_(Match.user1_id == user1_id, Match.user2_id == user2_id),
                and_(Match.user1_id == user2_id, Match.user2_id == user1_id),
            )
        )
        .first()
    )


@router.post("", response_model=MatchResponse, status_code=status.HTTP_201_CREATED)
async def check_and_create_match(
    current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)
):
    """
    Check for new matches and create them.

    This should be called after each interaction to detect mutual likes.
    """
    new_matches = []

    # Get user's interactions where they liked someone
    user_likes = (
        db.query(Interaction)
        .filter(
            and_(
                Interaction.user_id == current_user.id,
                Interaction.target_type == "profile",
                Interaction.action == InteractionType.LIKE,
            )
        )
        .all()
    )

    for interaction in user_likes:
        target_user_id = interaction.target_id

        # Check if target user has liked back
        if check_for_mutual_like(current_user.id, target_user_id, db):
            # Check if match already exists
            existing_match = check_existing_match(current_user.id, target_user_id, db)

            if not existing_match:
                # Create new match
                match = Match(user1_id=current_user.id, user2_id=target_user_id, match_type="like")
                db.add(match)
                new_matches.append(match)

    if new_matches:
        db.commit()
        for match in new_matches:
            db.refresh(match)
        # Return the first new match
        return MatchResponse.model_validate(new_matches[0])
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No new matches found")


@router.get("", response_model=List[MatchResponse])
async def get_matches(
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get all matches for the current user."""
    matches = (
        db.query(Match)
        .filter(
            or_(Match.user1_id == current_user.id, Match.user2_id == current_user.id),
            Match.is_active == True,
            Match.unmatched == False,
        )
        .offset(skip)
        .limit(limit)
        .all()
    )

    return [MatchResponse.model_validate(m) for m in matches]


@router.get("/{match_id}", response_model=MatchResponse)
async def get_match(
    match_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get a specific match."""
    match = db.query(Match).filter(Match.id == match_id).first()

    if not match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Match not found")

    # Verify user is part of the match
    if match.user1_id != current_user.id and match.user2_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view this match",
        )

    return MatchResponse.model_validate(match)


@router.delete("/{match_id}", status_code=status.HTTP_200_OK)
async def unmatch(
    match_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Unmatch with someone."""
    match = db.query(Match).filter(Match.id == match_id).first()

    if not match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Match not found")

    # Verify user is part of the match
    if match.user1_id != current_user.id and match.user2_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to unmatch this user",
        )

    # Mark as unmatched
    match.unmatched = True
    match.is_active = False

    db.commit()

    return {"message": "Match unmatched successfully", "match_id": match_id}
