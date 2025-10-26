"""Listing endpoints for job postings."""

import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from decimal import Decimal

from app.core.database import get_db
from app.core.auth import get_current_active_user
from app.models.user import User
from app.models.listing import Listing, ListingStatus
from app.schemas.listing import (
    ListingCreate,
    ListingUpdate,
    ListingResponse,
    ListingCard,
    ListingFilter,
)

router = APIRouter(prefix="/listings", tags=["listings"])


def parse_json_field(field_value: str):
    """Parse JSON string field."""
    if field_value:
        try:
            return json.loads(field_value)
        except (json.JSONDecodeError, TypeError):
            return []
    return []


def serialize_json_field(field_value):
    """Serialize field to JSON string."""
    if field_value:
        return json.dumps(field_value)
    return None


@router.post("", response_model=ListingResponse, status_code=status.HTTP_201_CREATED)
async def create_listing(
    listing_data: ListingCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Create a new job listing."""
    # Only hirers and admins can create listings
    if current_user.role not in ["hirer", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Only hirers can create listings"
        )

    # Validate salary range
    if listing_data.salary_min and listing_data.salary_max:
        if listing_data.salary_min > listing_data.salary_max:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Minimum salary cannot be greater than maximum salary",
            )

    # Create listing
    new_listing = Listing(
        user_id=current_user.id,
        title=listing_data.title,
        company=listing_data.company,
        description=listing_data.description,
        skills_required=serialize_json_field(listing_data.skills_required),
        location=listing_data.location,
        remote_preference=listing_data.remote_preference,
        salary_min=listing_data.salary_min,
        salary_max=listing_data.salary_max,
        hourly_rate=listing_data.hourly_rate,
        equity_offered=listing_data.equity_offered or False,
        media_refs=serialize_json_field(listing_data.media_refs or {}),
        status=listing_data.status,
    )

    db.add(new_listing)
    db.commit()
    db.refresh(new_listing)

    # Parse JSON fields for response
    listing_dict = {
        **{k: v for k, v in new_listing.__dict__.items() if not k.startswith("_")},
        "skills_required": parse_json_field(new_listing.skills_required),
        "media_refs": parse_json_field(new_listing.media_refs or "{}"),
    }

    return ListingResponse(**listing_dict)


@router.get("", response_model=List[ListingCard])
async def get_listings(
    status_filter: Optional[ListingStatus] = Query(None, alias="status"),
    skills: Optional[str] = Query(None, description="Comma-separated list of skills"),
    location: Optional[str] = None,
    remote_preference: Optional[str] = Query(None, pattern="^(remote|onsite|hybrid)$"),
    min_salary: Optional[Decimal] = Query(None, ge=0),
    max_salary: Optional[Decimal] = Query(None, ge=0),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Get listings with optional filters."""
    query = db.query(Listing).filter(Listing.is_active == True)

    # Apply filters
    if status_filter:
        query = query.filter(Listing.status == status_filter)
    else:
        query = query.filter(Listing.status == ListingStatus.ACTIVE)

    if location:
        query = query.filter(Listing.location.ilike(f"%{location}%"))

    if remote_preference:
        query = query.filter(Listing.remote_preference == remote_preference)

    if min_salary:
        query = query.filter(
            or_(
                Listing.salary_max >= min_salary,
                Listing.hourly_rate * 40 * 50 >= min_salary,  # Approximate annual from hourly
            )
        )

    if max_salary:
        query = query.filter(
            or_(Listing.salary_min <= max_salary, Listing.hourly_rate * 40 * 50 <= max_salary)
        )

    # Skills filter - check if any of the required skills match
    if skills:
        skills_list = [s.strip() for s in skills.split(",")]
        skill_conditions = []
        for skill in skills_list:
            skill_conditions.append(Listing.skills_required.ilike(f"%{skill}%"))
        query = query.filter(or_(*skill_conditions))

    # Order by boosted first, then by created_at desc
    listings = (
        query.order_by(Listing.is_boosted.desc(), Listing.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    # Parse JSON fields
    result = []
    for listing in listings:
        listing_dict = {
            "id": listing.id,
            "title": listing.title,
            "company": listing.company,
            "location": listing.location,
            "remote_preference": listing.remote_preference,
            "skills_required": parse_json_field(listing.skills_required),
            "hourly_rate": listing.hourly_rate,
            "salary_min": listing.salary_min,
            "salary_max": listing.salary_max,
            "created_at": listing.created_at,
            "is_boosted": listing.is_boosted,
        }
        result.append(ListingCard(**listing_dict))

    return result


@router.get("/my-listings", response_model=List[ListingResponse])
async def get_my_listings(
    current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)
):
    """Get current user's listings."""
    listings = db.query(Listing).filter(Listing.user_id == current_user.id).all()

    result = []
    for listing in listings:
        listing_dict = {
            **{k: v for k, v in listing.__dict__.items() if not k.startswith("_")},
            "skills_required": parse_json_field(listing.skills_required),
            "media_refs": parse_json_field(listing.media_refs or "{}"),
        }
        result.append(ListingResponse(**listing_dict))

    return result


@router.get("/{listing_id}", response_model=ListingResponse)
async def get_listing(listing_id: int, db: Session = Depends(get_db)):
    """Get a specific listing by ID."""
    listing = db.query(Listing).filter(Listing.id == listing_id).first()

    if not listing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing not found")

    listing_dict = {
        **{k: v for k, v in listing.__dict__.items() if not k.startswith("_")},
        "skills_required": parse_json_field(listing.skills_required),
        "media_refs": parse_json_field(listing.media_refs or "{}"),
    }

    return ListingResponse(**listing_dict)


@router.put("/{listing_id}", response_model=ListingResponse)
async def update_listing(
    listing_id: int,
    listing_data: ListingUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Update a listing."""
    listing = db.query(Listing).filter(Listing.id == listing_id).first()

    if not listing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing not found")

    # Check ownership or admin
    if listing.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this listing",
        )

    # Update fields
    update_data = listing_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        if key == "skills_required" and value is not None:
            setattr(listing, key, serialize_json_field(value))
        elif key == "media_refs" and value is not None:
            setattr(listing, key, serialize_json_field(value))
        else:
            setattr(listing, key, value)

    # Validate salary range if both provided
    if listing.salary_min and listing.salary_max:
        if listing.salary_min > listing.salary_max:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Minimum salary cannot be greater than maximum salary",
            )

    db.commit()
    db.refresh(listing)

    listing_dict = {
        **{k: v for k, v in listing.__dict__.items() if not k.startswith("_")},
        "skills_required": parse_json_field(listing.skills_required),
        "media_refs": parse_json_field(listing.media_refs or "{}"),
    }

    return ListingResponse(**listing_dict)


@router.delete("/{listing_id}", status_code=status.HTTP_200_OK)
async def delete_listing(
    listing_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Delete a listing."""
    listing = db.query(Listing).filter(Listing.id == listing_id).first()

    if not listing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing not found")

    # Check ownership or admin
    if listing.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this listing",
        )

    db.delete(listing)
    db.commit()

    return {"message": "Listing deleted successfully", "listing_id": listing_id}
