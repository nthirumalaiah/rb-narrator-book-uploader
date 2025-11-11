"""
Dependency injection container for the application.
Follows Dependency Inversion Principle and makes testing easier.
"""

from functools import lru_cache
from sqlalchemy.orm import Session
from repositories.interfaces.chapter_repository import ChapterRepositoryInterface
from repositories.chapter_repository import SQLAlchemyChapterRepository
from services.interfaces.chapter_service import ChapterServiceInterface
from services.chapter_service import ChapterService
from core.db import SessionLocal


class DependencyContainer:
    """
    Dependency injection container that manages object creation and lifecycle.
    Follows Dependency Inversion Principle.
    """
    
    def __init__(self):
        self._chapter_repository = None
        self._chapter_service = None
    
    def get_db_session(self) -> Session:
        """Get database session"""
        return SessionLocal()
    
    def get_chapter_repository(self, db_session: Session) -> ChapterRepositoryInterface:
        """Get chapter repository with injected database session"""
        return SQLAlchemyChapterRepository(db_session)
    
    def get_chapter_service(self, db_session: Session) -> ChapterServiceInterface:
        """Get chapter service with injected dependencies"""
        chapter_repository = self.get_chapter_repository(db_session)
        return ChapterService(chapter_repository)


# Global container instance
@lru_cache()
def get_container() -> DependencyContainer:
    """Get singleton instance of dependency container"""
    return DependencyContainer()


# Dependency providers for FastAPI
def get_db() -> Session:
    """Database session dependency provider"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_chapter_service(db: Session = None) -> ChapterServiceInterface:
    """Chapter service dependency provider"""
    if db is None:
        db = next(get_db())
    
    container = get_container()
    return container.get_chapter_service(db)