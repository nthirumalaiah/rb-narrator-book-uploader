"""
Upload routes for S3 multipart upload functionality.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from services.s3_service import S3ServiceInterface, AWSS3Service
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


# Create router instance
router = APIRouter(
    prefix="/upload",
    tags=["uploads"],
    dependencies=[],
    responses={
        500: {"description": "Upload service error"},
        400: {"description": "Invalid request"}
    },
)


def get_s3_service() -> S3ServiceInterface:
    """Dependency provider for S3 service"""
    return AWSS3Service()


@router.post(
    "/initiate",
    response_model=InitiateUploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Initiate multipart upload",
    description="Start a new multipart upload to S3"
)
async def initiate_upload(
    request: InitiateUploadRequest,
    s3_service: S3ServiceInterface = Depends(get_s3_service)
) -> InitiateUploadResponse:
    """
    Initiate a multipart upload to S3.
    
    - **filename**: Name of the file to upload
    - **content_type**: MIME type of the file (default: audio/mpeg)
    
    Returns upload_id and key for subsequent operations.
    """
    try:
        return await s3_service.initiate_multipart_upload(request)
    except BaseApplicationException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initiate upload: {str(e)}"
        )


@router.post(
    "/presign-part",
    response_model=PresignedPartResponse,
    summary="Generate presigned URL for upload part",
    description="Get a presigned URL for uploading a specific part"
)
async def get_presigned_url(
    request: PresignedPartRequest,
    s3_service: S3ServiceInterface = Depends(get_s3_service)
) -> PresignedPartResponse:
    """
    Generate a presigned URL for uploading a part.
    
    - **key**: The S3 key from initiate response
    - **upload_id**: The upload ID from initiate response
    - **part_number**: Part number (1-10000)
    - **expires_in**: URL expiration time in seconds (default: 3600)
    """
    try:
        return await s3_service.generate_presigned_url(request)
    except BaseApplicationException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate presigned URL: {str(e)}"
        )


@router.post(
    "/complete",
    response_model=CompleteUploadResponse,
    summary="Complete multipart upload",
    description="Complete the multipart upload by combining all parts"
)
async def complete_upload(
    request: CompleteUploadRequest,
    s3_service: S3ServiceInterface = Depends(get_s3_service)
) -> CompleteUploadResponse:
    """
    Complete the multipart upload.
    
    - **key**: The S3 key from initiate response
    - **upload_id**: The upload ID from initiate response
    - **parts**: List of uploaded parts with ETag and PartNumber
    """
    try:
        return await s3_service.complete_multipart_upload(request)
    except BaseApplicationException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to complete upload: {str(e)}"
        )


@router.post(
    "/abort",
    response_model=AbortUploadResponse,
    summary="Abort multipart upload",
    description="Cancel the multipart upload and clean up"
)
async def abort_upload(
    request: AbortUploadRequest,
    s3_service: S3ServiceInterface = Depends(get_s3_service)
) -> AbortUploadResponse:
    """
    Abort the multipart upload.
    
    - **key**: The S3 key from initiate response
    - **upload_id**: The upload ID from initiate response
    """
    try:
        return await s3_service.abort_multipart_upload(request)
    except BaseApplicationException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to abort upload: {str(e)}"
        )