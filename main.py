"""
Main application entry point.
"""

from typing import Dict, Any
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.db import Base, engine
from api.routes.upload_routes import router as upload_router
from api.routes.chapter_routes import router as chapter_router
from api.routes.health_routes import router as health_router
import logging
import os

# Configure logging with proper typing
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger: logging.Logger = logging.getLogger(__name__)


def create_application() -> FastAPI:
    """
    Application factory function following Dependency Inversion Principle.
    Creates and configures the FastAPI application.
    """
    
    # Create FastAPI application with metadata
    app = FastAPI(
        title="RB Narrator Book Uploader API",
        description="API for managing book chapters and audio uploads",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        contact={
            "name": "RB Narrator Team",
            "email": "support@rbnarrator.com",
        },
        license_info={
            "name": "RB Media",
        }
    )
    
    # Configure CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure properly for production
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"],
        allow_headers=["*"],
    )
    
    # Create database tables (Infrastructure setup)
    Base.metadata.create_all(bind=engine)
    
    # Include routers
    app.include_router(health_router, tags=["health"])
    app.include_router(upload_router, tags=["uploads"])
    app.include_router(chapter_router, tags=["chapters"])
    
    # Add startup and shutdown event handlers
    @app.on_event("startup")
    async def startup_event() -> None:
        """Application startup tasks"""
        environment: str = os.getenv("ENVIRONMENT", "development")
        logger.info("🚀 Starting RB Narrator Book Uploader API v1.0.0")
        logger.info("📊 Database connection established")
        logger.info("🌐 Environment: %s", environment)
        logger.info("📚 API Documentation available at /docs")

    @app.on_event("shutdown")
    async def shutdown_event() -> None:
        """Application shutdown tasks"""
        logger.info("👋 Shutting down RB Narrator Book Uploader API...")
    
    return app


# Create application instance
app = create_application()


# Development server runner
if __name__ == "__main__":
    import uvicorn
    
    # Get configuration from environment variables with proper typing
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    debug: bool = os.getenv("DEBUG", "true").lower() == "true"
    
    logger.info("Starting development server...")
    logger.info("Server will run at: http://%s:%s", host, port)
    logger.info("API Documentation: http://%s:%s/docs", host, port)
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info" if not debug else "debug",
        access_log=True
    )

