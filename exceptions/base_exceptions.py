"""
Base exception classes for the application.
Follows Open/Closed Principle - new exceptions can be added without modifying existing ones.
"""


class BaseApplicationException(Exception):
    """Base class for all application exceptions"""
    
    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        super().__init__(self.message)


class ValidationError(BaseApplicationException):
    """Base class for validation errors"""
    pass


class BusinessRuleError(BaseApplicationException):
    """Base class for business rule violations"""
    pass


class NotFoundError(BaseApplicationException):
    """Base class for not found errors"""
    pass


class DatabaseError(BaseApplicationException):
    """Base class for database-related errors"""
    pass