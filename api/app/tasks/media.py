"""Media processing tasks."""
import json
from io import BytesIO
from PIL import Image
from typing import Optional
import boto3
from app.core.config import settings
from app.core.storage import s3_client, get_file_url, validate_file_type
import logging

logger = logging.getLogger(__name__)


def generate_thumbnail(object_key: str, max_size: tuple = (400, 400)) -> Optional[str]:
    """
    Generate a thumbnail for an image.
    
    Args:
        object_key: S3 object key of the source image
        max_size: Maximum size of the thumbnail (width, height)
    
    Returns:
        Object key of the thumbnail, or None if failed
    """
    try:
        # Download original image from S3
        response = s3_client.get_object(Bucket=settings.s3_bucket_name, Key=object_key)
        image_data = response['Body'].read()
        
        # Open and resize image
        image = Image.open(BytesIO(image_data))
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Save to buffer
        thumbnail_buffer = BytesIO()
        
        # Determine format
        file_ext = object_key.rsplit('.', 1)[-1].lower() if '.' in object_key else 'jpg'
        if file_ext not in ['jpg', 'jpeg', 'png']:
            format_type = 'JPEG'
        else:
            format_type = file_ext.upper()
        
        # Handle alpha channel for PNG
        if format_type == 'JPEG' and image.mode in ('RGBA', 'LA', 'P'):
            # Create white background
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
            image = background
        
        image.save(thumbnail_buffer, format_type, quality=85, optimize=True)
        thumbnail_buffer.seek(0)
        
        # Upload thumbnail to S3
        thumbnail_key = object_key.rsplit('.', 1)[0] + '_thumb.' + file_ext
        s3_client.put_object(
            Bucket=settings.s3_bucket_name,
            Key=thumbnail_key,
            Body=thumbnail_buffer.getvalue(),
            ContentType=response.get('ContentType', 'image/jpeg')
        )
        
        logger.info(f"Generated thumbnail: {thumbnail_key}")
        return thumbnail_key
        
    except Exception as e:
        logger.error(f"Error generating thumbnail for {object_key}: {e}")
        return None


def process_image_upload(object_key: str, update_profile: Optional[int] = None) -> dict:
    """
    Process an uploaded image (generate thumbnail, extract metadata).
    
    Args:
        object_key: S3 object key of the uploaded image
        update_profile: Profile ID to update with thumbnail reference
    
    Returns:
        Dict with processing results
    """
    try:
        # Generate thumbnail
        thumbnail_key = generate_thumbnail(object_key)
        
        result = {
            'original': object_key,
            'thumbnail': thumbnail_key,
            'status': 'success'
        }
        
        # If profile update requested, update it with thumbnail info
        if update_profile and thumbnail_key:
            # This would typically update the profile's media_refs
            # For now, just log it
            logger.info(f"Would update profile {update_profile} with thumbnail {thumbnail_key}")
        
        return result
        
    except Exception as e:
        logger.error(f"Error processing image {object_key}: {e}")
        return {
            'original': object_key,
            'status': 'error',
            'error': str(e)
        }


def validate_media_safety(object_key: str) -> dict:
    """
    Basic media safety validation.
    
    Args:
        object_key: S3 object key to validate
    
    Returns:
        Dict with validation results
    """
    try:
        # Get file metadata
        response = s3_client.head_object(Bucket=settings.s3_bucket_name, Key=object_key)
        content_type = response.get('ContentType', '')
        size = response.get('ContentLength', 0)
        
        # Basic validation
        is_safe = True
        flags = []
        
        # Check for suspicious file types
        suspicious_types = ['application/x-executable', 'application/x-sharedlib']
        if content_type in suspicious_types:
            is_safe = False
            flags.append('suspicious_file_type')
        
        # Check for extremely large files
        if size > 50 * 1024 * 1024:  # 50MB
            flags.append('file_too_large')
        
        # TODO: Add actual content safety checks (NSFW detection, etc.)
        
        return {
            'object_key': object_key,
            'is_safe': is_safe,
            'flags': flags,
            'content_type': content_type,
            'size': size
        }
        
    except Exception as e:
        logger.error(f"Error validating media {object_key}: {e}")
        return {
            'object_key': object_key,
            'is_safe': False,
            'flags': ['validation_error']
        }

