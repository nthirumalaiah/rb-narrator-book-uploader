from abc import ABC, abstractmethod
from typing import List, Optional
from sqlalchemy.orm import Session
from models.chapter import Chapter


class ChapterRepositoryInterface(ABC):
    """
    Abstract interface for Chapter repository operations.
    Follows Interface Segregation Principle by defining only necessary methods.
    """

    @abstractmethod
    def create(self, chapter: Chapter) -> Chapter:
        """Create a new chapter"""
        pass

    @abstractmethod
    def get_by_id(self, chapter_id: int) -> Optional[Chapter]:
        """Get chapter by ID"""
        pass

    @abstractmethod
    def get_all(self) -> List[Chapter]:
        """Get all chapters"""
        pass

    @abstractmethod
    def get_by_book_id(self, book_id: int) -> List[Chapter]:
        """Get chapters by book ID"""
        pass

    @abstractmethod
    def update(self, chapter_id: int, chapter_data: dict) -> Optional[Chapter]:
        """Update chapter"""
        pass

    @abstractmethod
    def delete(self, chapter_id: int) -> bool:
        """Delete chapter"""
        pass

    @abstractmethod
    def exists(self, chapter_id: int) -> bool:
        """Check if chapter exists"""
        pass