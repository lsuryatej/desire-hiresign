"""Storage utilities for MinIO/S3."""
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from fastapi import HTTPException, status
from typing import Optional
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Initialize S3 client
s3_client = boto3.client(
    's3',
    endpoint_url=settings.minio_endpoint,
    aws_access_key_id=settings.minio_access_key,
    aws_secret_access_key=settings.minio_secret_key,
    config=Config(signature_version='s3v4'),
    region_name='us-east-1'
)

# Allowed file types and max sizes
ALLOWED_IMAGE_TYPES = {'image/jpeg', 'image/png', 'image/gif', 'image/webp'}
ALLOWED_DOC_TYPES = {'application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'}
ALLOWED_VIDEO_TYPES = {'video/mp4', 'video/webm'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


def validate_file_type(content_type: str, file_type: str = 'image') -> bool:
    """Validate file type."""
    if file_type == 'image':
        return content_type in ALLOWED_IMAGE_TYPES
    elif file_type == 'document':
        return content_type in ALLOWED_DOC_TYPES
    elif file_type == 'video':
        return content_type in ALLOWED_VIDEO_TYPES
    return False


def generate_presigned_url(
    object_key: str,
    expiration: int = 3600,
    http_method: str = 'PUT'
) -> Optional[str]:
    """
    Generate a presigned URL for uploading/downloading files.
    
    Args:
        object_key: The S3 object key (file path)
        expiration: URL expiration time in seconds (default: 1 hour)
        http_method: HTTP method for the presigned URL (PUT for upload, GET for download)
    
    Returns:
        Presigned URL or None if error
    """
    try:
        if http_method == 'PUT':
            url = s3_client.generate_presigned_url(
                'put_object',
                Params={
                    'Bucket': settings.s3_bucket_name,
                    'Key': object_key,
                    'ContentType': 'application/octet-stream'
                },
                ExpiresIn=expiration
            )
        else:  # GET
            url = s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': settings.s3_bucket_name,
                    'Key': object_key
                },
                ExpiresIn=expiration
            )
        return url
    except ClientError as e:
        logger.error(f"Error generating presigned URL: {e}")
        return None


def delete_file(object_key: str) -> bool:
    """
    Delete a file from S3.
    
    Args:
        object_key: The S3 object key (file path)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        s3_client.delete_object(
            Bucket=settings.s3_bucket_name,
            Key=object_key
        )
        return True
    except ClientError as e:
        logger.error(f"Error deleting file: {e}")
        return False


def get_file_url(object_key: str, expiration: int = 3600) -> str:
    """
    Get a temporary URL to access a file.
    
    Args:
        object_key: The S3 object key (file path)
        expiration: URL expiration time in seconds (default: 1 hour)
    
    Returns:
        Presigned GET URL
    """
    return generate_presigned_url(object_key, expiration=expiration, http_method='GET')


def ensure_bucket_exists():
    """Ensure the S3 bucket exists, create if not."""
    try:
        s3_client.head_bucket(Bucket=settings.s3_bucket_name)
        logger.info(f"Bucket {settings.s3_bucket_name} exists")
    except ClientError:
        # Bucket doesn't exist, create it
        try:
            s3_client.create_bucket(Bucket=settings.s3_bucket_name)
            logger.info(f"Created bucket {settings.s3_bucket_name}")
        except ClientError as e:
            logger.error(f"Error creating bucket: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create storage bucket"
            )


# Ensure bucket exists on module import
try:
    ensure_bucket_exists()
except Exception as e:
    logger.warning(f"Could not ensure bucket exists: {e}")
