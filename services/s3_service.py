"""
S3 service for handling file uploads following SOLID principles.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
import boto3
import uuid
import os
from botocore.exceptions import ClientError

from schemas.upload import (
    InitiateUploadRequest,
    InitiateUploadResponse,
    PresignedPartRequest,
    PresignedPartResponse,
    CompleteUploadRequest,
    CompleteUploadResponse,
    AbortUploadRequest,
    AbortUploadResponse
)
from exceptions.base_exceptions import BaseApplicationException


class S3ServiceInterface(ABC):
    """Abstract interface for S3 service operations"""
    
    @abstractmethod
    async def initiate_multipart_upload(self, request: InitiateUploadRequest) -> InitiateUploadResponse:
        """Initiate a multipart upload"""
        ...
    
    @abstractmethod
    async def generate_presigned_url(self, request: PresignedPartRequest) -> PresignedPartResponse:
        """Generate presigned URL for upload part"""
        ...
    
    @abstractmethod
    async def complete_multipart_upload(self, request: CompleteUploadRequest) -> CompleteUploadResponse:
        """Complete multipart upload"""
        ...
    
    @abstractmethod
    async def abort_multipart_upload(self, request: AbortUploadRequest) -> AbortUploadResponse:
        """Abort multipart upload"""
        ...


class S3UploadError(BaseApplicationException):
    """Custom exception for S3 upload errors"""
    pass


class AWSS3Service(S3ServiceInterface):
    """AWS S3 implementation of S3 service"""
    
    def __init__(self):
        """Initialize AWS S3 client"""
        self.region = os.getenv("AWS_REGION", "us-west-2")
        self.bucket = os.getenv("S3_BUCKET")
        
        if not self.bucket:
            raise S3UploadError("S3_BUCKET environment variable is required")
        
        try:
            self.s3_client = boto3.client("s3", region_name=self.region)
        except Exception as e:
            raise S3UploadError(f"Failed to initialize S3 client: {str(e)}")
    
    async def initiate_multipart_upload(self, request: InitiateUploadRequest) -> InitiateUploadResponse:
        """Initiate a multipart upload"""
        try:
            # Generate unique key for the upload
            key = f"uploads/{uuid.uuid4()}-{request.filename}"
            
            # Create multipart upload
            response = self.s3_client.create_multipart_upload(
                Bucket=self.bucket,
                Key=key,
                ContentType=request.content_type,
                Metadata={
                    "original_filename": request.filename,
                    "upload_timestamp": str(uuid.uuid4())
                }
            )
            
            return InitiateUploadResponse(
                upload_id=response["UploadId"],
                key=key,
                bucket=self.bucket
            )
        except ClientError as e:
            raise S3UploadError(f"Failed to initiate multipart upload: {str(e)}")
        except Exception as e:
            raise S3UploadError(f"Unexpected error during upload initiation: {str(e)}")
    
    async def generate_presigned_url(self, request: PresignedPartRequest) -> PresignedPartResponse:
        """Generate presigned URL for upload part"""
        try:
            url = self.s3_client.generate_presigned_url(
                ClientMethod="upload_part",
                Params={
                    "Bucket": self.bucket,
                    "Key": request.key,
                    "UploadId": request.upload_id,
                    "PartNumber": request.part_number,
                },
                ExpiresIn=request.expires_in
            )
            
            return PresignedPartResponse(
                presigned_url=url,
                part_number=request.part_number
            )
        except ClientError as e:
            raise S3UploadError(f"Failed to generate presigned URL: {str(e)}")
        except Exception as e:
            raise S3UploadError(f"Unexpected error generating presigned URL: {str(e)}")
    
    async def complete_multipart_upload(self, request: CompleteUploadRequest) -> CompleteUploadResponse:
        """Complete multipart upload"""
        try:
            # Format parts for AWS API
            parts_formatted = [
                {"ETag": part.ETag, "PartNumber": part.PartNumber}
                for part in request.parts
            ]
            
            response = self.s3_client.complete_multipart_upload(
                Bucket=self.bucket,
                Key=request.key,
                UploadId=request.upload_id,
                MultipartUpload={"Parts": parts_formatted}
            )
            
            return CompleteUploadResponse(
                location=response["Location"],
                bucket=self.bucket,
                key=request.key,
                etag=response["ETag"]
            )
        except ClientError as e:
            raise S3UploadError(f"Failed to complete multipart upload: {str(e)}")
        except Exception as e:
            raise S3UploadError(f"Unexpected error completing upload: {str(e)}")
    
    async def abort_multipart_upload(self, request: AbortUploadRequest) -> AbortUploadResponse:
        """Abort multipart upload"""
        try:
            self.s3_client.abort_multipart_upload(
                Bucket=self.bucket,
                Key=request.key,
                UploadId=request.upload_id
            )
            
            return AbortUploadResponse(
                status="aborted",
                message=f"Upload {request.upload_id} has been successfully aborted"
            )
        except ClientError as e:
            raise S3UploadError(f"Failed to abort multipart upload: {str(e)}")
        except Exception as e:
            raise S3UploadError(f"Unexpected error aborting upload: {str(e)}")