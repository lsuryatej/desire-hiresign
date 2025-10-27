"""Report endpoints for content moderation."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import get_db
from app.core.auth import get_current_active_user
from app.models.user import User, UserRole
from app.models.report import Report, ReportStatus, ReportType
from app.schemas.report import ReportCreate, ReportResponse, ReportUpdate

router = APIRouter(prefix="/reports", tags=["reports"])


def require_admin(current_user: User = Depends(get_current_active_user)) -> User:
    """Dependency to ensure user is admin."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return current_user


@router.post("", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
async def create_report(
    report_data: ReportCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Create a new report."""
    # Validate report type
    try:
        report_type = ReportType(report_data.report_type)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid report type. Must be one of: {[e.value for e in ReportType]}",
        )

    # Create report
    new_report = Report(
        reporter_id=current_user.id,
        report_type=report_type,
        target_id=report_data.target_id,
        reason=report_data.reason,
        description=report_data.description,
    )

    db.add(new_report)
    db.commit()
    db.refresh(new_report)

    return ReportResponse.model_validate(new_report)


@router.get("/my-reports", response_model=List[ReportResponse])
async def get_my_reports(
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get current user's reports."""
    reports = (
        db.query(Report)
        .filter(Report.reporter_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return [ReportResponse.model_validate(r) for r in reports]


@router.get("/pending", response_model=List[ReportResponse])
async def get_pending_reports(
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Get all pending reports (admin only)."""
    reports = (
        db.query(Report)
        .filter(Report.status == ReportStatus.PENDING)
        .order_by(Report.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return [ReportResponse.model_validate(r) for r in reports]


@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(
    report_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get a specific report."""
    report = db.query(Report).filter(Report.id == report_id).first()

    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")

    # Users can only see their own reports unless they're admin
    if report.reporter_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    return ReportResponse.model_validate(report)


@router.put("/{report_id}/review", response_model=ReportResponse)
async def review_report(
    report_id: int,
    review_data: ReportUpdate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Review a report (admin only)."""
    report = db.query(Report).filter(Report.id == report_id).first()

    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")

    # Validate status
    try:
        new_status = ReportStatus(review_data.status)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of: {[e.value for e in ReportStatus]}",
        )

    # Update report
    report.status = new_status
    report.reviewed_by = current_user.id
    report.review_notes = review_data.review_notes
    report.reviewed_at = datetime.utcnow()

    db.commit()
    db.refresh(report)

    return ReportResponse.model_validate(report)


@router.get("/stats/overview")
async def get_report_stats(
    current_user: User = Depends(require_admin), db: Session = Depends(get_db)
):
    """Get report statistics (admin only)."""
    total_reports = db.query(Report).count()
    pending_reports = db.query(Report).filter(Report.status == ReportStatus.PENDING).count()
    reviewed_reports = db.query(Report).filter(Report.status == ReportStatus.REVIEWED).count()
    resolved_reports = db.query(Report).filter(Report.status == ReportStatus.RESOLVED).count()

    return {
        "total_reports": total_reports,
        "pending_reports": pending_reports,
        "reviewed_reports": reviewed_reports,
        "resolved_reports": resolved_reports,
    }
