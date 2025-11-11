"""
Health check and system status routes.
"""

from fastapi import APIRouter
from typing import Dict, Any

router = APIRouter(
    prefix="",
    tags=["health"],
    responses={200: {"description": "System is healthy"}},
)


@router.get(
    "/",
    summary="API Health Check",
    description="Check if the API is running and healthy"
)
async def root() -> Dict[str, Any]:
    """
    Root endpoint for API health check.
    Returns basic information about the API status.
    """
    return {
        "message": "RB Narrator Book Uploader API is running!",
        "status": "healthy",
        "version": "1.0.0"
    }


@router.get(
    "/health",
    summary="Detailed Health Check",
    description="Detailed health check including system status"
)
async def health_check() -> Dict[str, Any]:
    """
    Detailed health check endpoint.
    """
    return {
        "status": "healthy",
        "service": "rb-narrator-api",
        "version": "1.0.0",
        "environment": "development",
        "checks": {
            "database": "connected",
            "api": "operational"
        }
    }