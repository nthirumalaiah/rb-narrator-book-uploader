"""
Configuration management following Open/Closed Principle.
New configuration sections can be added without modifying existing ones.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import validator
from dotenv import load_dotenv
from urllib.parse import quote_plus


# Load environment variables
load_dotenv()


class DatabaseSettings(BaseSettings):
    """Database configuration settings"""
    
    host: str = "localhost"
    port: int = 3306
    username: str = "root"
    password: str = "password"
    database: str = "narrator_portal"
    driver: str = "pymysql"
    
    @validator('port')
    def port_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Port must be positive')
        return v
    
    @property
    def database_url(self) -> str:
        """Construct database URL from components"""
        encoded_password = quote_plus(self.password)
        return f"mysql+{self.driver}://{self.username}:{encoded_password}@{self.host}:{self.port}/{self.database}"
    
    class Config:
        env_prefix = "DB_"


class AWSSettings(BaseSettings):
    """AWS configuration settings"""
    
    region: str = "us-west-2"
    access_key_id: Optional[str] = None
    secret_access_key: Optional[str] = None
    s3_bucket: Optional[str] = None
    
    class Config:
        env_prefix = "AWS_"


class AppSettings(BaseSettings):
    """Application configuration settings"""
    
    title: str = "RB Narrator Book Uploader API"
    description: str = "API for managing book chapters and audio uploads"
    version: str = "1.0.0"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False
    
    # CORS settings
    cors_origins: list = ["*"]
    cors_methods: list = ["*"]
    cors_headers: list = ["*"]
    
    class Config:
        env_prefix = "APP_"


class LoggingSettings(BaseSettings):
    """Logging configuration settings"""
    
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_path: Optional[str] = None
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5
    
    class Config:
        env_prefix = "LOG_"


class Settings:
    """
    Main settings class that aggregates all configuration sections.
    Follows Composition over Inheritance and Single Responsibility Principle.
    """
    
    def __init__(self):
        self.database = DatabaseSettings()
        self.aws = AWSSettings()
        self.app = AppSettings()
        self.logging = LoggingSettings()
    
    def __repr__(self):
        return f"Settings(app={self.app.title}, db={self.database.host}:{self.database.port})"


# Global settings instance
def get_settings() -> Settings:
    """Get application settings"""
    return Settings()


# Environment-specific settings
def get_development_settings() -> Settings:
    """Get development environment settings"""
    settings = Settings()
    settings.app.debug = True
    settings.app.reload = True
    settings.logging.level = "DEBUG"
    return settings


def get_production_settings() -> Settings:
    """Get production environment settings"""
    settings = Settings()
    settings.app.debug = False
    settings.app.reload = False
    settings.logging.level = "WARNING"
    settings.logging.file_path = "/var/log/narrator-api.log"
    return settings


def get_test_settings() -> Settings:
    """Get test environment settings"""
    settings = Settings()
    settings.database.database = "narrator_portal_test"
    settings.app.debug = True
    settings.logging.level = "DEBUG"
    return settings