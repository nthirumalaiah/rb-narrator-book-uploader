"""
Chapter-specific exception classes.
Follows Single Responsibility Principle - each exception has a specific purpose.
"""

from exceptions.base_exceptions import ValidationError, BusinessRuleError, NotFoundError


class ChapterValidationError(ValidationError):
    """Raised when chapter data validation fails"""
    
    def __init__(self, message: str, field: str = None):
        self.field = field
        super().__init__(message, "CHAPTER_VALIDATION_ERROR")


class ChapterNotFoundError(NotFoundError):
    """Raised when a requested chapter is not found"""
    
    def __init__(self, message: str, chapter_id: int = None):
        self.chapter_id = chapter_id
        super().__init__(message, "CHAPTER_NOT_FOUND")


class ChapterBusinessRuleError(BusinessRuleError):
    """Raised when a business rule is violated"""
    
    def __init__(self, message: str, rule_name: str = None):
        self.rule_name = rule_name
        super().__init__(message, "CHAPTER_BUSINESS_RULE_ERROR")


class ChapterAlreadyExistsError(BusinessRuleError):
    """Raised when trying to create a chapter that already exists"""
    
    def __init__(self, message: str, book_id: int = None, sequence: int = None):
        self.book_id = book_id
        self.sequence = sequence
        super().__init__(message, "CHAPTER_ALREADY_EXISTS")