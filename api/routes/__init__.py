# API Routes package
from .chapter_routes import router as chapter_router
from .health_routes import router as health_router
from .upload_routes import router as upload_router

__all__ = ["chapter_router", "health_router", "upload_router"]