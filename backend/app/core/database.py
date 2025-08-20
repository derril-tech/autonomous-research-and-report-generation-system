"""
Database configuration and session management for the Autonomous Research System.

This module handles database connections, session management, and provides
utilities for database operations with SQLAlchemy 2.0 async support.
"""

from typing import AsyncGenerator, Optional
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
    AsyncEngine
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import QueuePool
from sqlalchemy import event
import logging
from contextlib import asynccontextmanager

from .config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class Base(DeclarativeBase):
    """Base class for all database models."""
    pass


class DatabaseManager:
    """Database connection and session manager."""
    
    def __init__(self):
        self.engine: Optional[AsyncEngine] = None
        self.session_factory: Optional[async_sessionmaker[AsyncSession]] = None
        self._initialized = False
    
    async def initialize(self) -> None:
        """Initialize database connection and session factory."""
        if self._initialized:
            return
        
        # Create async engine with connection pooling
        self.engine = create_async_engine(
            settings.DATABASE_URL,
            echo=settings.DEBUG,
            poolclass=QueuePool,
            pool_size=settings.DATABASE_POOL_SIZE,
            max_overflow=settings.DATABASE_MAX_OVERFLOW,
            pool_timeout=settings.DATABASE_POOL_TIMEOUT,
            pool_pre_ping=True,
            pool_recycle=3600,  # Recycle connections every hour
        )
        
        # Create session factory
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )
        
        # Add engine event listeners for monitoring
        self._setup_engine_events()
        
        self._initialized = True
        logger.info("Database manager initialized successfully")
    
    def _setup_engine_events(self) -> None:
        """Setup engine event listeners for monitoring and debugging."""
        
        @event.listens_for(self.engine.sync_engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            """Set SQLite pragmas for better performance."""
            if "sqlite" in settings.DATABASE_URL:
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA journal_mode=WAL")
                cursor.execute("PRAGMA synchronous=NORMAL")
                cursor.execute("PRAGMA cache_size=10000")
                cursor.execute("PRAGMA temp_store=MEMORY")
                cursor.close()
        
        @event.listens_for(self.engine.sync_engine, "checkout")
        def receive_checkout(dbapi_connection, connection_record, connection_proxy):
            """Log connection checkout events."""
            if settings.DEBUG:
                logger.debug(f"Database connection checked out: {connection_record.info}")
        
        @event.listens_for(self.engine.sync_engine, "checkin")
        def receive_checkin(dbapi_connection, connection_record):
            """Log connection checkin events."""
            if settings.DEBUG:
                logger.debug(f"Database connection checked in: {connection_record.info}")
    
    async def close(self) -> None:
        """Close database connections and cleanup."""
        if self.engine:
            await self.engine.dispose()
            self.engine = None
            self.session_factory = None
            self._initialized = False
            logger.info("Database manager closed successfully")
    
    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get a database session with automatic cleanup."""
        if not self._initialized:
            await self.initialize()
        
        if not self.session_factory:
            raise RuntimeError("Database session factory not initialized")
        
        async with self.session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                await session.rollback()
                logger.error(f"Database session error: {e}")
                raise
            finally:
                await session.close()
    
    async def get_session_dependency(self) -> AsyncGenerator[AsyncSession, None]:
        """Dependency function for FastAPI dependency injection."""
        async with self.get_session() as session:
            yield session
    
    async def health_check(self) -> bool:
        """Check database connectivity."""
        try:
            async with self.get_session() as session:
                await session.execute("SELECT 1")
                return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False
    
    async def get_connection_info(self) -> dict:
        """Get database connection information."""
        if not self.engine:
            return {"status": "not_initialized"}
        
        try:
            async with self.engine.begin() as conn:
                result = await conn.execute("SELECT version()")
                version = result.scalar()
                
                return {
                    "status": "connected",
                    "version": version,
                    "pool_size": self.engine.pool.size(),
                    "checked_in": self.engine.pool.checkedin(),
                    "checked_out": self.engine.pool.checkedout(),
                    "overflow": self.engine.pool.overflow(),
                }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }


# Global database manager instance
db_manager = DatabaseManager()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency for database sessions."""
    async with db_manager.get_session() as session:
        yield session


async def init_db() -> None:
    """Initialize database and create tables."""
    await db_manager.initialize()
    
    # Import models to ensure they are registered
    from ..models import user, research_job, report
    
    # Create tables
    async with db_manager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("Database tables created successfully")


async def close_db() -> None:
    """Close database connections."""
    await db_manager.close()


# Database utilities
class DatabaseUtils:
    """Utility functions for database operations."""
    
    @staticmethod
    async def execute_raw_sql(sql: str, params: Optional[dict] = None) -> any:
        """Execute raw SQL query."""
        async with db_manager.get_session() as session:
            result = await session.execute(sql, params or {})
            return result
    
    @staticmethod
    async def get_table_count(table_name: str) -> int:
        """Get row count for a table."""
        async with db_manager.get_session() as session:
            result = await session.execute(f"SELECT COUNT(*) FROM {table_name}")
            return result.scalar()
    
    @staticmethod
    async def vacuum_database() -> None:
        """Vacuum database to reclaim space (SQLite only)."""
        if "sqlite" in settings.DATABASE_URL:
            async with db_manager.get_session() as session:
                await session.execute("VACUUM")
                await session.commit()
                logger.info("Database vacuum completed")
    
    @staticmethod
    async def analyze_database() -> None:
        """Analyze database for query optimization."""
        async with db_manager.get_session() as session:
            await session.execute("ANALYZE")
            await session.commit()
            logger.info("Database analysis completed")


# Migration utilities
class MigrationUtils:
    """Utilities for database migrations."""
    
    @staticmethod
    async def get_current_version() -> Optional[str]:
        """Get current database version."""
        try:
            async with db_manager.get_session() as session:
                result = await session.execute(
                    "SELECT version_num FROM alembic_version LIMIT 1"
                )
                return result.scalar()
        except Exception:
            return None
    
    @staticmethod
    async def is_migration_needed() -> bool:
        """Check if database migration is needed."""
        # This would typically check against expected schema version
        # For now, return False as a placeholder
        return False


# Export commonly used items
__all__ = [
    "Base",
    "DatabaseManager",
    "db_manager",
    "get_db",
    "init_db",
    "close_db",
    "DatabaseUtils",
    "MigrationUtils",
]
