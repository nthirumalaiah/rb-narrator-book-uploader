"""
Chapter API routes following Single Responsibility Principle.
This module is responsible only for HTTP layer concerns with comprehensive validation.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

from schemas.chapter import ChapterCreate, ChapterResponse, ChapterUpdate
from models.chapter import Chapter
from core.dependencies import get_db

# Create router instance with comprehensive error responses
router = APIRouter(
    prefix="/chapters",
    tags=["chapters"],
    responses={
        400: {"description": "Bad request - Invalid input data"},
        404: {"description": "Chapter not found"},
        422: {"description": "Validation error"},
        500: {"description": "Internal server error"}
    },
)


@router.post(
    "/",
    response_model=ChapterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new chapter",
    description="Create a new chapter with comprehensive validation"
)
async def create_chapter(
    chapter_data: ChapterCreate,
    db: Session = Depends(get_db)
) -> ChapterResponse:
    """
    Create a new chapter with validation.
    
    - **book_id**: ID of the book this chapter belongs to (must be positive)
    - **title**: Title of the chapter (1-200 characters)
    - **sequence**: Sequential number of the chapter within the book (>= 1)
    - **file_url**: Optional URL to the audio file
    - **status**: Chapter status (pending, uploaded, processed, completed)
    
    Raises:
        HTTPException: 400 if validation fails or duplicate sequence
        HTTPException: 500 if database error occurs
    """
    try:
        # Check for duplicate sequence in the same book
        existing_chapter = db.query(Chapter).filter(
            Chapter.book_id == chapter_data.book_id,
            Chapter.sequence == chapter_data.sequence
        ).first()
        
        if existing_chapter:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Chapter with sequence {chapter_data.sequence} already exists for book {chapter_data.book_id}"
            )
        
        # Create new chapter instance
        new_chapter = Chapter(
            book_id=chapter_data.book_id,
            title=chapter_data.title,
            sequence=chapter_data.sequence,
            file_url=chapter_data.file_url,
            status=chapter_data.status,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Add to database
        db.add(new_chapter)
        db.commit()
        db.refresh(new_chapter)
        
        return new_chapter
        
    except HTTPException:
        # Re-raise HTTP exceptions (like duplicate sequence)
        db.rollback()
        raise
    except SQLAlchemyError as e:
        # Database-specific errors
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        ) from e
    except Exception as e:
        # General errors
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating chapter: {str(e)}"
        ) from e


@router.get(
    "/",
    response_model=List[ChapterResponse],
    summary="Get all chapters",
    description="Retrieve all chapters with optional filtering and pagination"
)
async def get_all_chapters(
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    book_id: Optional[int] = Query(None, ge=1, description="Filter by book ID"),
    db: Session = Depends(get_db)
) -> List[ChapterResponse]:
    """
    Get all chapters with optional filtering and pagination.
    
    Args:
        skip: Number of records to skip (pagination)
        limit: Maximum number of records to return (1-1000)
        book_id: Optional filter by book ID
        db: Database session
        
    Returns:
        List of chapters ordered by book_id and sequence
        
    Raises:
        HTTPException: 500 if database error occurs
    """
    try:
        query = db.query(Chapter)
        
        # Apply book filter if provided
        if book_id is not None:
            query = query.filter(Chapter.book_id == book_id)
            
        # Apply ordering and pagination
        chapters = query.order_by(Chapter.book_id, Chapter.sequence).offset(skip).limit(limit).all()
        return chapters
        
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error retrieving chapters: {str(e)}"
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving chapters: {str(e)}"
        ) from e


@router.get(
    "/{chapter_id}",
    response_model=ChapterResponse,
    summary="Get chapter by ID",
    description="Retrieve a specific chapter by its ID with validation"
)
async def get_chapter(
    chapter_id: int = Path(..., gt=0, description="Chapter ID (must be positive)"),
    db: Session = Depends(get_db)
) -> ChapterResponse:
    """
    Get a specific chapter by ID with validation.
    
    Args:
        chapter_id: Positive integer ID of the chapter
        db: Database session
        
    Returns:
        Chapter data if found
        
    Raises:
        HTTPException: 404 if chapter not found
        HTTPException: 500 if database error occurs
    """
    try:
        chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
        if not chapter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Chapter with ID {chapter_id} not found"
            )
        return chapter
        
    except HTTPException:
        # Re-raise HTTP exceptions (like 404)
        raise
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error retrieving chapter: {str(e)}"
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving chapter: {str(e)}"
        ) from e


@router.get(
    "/book/{book_id}",
    response_model=List[ChapterResponse],
    summary="Get chapters by book ID", 
    description="Retrieve all chapters for a specific book with validation"
)
async def get_chapters_by_book(
    book_id: int = Path(..., gt=0, description="Book ID (must be positive)"),
    db: Session = Depends(get_db)
) -> List[ChapterResponse]:
    """
    Get all chapters for a specific book with validation.
    
    Args:
        book_id: Positive integer ID of the book
        db: Database session
        
    Returns:
        List of chapters ordered by sequence
        
    Raises:
        HTTPException: 500 if database error occurs
    """
    try:
        chapters = db.query(Chapter).filter(
            Chapter.book_id == book_id
        ).order_by(Chapter.sequence).all()
        return chapters
        
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error retrieving chapters for book {book_id}: {str(e)}"
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving chapters for book {book_id}: {str(e)}"
        ) from e