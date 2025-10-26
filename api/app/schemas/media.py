"""Media upload schemas."""
from pydantic import BaseModel, Field
from typing import Optional, Literal


class SignedUrlRequest(BaseModel):
    """Request for generating a signed URL."""
    file_name: str = Field(..., description="Original file name")
    content_type: str = Field(..., description="MIME type of the file")
    file_type: Literal["image", "document", "video"] = Field(
        default="image",
        description="Type of file (image, document, video)"
    )
    file_size: int = Field(..., ge=1, le=10485760, description="File size in bytes (max 10MB)")


class SignedUrlResponse(BaseModel):
    """Response containing signed upload URL."""
    upload_url: str = Field(..., description="Presigned URL for uploading")
    object_key: str = Field(..., description="S3 object key (file path)")
    download_url: str = Field(..., description="Presigned URL for downloading")
    expires_in: int = Field(default=3600, description="URL expiration time in seconds")


class FileInfo(BaseModel):
    """File information."""
    object_key: str
    file_name: str
    content_type: str
    file_size: int
    url: str


class DeleteFileRequest(BaseModel):
    """Request to delete a file."""
    object_key: str
