from typing import List, Optional
from models.chapter import Chapter, StatusEnum
from repositories.interfaces.chapter_repository import ChapterRepositoryInterface
from services.interfaces.chapter_service import ChapterServiceInterface
from schemas.chapter import ChapterCreate, ChapterResponse, ChapterUpdate
from exceptions.chapter_exceptions import ChapterNotFoundError, ChapterValidationError, ChapterBusinessRuleError


class ChapterService(ChapterServiceInterface):
    """
    Concrete implementation of ChapterService.
    Contains business logic and follows Dependency Inversion Principle.
    """

    def __init__(self, chapter_repository: ChapterRepositoryInterface):
        """
        Initialize service with repository dependency.
        Follows Dependency Injection pattern.
        """
        self._repository = chapter_repository

    async def create_chapter(self, chapter_data: ChapterCreate) -> ChapterResponse:
        """
        Create a new chapter with business logic validation.
        Applies business rules before creation.
        """
        # Business rule: Validate sequence uniqueness within a book
        await self._validate_sequence_uniqueness(chapter_data.book_id, chapter_data.sequence)
        
        # Business rule: Validate chapter title
        self._validate_chapter_title(chapter_data.title)
        
        # Create chapter domain object
        chapter = Chapter(
            book_id=chapter_data.book_id,
            title=chapter_data.title.strip(),
            sequence=chapter_data.sequence,
            file_url=chapter_data.file_url,
            status=chapter_data.status
        )
        
        # Persist through repository
        created_chapter = self._repository.create(chapter)
        
        # Convert to response schema
        return self._map_to_response(created_chapter)

    async def get_chapter_by_id(self, chapter_id: int) -> Optional[ChapterResponse]:
        """Get chapter by ID with business logic"""
        if chapter_id <= 0:
            raise ChapterValidationError("Chapter ID must be positive")
        
        chapter = self._repository.get_by_id(chapter_id)
        if not chapter:
            return None
        
        return self._map_to_response(chapter)

    async def get_all_chapters(self) -> List[ChapterResponse]:
        """Get all chapters ordered by book_id and sequence"""
        chapters = self._repository.get_all()
        return [self._map_to_response(chapter) for chapter in chapters]

    async def get_chapters_by_book(self, book_id: int) -> List[ChapterResponse]:
        """Get chapters by book ID with validation"""
        if book_id <= 0:
            raise ChapterValidationError("Book ID must be positive")
        
        chapters = self._repository.get_by_book_id(book_id)
        return [self._map_to_response(chapter) for chapter in chapters]

    async def update_chapter(self, chapter_id: int, chapter_data: ChapterUpdate) -> Optional[ChapterResponse]:
        """Update chapter with validation and business rules"""
        # Check if chapter exists
        if not self._repository.exists(chapter_id):
            raise ChapterNotFoundError(f"Chapter with ID {chapter_id} not found")
        
        # Validate update data
        update_dict = {}
        if chapter_data.title is not None:
            self._validate_chapter_title(chapter_data.title)
            update_dict['title'] = chapter_data.title.strip()
        
        if chapter_data.sequence is not None:
            # Get current chapter to check if sequence is changing
            current_chapter = self._repository.get_by_id(chapter_id)
            if current_chapter and current_chapter.sequence != chapter_data.sequence:
                await self._validate_sequence_uniqueness(
                    current_chapter.book_id, 
                    chapter_data.sequence, 
                    exclude_chapter_id=chapter_id
                )
            update_dict['sequence'] = chapter_data.sequence
        
        # Add other fields
        if chapter_data.book_id is not None:
            update_dict['book_id'] = chapter_data.book_id
        if chapter_data.file_url is not None:
            update_dict['file_url'] = chapter_data.file_url
        if chapter_data.status is not None:
            update_dict['status'] = chapter_data.status
        
        # Update through repository
        updated_chapter = self._repository.update(chapter_id, update_dict)
        return self._map_to_response(updated_chapter) if updated_chapter else None

    async def delete_chapter(self, chapter_id: int) -> bool:
        """Delete chapter with business rules"""
        # Business rule: Check if chapter can be deleted
        chapter = self._repository.get_by_id(chapter_id)
        if not chapter:
            raise ChapterNotFoundError(f"Chapter with ID {chapter_id} not found")
        
        # Business rule: Cannot delete uploaded chapters without confirmation
        if chapter.status == StatusEnum.uploaded:
            raise ChapterBusinessRuleError("Cannot delete uploaded chapters. Please change status first.")
        
        return self._repository.delete(chapter_id)

    async def chapter_exists(self, chapter_id: int) -> bool:
        """Check if chapter exists"""
        return self._repository.exists(chapter_id)

    # Private helper methods
    
    def _validate_chapter_title(self, title: str) -> None:
        """Validate chapter title according to business rules"""
        if not title or not title.strip():
            raise ChapterValidationError("Chapter title cannot be empty")
        
        if len(title.strip()) < 3:
            raise ChapterValidationError("Chapter title must be at least 3 characters long")
        
        if len(title.strip()) > 255:
            raise ChapterValidationError("Chapter title cannot exceed 255 characters")

    async def _validate_sequence_uniqueness(self, book_id: int, sequence: int, exclude_chapter_id: Optional[int] = None) -> None:
        """Validate that sequence is unique within a book"""
        chapters = self._repository.get_by_book_id(book_id)
        
        for chapter in chapters:
            if chapter.sequence == sequence and chapter.id != exclude_chapter_id:
                raise ChapterBusinessRuleError(
                    f"Sequence {sequence} already exists for book {book_id}"
                )

    def _map_to_response(self, chapter: Chapter) -> ChapterResponse:
        """Map Chapter entity to ChapterResponse schema"""
        return ChapterResponse(
            id=chapter.id,
            book_id=chapter.book_id,
            title=chapter.title,
            sequence=chapter.sequence,
            file_url=chapter.file_url,
            status=chapter.status.value if isinstance(chapter.status, StatusEnum) else chapter.status
        )