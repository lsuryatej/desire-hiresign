"""Message endpoints for chat."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.core.database import get_db
from app.core.auth import get_current_active_user
from app.models.user import User
from app.models.match import Match
from app.models.message import Message
from app.schemas.message import MessageCreate, MessageResponse, MessageUpdate

router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def create_message(
    message_data: MessageCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Send a message in a match."""
    # Verify match exists and user is part of it
    match = db.query(Match).filter(Match.id == message_data.match_id).first()

    if not match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Match not found")

    # Verify user is part of the match
    if match.user1_id != current_user.id and match.user2_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You are not part of this match"
        )

    # Create message
    new_message = Message(
        match_id=message_data.match_id, sender_id=current_user.id, content=message_data.content
    )

    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return MessageResponse.model_validate(new_message)


@router.get("/match/{match_id}", response_model=List[MessageResponse])
async def get_messages(
    match_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get all messages in a match."""
    # Verify match exists and user is part of it
    match = db.query(Match).filter(Match.id == match_id).first()

    if not match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Match not found")

    # Verify user is part of the match
    if match.user1_id != current_user.id and match.user2_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You are not part of this match"
        )

    # Get messages
    messages = (
        db.query(Message)
        .filter(Message.match_id == match_id)
        .order_by(Message.created_at.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return [MessageResponse.model_validate(m) for m in messages]


@router.put("/{message_id}/read", response_model=MessageResponse)
async def mark_as_read(
    message_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Mark a message as read."""
    message = db.query(Message).filter(Message.id == message_id).first()

    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")

    # Verify user is part of the match (but not the sender)
    match = db.query(Match).filter(Match.id == message.match_id).first()
    if not match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Match not found")

    # Verify user is part of the match but not the sender
    if match.user1_id != current_user.id and match.user2_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You are not part of this match"
        )

    if message.sender_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot mark your own message as read",
        )

    # Mark as read
    message.read = True
    from datetime import datetime

    message.read_at = datetime.utcnow()

    db.commit()
    db.refresh(message)

    return MessageResponse.model_validate(message)


@router.get("/unread/count")
async def get_unread_count(
    current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)
):
    """Get count of unread messages for the current user."""
    # Get all matches where user is involved
    matches = (
        db.query(Match)
        .filter(
            or_(Match.user1_id == current_user.id, Match.user2_id == current_user.id),
            Match.is_active == True,
            Match.unmatched == False,
        )
        .all()
    )

    match_ids = [m.id for m in matches]

    # Count unread messages where user is NOT the sender
    unread_count = (
        db.query(Message)
        .filter(
            Message.match_id.in_(match_ids),
            Message.sender_id != current_user.id,
            Message.read == False,
        )
        .count()
    )

    return {"unread_count": unread_count}
