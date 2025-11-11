from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.chapter import Chapter
from repositories.interfaces.chapter_repository import ChapterRepositoryInterface
from datetime import datetime


class SQLAlchemyChapterRepository(ChapterRepositoryInterface):
    """
    Concrete implementation of ChapterRepository using SQLAlchemy.
    Follows Dependency Inversion Principle by depending on abstractions.
    """

    def __init__(self, db_session: Session):
        """
        Initialize repository with database session.
        Follows Dependency Injection pattern.
        """
        self._db = db_session

    def create(self, chapter: Chapter) -> Chapter:
        """Create a new chapter in the database"""
        try:
            chapter.created_at = datetime.now()
            chapter.updated_at = datetime.now()
            self._db.add(chapter)
            self._db.commit()
            self._db.refresh(chapter)
            return chapter
        except SQLAlchemyError as e:
            self._db.rollback()
            raise e

    def get_by_id(self, chapter_id: int) -> Optional[Chapter]:
        """Retrieve chapter by ID"""
        try:
            return self._db.query(Chapter).filter(Chapter.id == chapter_id).first()
        except SQLAlchemyError as e:
            raise e

    def get_all(self) -> List[Chapter]:
        """Retrieve all chapters"""
        try:
            return self._db.query(Chapter).all()
        except SQLAlchemyError as e:
            raise e

    def get_by_book_id(self, book_id: int) -> List[Chapter]:
        """Retrieve chapters by book ID"""
        try:
            return self._db.query(Chapter).filter(Chapter.book_id == book_id).order_by(Chapter.sequence).all()
        except SQLAlchemyError as e:
            raise e

    def update(self, chapter_id: int, chapter_data: dict) -> Optional[Chapter]:
        """Update chapter with new data"""
        try:
            chapter = self._db.query(Chapter).filter(Chapter.id == chapter_id).first()
            if not chapter:
                return None
            
            # Update only provided fields
            for field, value in chapter_data.items():
                if hasattr(chapter, field) and value is not None:
                    setattr(chapter, field, value)
            
            chapter.updated_at = datetime.now()
            self._db.commit()
            self._db.refresh(chapter)
            return chapter
        except SQLAlchemyError as e:
            self._db.rollback()
            raise e

    def delete(self, chapter_id: int) -> bool:
        """Delete chapter by ID"""
        try:
            chapter = self._db.query(Chapter).filter(Chapter.id == chapter_id).first()
            if not chapter:
                return False
            
            self._db.delete(chapter)
            self._db.commit()
            return True
        except SQLAlchemyError as e:
            self._db.rollback()
            raise e

    def exists(self, chapter_id: int) -> bool:
        """Check if chapter exists"""
        try:
            return self._db.query(Chapter).filter(Chapter.id == chapter_id).first() is not None
        except SQLAlchemyError as e:
            raise e