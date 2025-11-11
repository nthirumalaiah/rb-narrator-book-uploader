"""
Validation configuration and constants for the application.
Centralized validation rules to ensure consistency across all endpoints.
"""

from typing import Dict, Any
from pydantic import Field

# Global validation constants
class ValidationLimits:
    """Centralized validation limits and constraints"""
    
    # String length limits
    TITLE_MIN_LENGTH: int = 1
    TITLE_MAX_LENGTH: int = 200
    FILENAME_MAX_LENGTH: int = 255
    URL_MAX_LENGTH: int = 2048
    
    # Numeric limits
    MIN_POSITIVE_INT: int = 1
    MAX_SEQUENCE_NUMBER: int = 10000
    MIN_PART_NUMBER: int = 1
    MAX_PART_NUMBER: int = 10000
    
    # Pagination limits
    DEFAULT_SKIP: int = 0
    DEFAULT_LIMIT: int = 100
    MAX_LIMIT: int = 1000
    MIN_LIMIT: int = 1
    
    # Time limits (seconds)
    MIN_EXPIRES_IN: int = 60  # 1 minute
    MAX_EXPIRES_IN: int = 604800  # 7 days
    DEFAULT_EXPIRES_IN: int = 3600  # 1 hour
    
    # File type constraints
    ALLOWED_AUDIO_TYPES: list = [
        'audio/mpeg', 'audio/mp3', 'audio/wav', 'audio/aac', 
        'audio/ogg', 'audio/flac', 'audio/m4a'
    ]


class ValidationMessages:
    """Centralized validation error messages"""
    
    TITLE_EMPTY: str = "Title cannot be empty or whitespace only"
    TITLE_TOO_LONG: str = f"Title must not exceed {ValidationLimits.TITLE_MAX_LENGTH} characters"
    FILENAME_EMPTY: str = "Filename cannot be empty"
    FILENAME_INVALID_CHARS: str = "Filename contains invalid characters. Use only letters, numbers, dots, hyphens, and underscores."
    CONTENT_TYPE_INVALID: str = f"Content type must be one of: {', '.join(ValidationLimits.ALLOWED_AUDIO_TYPES)}"
    POSITIVE_INT_REQUIRED: str = "Value must be a positive integer"
    DUPLICATE_SEQUENCE: str = "Chapter with this sequence already exists for the book"
    CHAPTER_NOT_FOUND: str = "Chapter not found"
    INVALID_ETAG: str = "Invalid ETag format"
    PARTS_NOT_SEQUENTIAL: str = "Parts must be sequential starting from 1"


class ValidationFields:
    """Reusable field definitions with validation"""
    
    @staticmethod
    def positive_id(description: str = "Positive integer ID") -> Field:
        """Standard positive ID field validation"""
        return Field(..., gt=0, description=description)
    
    @staticmethod
    def title_field(description: str = "Title field") -> Field:
        """Standard title field validation"""
        return Field(
            ..., 
            min_length=ValidationLimits.TITLE_MIN_LENGTH,
            max_length=ValidationLimits.TITLE_MAX_LENGTH,
            description=description
        )
    
    @staticmethod
    def filename_field(description: str = "Filename") -> Field:
        """Standard filename field validation"""
        return Field(
            ...,
            min_length=1,
            max_length=ValidationLimits.FILENAME_MAX_LENGTH,
            description=description
        )
    
    @staticmethod
    def sequence_field(description: str = "Sequence number") -> Field:
        """Standard sequence field validation"""
        return Field(
            ...,
            ge=ValidationLimits.MIN_POSITIVE_INT,
            description=description
        )
    
    @staticmethod
    def part_number_field(description: str = "Part number") -> Field:
        """Standard part number field validation"""
        return Field(
            ...,
            ge=ValidationLimits.MIN_PART_NUMBER,
            le=ValidationLimits.MAX_PART_NUMBER,
            description=description
        )
    
    @staticmethod
    def expires_in_field(description: str = "Expiration time in seconds") -> Field:
        """Standard expiration field validation"""
        return Field(
            ValidationLimits.DEFAULT_EXPIRES_IN,
            ge=ValidationLimits.MIN_EXPIRES_IN,
            le=ValidationLimits.MAX_EXPIRES_IN,
            description=description
        )
    
    @staticmethod
    def pagination_skip_field(description: str = "Number of records to skip") -> Field:
        """Standard pagination skip field"""
        return Field(
            ValidationLimits.DEFAULT_SKIP,
            ge=0,
            description=description
        )
    
    @staticmethod
    def pagination_limit_field(description: str = "Maximum number of records") -> Field:
        """Standard pagination limit field"""
        return Field(
            ValidationLimits.DEFAULT_LIMIT,
            ge=ValidationLimits.MIN_LIMIT,
            le=ValidationLimits.MAX_LIMIT,
            description=description
        )


# Common response examples for documentation
VALIDATION_EXAMPLES = {
    "chapter_create": {
        "book_id": 1,
        "title": "Chapter 1: The Beginning",
        "sequence": 1,
        "file_url": "https://example.com/audio/chapter1.mp3",
        "status": "pending"
    },
    "chapter_response": {
        "id": 1,
        "book_id": 1,
        "title": "Chapter 1: The Beginning",
        "sequence": 1,
        "file_url": "https://example.com/audio/chapter1.mp3",
        "status": "completed",
        "created_at": "2023-01-01T12:00:00",
        "updated_at": "2023-01-01T12:00:00"
    },
    "upload_initiate": {
        "filename": "chapter1.mp3",
        "content_type": "audio/mpeg"
    },
    "validation_error": {
        "detail": [
            {
                "loc": ["body", "title"],
                "msg": ValidationMessages.TITLE_EMPTY,
                "type": "value_error"
            }
        ]
    },
    "not_found_error": {
        "detail": ValidationMessages.CHAPTER_NOT_FOUND
    }
}