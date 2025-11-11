from abc import ABC, abstractmethod
from typing import List, Optional
from schemas.chapter import ChapterCreate, ChapterResponse, ChapterUpdate


class ChapterServiceInterface(ABC):
    """
    Abstract interface for Chapter service operations.
    Follows Interface Segregation Principle.
    """

    @abstractmethod
    async def create_chapter(self, chapter_data: ChapterCreate) -> ChapterResponse:
        """Create a new chapter with business logic validation"""
        ...

    @abstractmethod
    async def get_chapter_by_id(self, chapter_id: int) -> Optional[ChapterResponse]:
        """Get chapter by ID with business logic"""
        ...

    @abstractmethod
    async def get_all_chapters(self) -> List[ChapterResponse]:
        """Get all chapters"""
        ...

    @abstractmethod
    async def get_chapters_by_book(self, book_id: int) -> List[ChapterResponse]:
        """Get chapters by book ID"""
        ...

    @abstractmethod
    async def update_chapter(self, chapter_id: int, chapter_data: ChapterUpdate) -> Optional[ChapterResponse]:
        """Update chapter with validation"""
        ...

    @abstractmethod
    async def delete_chapter(self, chapter_id: int) -> bool:
        """Delete chapter with business rules"""
        ...

    @abstractmethod
    async def chapter_exists(self, chapter_id: int) -> bool:
        """Check if chapter exists"""
        ...