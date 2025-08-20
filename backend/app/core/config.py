"""
Configuration management for the Autonomous Research System backend.

This module handles all configuration settings including environment variables,
database connections, API keys, and application settings.
"""

from typing import Optional, List
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Application
    APP_NAME: str = "Autonomous Research System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=False, env="DEBUG")
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    
    # Server
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")
    WORKERS: int = Field(default=1, env="WORKERS")
    
    # Database
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    DATABASE_POOL_SIZE: int = Field(default=10, env="DATABASE_POOL_SIZE")
    DATABASE_MAX_OVERFLOW: int = Field(default=20, env="DATABASE_MAX_OVERFLOW")
    DATABASE_POOL_TIMEOUT: int = Field(default=30, env="DATABASE_POOL_TIMEOUT")
    
    # Redis
    REDIS_URL: str = Field(default="redis://localhost:6379", env="REDIS_URL")
    REDIS_POOL_SIZE: int = Field(default=10, env="REDIS_POOL_SIZE")
    
    # Security
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = Field(default="HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, env="REFRESH_TOKEN_EXPIRE_DAYS")
    
    # CORS
    CORS_ORIGINS: List[str] = Field(default=["http://localhost:3000"], env="CORS_ORIGINS")
    CORS_ALLOW_CREDENTIALS: bool = Field(default=True, env="CORS_ALLOW_CREDENTIALS")
    CORS_ALLOW_METHODS: List[str] = Field(default=["*"], env="CORS_ALLOW_METHODS")
    CORS_ALLOW_HEADERS: List[str] = Field(default=["*"], env="CORS_ALLOW_HEADERS")
    
    # AI/ML Services
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    ANTHROPIC_API_KEY: str = Field(..., env="ANTHROPIC_API_KEY")
    LANGCHAIN_TRACING_V2: bool = Field(default=True, env="LANGCHAIN_TRACING_V2")
    LANGCHAIN_ENDPOINT: str = Field(default="https://api.smith.langchain.com", env="LANGCHAIN_ENDPOINT")
    LANGCHAIN_API_KEY: Optional[str] = Field(default=None, env="LANGCHAIN_API_KEY")
    LANGCHAIN_PROJECT: str = Field(default="autonomous-research", env="LANGCHAIN_PROJECT")
    
    # Search APIs
    TAVILY_API_KEY: Optional[str] = Field(default=None, env="TAVILY_API_KEY")
    SERPAPI_API_KEY: Optional[str] = Field(default=None, env="SERPAPI_API_KEY")
    
    # Storage
    STORAGE_TYPE: str = Field(default="local", env="STORAGE_TYPE")  # local, s3, gcs
    AWS_ACCESS_KEY_ID: Optional[str] = Field(default=None, env="AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: Optional[str] = Field(default=None, env="AWS_SECRET_ACCESS_KEY")
    AWS_REGION: str = Field(default="us-east-1", env="AWS_REGION")
    AWS_S3_BUCKET: Optional[str] = Field(default=None, env="AWS_S3_BUCKET")
    GCS_BUCKET: Optional[str] = Field(default=None, env="GCS_BUCKET")
    GCS_CREDENTIALS_FILE: Optional[str] = Field(default=None, env="GCS_CREDENTIALS_FILE")
    
    # File Storage
    UPLOAD_DIR: str = Field(default="./uploads", env="UPLOAD_DIR")
    MAX_FILE_SIZE: int = Field(default=50 * 1024 * 1024, env="MAX_FILE_SIZE")  # 50MB
    ALLOWED_FILE_TYPES: List[str] = Field(
        default=[".pdf", ".docx", ".txt", ".md", ".csv", ".xlsx"],
        env="ALLOWED_FILE_TYPES"
    )
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = Field(default=60, env="RATE_LIMIT_PER_MINUTE")
    RATE_LIMIT_PER_HOUR: int = Field(default=1000, env="RATE_LIMIT_PER_HOUR")
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FORMAT: str = Field(default="json", env="LOG_FORMAT")
    
    # Monitoring
    ENABLE_METRICS: bool = Field(default=True, env="ENABLE_METRICS")
    METRICS_PORT: int = Field(default=9090, env="METRICS_PORT")
    
    # Task Queue
    CELERY_BROKER_URL: str = Field(default="redis://localhost:6379/0", env="CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND: str = Field(default="redis://localhost:6379/0", env="CELERY_RESULT_BACKEND")
    CELERY_TASK_SERIALIZER: str = Field(default="json", env="CELERY_TASK_SERIALIZER")
    CELERY_RESULT_SERIALIZER: str = Field(default="json", env="CELERY_RESULT_SERIALIZER")
    CELERY_ACCEPT_CONTENT: List[str] = Field(default=["json"], env="CELERY_ACCEPT_CONTENT")
    CELERY_TIMEZONE: str = Field(default="UTC", env="CELERY_TIMEZONE")
    CELERY_ENABLE_UTC: bool = Field(default=True, env="CELERY_ENABLE_UTC")
    
    # Research Settings
    MAX_RESEARCH_TIME_MINUTES: int = Field(default=60, env="MAX_RESEARCH_TIME_MINUTES")
    MAX_SOURCES_PER_QUERY: int = Field(default=20, env="MAX_SOURCES_PER_QUERY")
    MIN_SOURCES_REQUIRED: int = Field(default=3, env="MIN_SOURCES_REQUIRED")
    
    # Report Settings
    DEFAULT_REPORT_FORMAT: str = Field(default="pdf", env="DEFAULT_REPORT_FORMAT")
    MAX_REPORT_LENGTH: int = Field(default=10000, env="MAX_REPORT_LENGTH")
    ENABLE_CITATIONS: bool = Field(default=True, env="ENABLE_CITATIONS")
    
    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS origins from string to list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @field_validator("ALLOWED_FILE_TYPES", mode="before")
    @classmethod
    def parse_file_types(cls, v):
        """Parse allowed file types from string to list."""
        if isinstance(v, str):
            return [ft.strip() for ft in v.split(",")]
        return v
    
    @field_validator("CELERY_ACCEPT_CONTENT", mode="before")
    @classmethod
    def parse_celery_content(cls, v):
        """Parse Celery accept content from string to list."""
        if isinstance(v, str):
            return [content.strip() for content in v.split(",")]
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get the global settings instance."""
    return settings


def is_development() -> bool:
    """Check if running in development mode."""
    return settings.ENVIRONMENT.lower() == "development"


def is_production() -> bool:
    """Check if running in production mode."""
    return settings.ENVIRONMENT.lower() == "production"


def is_testing() -> bool:
    """Check if running in testing mode."""
    return settings.ENVIRONMENT.lower() == "testing"


# Environment-specific configurations
class DevelopmentSettings(Settings):
    """Development-specific settings."""
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]


class ProductionSettings(Settings):
    """Production-specific settings."""
    DEBUG: bool = False
    LOG_LEVEL: str = "WARNING"
    WORKERS: int = 4


class TestingSettings(Settings):
    """Testing-specific settings."""
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///./test.db"
    REDIS_URL: str = "redis://localhost:6379/1"
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/1"


def get_environment_settings() -> Settings:
    """Get environment-specific settings."""
    env = os.getenv("ENVIRONMENT", "development").lower()
    
    if env == "production":
        return ProductionSettings()
    elif env == "testing":
        return TestingSettings()
    else:
        return DevelopmentSettings()
