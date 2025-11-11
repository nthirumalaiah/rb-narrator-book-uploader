from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from core.db import Base
import enum

class StatusEnum(str, enum.Enum):
    pending = "pending"
    uploaded = "uploaded"
    processed = "processed"

class Chapter(Base):
    __tablename__ = "chapters"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    title = Column(String(255))
    sequence = Column(Integer)
    file_url = Column(String(255), nullable=True)
    status = Column(Enum(StatusEnum), default=StatusEnum.pending)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)