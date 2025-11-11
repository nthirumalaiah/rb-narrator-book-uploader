"""
Global exception handlers for the FastAPI application.
Follows Open/Closed Principle - new handlers can be added without modifying existing ones.
"""

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import http_exception_handler
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import SQLAlchemyError
import logging

from exceptions.base_exceptions import (
    BaseApplicationException,
    ValidationError,
    BusinessRuleError,
    NotFoundError,
    DatabaseError
)

# Configure logger
logger = logging.getLogger(__name__)


async def base_application_exception_handler(request: Request, exc: BaseApplicationException) -> JSONResponse:
    """Handle all application-specific exceptions"""
    logger.error(f"Application exception: {exc.message}", exc_info=exc)
    
    return JSONResponse(
        status_code=400,
        content={
            "error": {
                "code": exc.error_code,
                "message": exc.message,
                "type": "application_error"
            }
        }
    )


async def validation_error_handler(request: Request, exc: ValidationError) -> JSONResponse:
    """Handle validation errors"""
    logger.warning(f"Validation error: {exc.message}")
    
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": exc.error_code,
                "message": exc.message,
                "type": "validation_error"
            }
        }
    )


async def business_rule_error_handler(request: Request, exc: BusinessRuleError) -> JSONResponse:
    """Handle business rule violations"""
    logger.warning(f"Business rule violation: {exc.message}")
    
    return JSONResponse(
        status_code=409,
        content={
            "error": {
                "code": exc.error_code,
                "message": exc.message,
                "type": "business_rule_error"
            }
        }
    )


async def not_found_error_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    """Handle not found errors"""
    logger.info(f"Resource not found: {exc.message}")
    
    return JSONResponse(
        status_code=404,
        content={
            "error": {
                "code": exc.error_code,
                "message": exc.message,
                "type": "not_found_error"
            }
        }
    )


async def database_error_handler(request: Request, exc: DatabaseError) -> JSONResponse:
    """Handle database errors"""
    logger.error(f"Database error: {exc.message}", exc_info=exc)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": exc.error_code,
                "message": "An internal database error occurred",
                "type": "database_error"
            }
        }
    )


async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """Handle SQLAlchemy errors"""
    logger.error(f"SQLAlchemy error: {str(exc)}", exc_info=exc)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "DATABASE_ERROR",
                "message": "A database error occurred",
                "type": "sqlalchemy_error"
            }
        }
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle all unhandled exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=exc)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An internal server error occurred",
                "type": "internal_error"
            }
        }
    )


def register_exception_handlers(app):
    """Register all exception handlers with the FastAPI app"""
    app.add_exception_handler(ValidationError, validation_error_handler)
    app.add_exception_handler(BusinessRuleError, business_rule_error_handler)
    app.add_exception_handler(NotFoundError, not_found_error_handler)
    app.add_exception_handler(DatabaseError, database_error_handler)
    app.add_exception_handler(BaseApplicationException, base_application_exception_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)
    app.add_exception_handler(Exception, general_exception_handler)