"""
S3 upload schemas for multipart upload functionality with comprehensive validation.
"""

from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Optional
import re


class InitiateUploadRequest(BaseModel):
    """Request model for initiating multipart upload with validation"""
    filename: str = Field(..., min_length=1, max_length=255, description="Name of the file to upload")
    content_type: str = Field("audio/mpeg", description="MIME type of the file")

    @validator('filename')
    def validate_filename(cls, v: str) -> str:
        # Remove any path separators for security
        filename = v.split('/')[-1].split('\\')[-1]
        if not filename.strip():
            raise ValueError('Filename cannot be empty')
        # Check for valid characters (basic validation)
        if not re.match(r'^[a-zA-Z0-9._-]+$', filename):
            raise ValueError('Filename contains invalid characters. Use only letters, numbers, dots, hyphens, and underscores.')
        return filename

    @validator('content_type')
    def validate_content_type(cls, v: str) -> str:
        allowed_types = [
            'audio/mpeg', 'audio/mp3', 'audio/wav', 'audio/aac', 
            'audio/ogg', 'audio/flac', 'audio/m4a'
        ]
        if v not in allowed_types:
            raise ValueError(f'Content type must be one of: {", ".join(allowed_types)}')
        return v

    class Config:
        schema_extra = {
            "example": {
                "filename": "chapter1.mp3",
                "content_type": "audio/mpeg"
            }
        }


class InitiateUploadResponse(BaseModel):
    """Response model for multipart upload initiation"""
    upload_id: str = Field(..., description="Unique upload identifier")
    key: str = Field(..., description="S3 object key")
    bucket: str = Field(..., description="S3 bucket name")

    class Config:
        schema_extra = {
            "example": {
                "upload_id": "abc123-def456-ghi789",
                "key": "uploads/chapter1.mp3",
                "bucket": "my-audio-bucket"
            }
        }


class PresignedPartRequest(BaseModel):
    """Request model for generating presigned URL for upload part"""
    key: str = Field(..., min_length=1, description="S3 object key")
    upload_id: str = Field(..., min_length=1, description="Upload identifier")
    part_number: int = Field(..., ge=1, le=10000, description="Part number (1-10000)")
    expires_in: int = Field(3600, ge=60, le=604800, description="URL expiration time in seconds (1 min - 7 days)")

    class Config:
        schema_extra = {
            "example": {
                "key": "uploads/chapter1.mp3",
                "upload_id": "abc123-def456-ghi789",
                "part_number": 1,
                "expires_in": 3600
            }
        }


class PresignedPartResponse(BaseModel):
    """Response model for presigned URL"""
    presigned_url: str = Field(..., description="Pre-signed URL for uploading")
    part_number: int = Field(..., description="Part number")
    expires_at: Optional[str] = Field(None, description="URL expiration timestamp")

    class Config:
        schema_extra = {
            "example": {
                "presigned_url": "https://s3.amazonaws.com/bucket/key?signature=...",
                "part_number": 1,
                "expires_at": "2023-01-01T13:00:00Z"
            }
        }


class UploadPart(BaseModel):
    """Model for upload part information with validation"""
    ETag: str = Field(..., min_length=1, description="ETag returned from S3 upload")
    PartNumber: int = Field(..., ge=1, le=10000, description="Part number")

    @validator('ETag')
    def validate_etag(cls, v: str) -> str:
        # Remove quotes if present and validate format
        etag = v.strip().strip('"')
        if not re.match(r'^[a-fA-F0-9]{32}(-\d+)?$', etag):
            raise ValueError('Invalid ETag format')
        return f'"{etag}"'  # Ensure quotes are present

    class Config:
        schema_extra = {
            "example": {
                "ETag": "\"d41d8cd98f00b204e9800998ecf8427e\"",
                "PartNumber": 1
            }
        }


class CompleteUploadRequest(BaseModel):
    """Request model for completing multipart upload"""
    key: str = Field(..., min_length=1, description="S3 object key")
    upload_id: str = Field(..., min_length=1, description="Upload identifier")
    parts: List[UploadPart] = Field(..., min_items=1, description="List of uploaded parts")

    @validator('parts')
    def validate_parts_sequence(cls, v: List[UploadPart]) -> List[UploadPart]:
        # Ensure parts are in sequential order
        part_numbers = [part.PartNumber for part in v]
        if part_numbers != list(range(1, len(part_numbers) + 1)):
            raise ValueError('Parts must be sequential starting from 1')
        return v

    class Config:
        schema_extra = {
            "example": {
                "key": "uploads/chapter1.mp3",
                "upload_id": "abc123-def456-ghi789",
                "parts": [
                    {"ETag": "\"d41d8cd98f00b204e9800998ecf8427e\"", "PartNumber": 1},
                    {"ETag": "\"098f6bcd4621d373cade4e832627b4f6\"", "PartNumber": 2}
                ]
            }
        }


class CompleteUploadResponse(BaseModel):
    """Response model for completed upload"""
    location: str = Field(..., description="URL of the uploaded object")
    bucket: str = Field(..., description="S3 bucket name")
    key: str = Field(..., description="S3 object key")
    etag: str = Field(..., description="Final ETag of the object")
    size: Optional[int] = Field(None, description="Size of the uploaded file in bytes")

    class Config:
        schema_extra = {
            "example": {
                "location": "https://my-bucket.s3.amazonaws.com/uploads/chapter1.mp3",
                "bucket": "my-audio-bucket",
                "key": "uploads/chapter1.mp3",
                "etag": "\"d41d8cd98f00b204e9800998ecf8427e\"",
                "size": 1048576
            }
        }


class AbortUploadRequest(BaseModel):
    """Request model for aborting multipart upload"""
    key: str = Field(..., min_length=1, description="S3 object key")
    upload_id: str = Field(..., min_length=1, description="Upload identifier")

    class Config:
        schema_extra = {
            "example": {
                "key": "uploads/chapter1.mp3",
                "upload_id": "abc123-def456-ghi789"
            }
        }


class AbortUploadResponse(BaseModel):
    """Response model for aborted upload"""
    status: str = Field(..., description="Operation status")
    message: str = Field(..., description="Descriptive message")
    upload_id: str = Field(..., description="Upload identifier that was aborted")

    class Config:
        schema_extra = {
            "example": {
                "status": "aborted",
                "message": "Upload successfully aborted",
                "upload_id": "abc123-def456-ghi789"
            }
        }