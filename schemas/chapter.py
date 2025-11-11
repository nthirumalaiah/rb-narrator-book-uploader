from pydantic import BaseModel, Field, validator, HttpUrl
from typing import Optional, Union
from datetime import datetime
from models.chapter import StatusEnum


class ChapterCreate(BaseModel):
    """Request model for creating chapters with validation"""
    book_id: int = Field(..., gt=0, description="Book ID must be positive")
    title: str = Field(..., min_length=1, max_length=200, description="Chapter title")
    sequence: int = Field(..., ge=1, description="Chapter sequence number (starting from 1)")
    file_url: Optional[Union[HttpUrl, str]] = Field(None, description="URL to the audio file")
    status: StatusEnum = Field(StatusEnum.pending, description="Chapter status")

    @validator('title')
    def validate_title(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Title cannot be empty or whitespace only')
        return v.strip()

    @validator('file_url', pre=True)
    def validate_file_url(cls, v: Union[str, None]) -> Union[str, None]:
        if v is not None and v.strip() == '':
            return None
        return v

    class Config:
        schema_extra = {
            "example": {
                "book_id": 1,
                "title": "Chapter 1: The Beginning",
                "sequence": 1,
                "file_url": "https://example.com/audio/chapter1.mp3",
                "status": "pending"
            }
        }


class ChapterResponse(BaseModel):
    """Response model for chapter data"""
    id: int = Field(..., description="Unique chapter identifier")
    book_id: int = Field(..., description="Associated book identifier")
    title: str = Field(..., description="Chapter title")
    sequence: int = Field(..., description="Chapter sequence number")
    file_url: Optional[str] = Field(None, description="URL to the audio file")
    status: str = Field(..., description="Current chapter status")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "book_id": 1,
                "title": "Chapter 1: The Beginning",
                "sequence": 1,
                "file_url": "https://example.com/audio/chapter1.mp3",
                "status": "completed",
                "created_at": "2023-01-01T12:00:00",
                "updated_at": "2023-01-01T12:00:00"
            }
        }


class ChapterUpdate(BaseModel):
    """Request model for updating chapters with validation"""
    book_id: Optional[int] = Field(None, gt=0, description="Book ID must be positive")
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Chapter title")
    sequence: Optional[int] = Field(None, ge=1, description="Chapter sequence number")
    file_url: Optional[Union[HttpUrl, str]] = Field(None, description="URL to the audio file")
    status: Optional[StatusEnum] = Field(None, description="Chapter status")

    @validator('title')
    def validate_title(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError('Title cannot be empty or whitespace only')
        return v.strip() if v else None

    @validator('file_url', pre=True)
    def validate_file_url(cls, v: Union[str, None]) -> Union[str, None]:
        if v is not None and v.strip() == '':
            return None
        return v

    class Config:
        schema_extra = {
            "example": {
                "title": "Chapter 1: The Updated Beginning",
                "status": "completed",
                "file_url": "https://example.com/audio/chapter1_final.mp3"
            }
        }