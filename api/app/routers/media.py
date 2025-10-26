"""Media upload endpoints."""

import secrets
import hashlib
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.storage import (
    generate_presigned_url,
    validate_file_type,
    delete_file,
    get_file_url,
    MAX_FILE_SIZE,
)
from app.core.auth import get_current_active_user
from app.models.user import User
from app.schemas.media import SignedUrlRequest, SignedUrlResponse, DeleteFileRequest
from app.worker import task_queue

# Import tasks to make them available
from app.tasks import media as media_tasks

router = APIRouter(prefix="/media", tags=["media"])


def generate_object_key(user_id: int, file_name: str, file_type: str) -> str:
    """
    Generate a unique S3 object key for a file.

    Args:
        user_id: User ID
        file_name: Original file name
        file_type: Type of file (image, document, video)

    Returns:
        Object key (file path)
    """
    # Generate a unique hash for the file
    timestamp = datetime.utcnow().strftime("%Y%m%d")
    random_hash = secrets.token_hex(8)

    # Get file extension
    file_ext = file_name.rsplit(".", 1)[-1] if "." in file_name else ""

    # Generate object key: file_type/user_id/date/hash.ext
    object_key = f"{file_type}/{user_id}/{timestamp}/{random_hash}"
    if file_ext:
        object_key += f".{file_ext}"

    return object_key


@router.post("/signed-url", response_model=SignedUrlResponse, status_code=status.HTTP_201_CREATED)
async def get_signed_upload_url(
    request: SignedUrlRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Generate a presigned URL for uploading a file to S3.

    The client should:
    1. Call this endpoint to get a presigned URL
    2. Upload the file directly to S3 using the presigned URL
    3. Store the object_key in the profile/listing media_refs field
    """
    # Validate file type
    if not validate_file_type(request.content_type, request.file_type):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type {request.content_type} not allowed for {request.file_type}",
        )

    # Validate file size
    if request.file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds maximum allowed size of {MAX_FILE_SIZE / 1024 / 1024}MB",
        )

    # Generate unique object key
    object_key = generate_object_key(current_user.id, request.file_name, request.file_type)

    # Generate presigned upload URL (1 hour expiration)
    upload_url = generate_presigned_url(object_key=object_key, expiration=3600, http_method="PUT")

    if not upload_url:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate upload URL",
        )

    # Generate presigned download URL
    download_url = generate_presigned_url(object_key=object_key, expiration=3600, http_method="GET")

    return SignedUrlResponse(
        upload_url=upload_url, object_key=object_key, download_url=download_url, expires_in=3600
    )


@router.post("/delete", status_code=status.HTTP_200_OK)
async def delete_file_endpoint(
    request: DeleteFileRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Delete a file from S3.

    Note: Only the file owner (based on object_key user_id) can delete.
    """
    # Parse user_id from object_key to verify ownership
    # object_key format: file_type/user_id/date/hash.ext
    try:
        parts = request.object_key.split("/")
        if len(parts) < 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid object_key format"
            )

        file_user_id = int(parts[1])

        # Verify ownership
        if file_user_id != current_user.id and current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to delete this file",
            )

        # Delete the file
        success = delete_file(request.object_key)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete file"
            )

        return {"message": "File deleted successfully", "object_key": request.object_key}

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid object_key format"
        )


@router.get("/url/{object_key:path}", status_code=status.HTTP_200_OK)
async def get_file_url_endpoint(
    object_key: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Get a presigned URL to access/download a file.

    Note: Files are generally publicly accessible via presigned URLs,
    but authenticated users can generate fresh URLs.
    """
    url = get_file_url(object_key, expiration=3600)

    if not url:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to generate file URL"
        )

    return {"url": url, "object_key": object_key, "expires_in": 3600}


@router.post("/process", status_code=status.HTTP_202_ACCEPTED)
async def process_image(
    object_key: str,
    profile_id: int = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Process an uploaded image (generate thumbnail, validate safety).

    This endpoint enqueues a background job to:
    1. Generate a thumbnail for the image
    2. Validate media safety
    3. Update profile if profile_id provided
    """
    # Verify ownership
    parts = object_key.split("/")
    if len(parts) >= 2:
        file_user_id = int(parts[1])
        if file_user_id != current_user.id and current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to process this file",
            )

    # Enqueue processing job
    try:
        # Check if file is an image by extension
        file_ext = object_key.split(".")[-1].lower()
        if file_ext not in ["jpg", "jpeg", "png", "gif", "webp"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only images can be processed for thumbnails",
            )

        job = task_queue.enqueue(
            media_tasks.process_image_upload, object_key, update_profile=profile_id
        )

        return {
            "message": "Image processing job enqueued",
            "job_id": job.id,
            "object_key": object_key,
            "status": "pending",
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to enqueue processing job: {str(e)}",
        )
