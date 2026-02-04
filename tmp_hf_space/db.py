"""
Database connection and session management module.

This module provides async database connectivity to Neon PostgreSQL
using SQLModel and asyncpg driver. It implements connection pooling,
session management, and lifecycle utilities.

Usage:
    from db import get_engine, get_session, init_db, close_db

    # Initialize database tables
    await init_db()

    # Use session in FastAPI endpoint
    async def endpoint(session: AsyncSession = Depends(get_session)):
        ...
"""

import os
import logging
from typing import AsyncGenerator

from contextlib import asynccontextmanager

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession, async_sessionmaker
from sqlmodel import SQLModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Module-level engine singleton
_engine: AsyncEngine | None = None

# Session factory
_async_session_maker: async_sessionmaker[AsyncSession] | None = None


def _get_database_url() -> str:
    """
    Get and validate the DATABASE_URL environment variable.

    Returns:
        str: The validated database URL.

    Raises:
        ValueError: If DATABASE_URL is not set or invalid.
    """
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError(
            "DATABASE_URL environment variable is not set. "
            "Please create a .env file with your Neon database connection string. "
            "Example: DATABASE_URL=postgresql+asyncpg://user:pass@host/db?sslmode=require"
        )

    if not database_url.startswith("postgresql+asyncpg://"):
        raise ValueError(
            "DATABASE_URL must use asyncpg driver format. "
            "Expected: postgresql+asyncpg://user:pass@host/db?sslmode=require"
        )

    if "ssl=require" not in database_url and "sslmode=require" not in database_url:
        logger.warning("DATABASE_URL should include ssl=require for Neon PostgreSQL")

    return database_url


def get_engine() -> AsyncEngine:
    """
    Get the async database engine (singleton pattern).

    Creates the engine on first call with connection pooling configured:
    - pool_size: 1 (minimum connections)
    - max_overflow: 9 (allows up to 10 total connections)
    - pool_pre_ping: True (validates connections before use)

    Returns:
        AsyncEngine: The SQLAlchemy async engine instance.

    Raises:
        ValueError: If DATABASE_URL is not configured.

    Example:
        engine = get_engine()
    """
    global _engine

    if _engine is None:
        database_url = _get_database_url()

        try:
            _engine = create_async_engine(
                database_url,
                echo=False,  # Set to True for SQL query logging
                pool_size=1,  # Minimum connections in pool
                max_overflow=9,  # Allow up to 10 total connections
                pool_pre_ping=True,  # Validate connections before use
                pool_recycle=300,  # Recycle connections after 5 minutes
            )
            logger.info("Database engine created successfully")
        except Exception as e:
            logger.error(f"Failed to create database engine: {e}")
            raise

    return _engine


def _get_session_maker() -> async_sessionmaker[AsyncSession]:
    """
    Get the async session maker (singleton pattern).

    Returns:
        async_sessionmaker: Session factory bound to the engine.
    """
    global _async_session_maker

    if _async_session_maker is None:
        engine = get_engine()
        _async_session_maker = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    return _async_session_maker


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Async generator that yields a database session for FastAPI Depends().

    Use with FastAPI's Depends() for automatic session lifecycle management.
    The session is committed on success and rolled back on exception.
    Session cleanup is guaranteed via finally block.

    Yields:
        AsyncSession: Database session for performing operations.

    Example:
        # FastAPI endpoint
        @app.get("/tasks")
        async def get_tasks(session: AsyncSession = Depends(get_session)):
            result = await session.execute(select(Task))
            return result.scalars().all()
    """
    session_maker = _get_session_maker()
    session = session_maker()

    try:
        yield session
        await session.commit()
    except Exception as e:
        await session.rollback()
        logger.error(f"Session error, rolled back: {e}")
        raise
    finally:
        await session.close()


@asynccontextmanager
async def get_session_context() -> AsyncGenerator[AsyncSession, None]:
    """
    Async context manager that yields a database session.

    Use for direct context manager usage outside of FastAPI dependency injection.
    The session is committed on success and rolled back on exception.
    Session cleanup is guaranteed via finally block.

    Yields:
        AsyncSession: Database session for performing operations.

    Example:
        async with get_session_context() as session:
            result = await session.execute(select(Task))
            return result.scalars().all()
    """
    session_maker = _get_session_maker()
    session = session_maker()

    try:
        yield session
        await session.commit()
    except Exception as e:
        await session.rollback()
        logger.error(f"Session error, rolled back: {e}")
        raise
    finally:
        await session.close()


async def init_db() -> None:
    """
    Initialize the database by creating all tables.

    Uses SQLModel metadata to create tables if they don't exist.
    This operation is idempotent - safe to call multiple times.

    Note: Foreign key constraints to users table will fail until
    Module 3 (Authentication) creates the users table.

    Raises:
        Exception: If table creation fails.

    Example:
        # On application startup
        await init_db()
    """
    engine = get_engine()

    try:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise


async def close_db() -> None:
    """
    Close the database engine and all connections.

    Should be called on application shutdown to ensure
    clean release of database connections.

    Example:
        # On application shutdown
        await close_db()
    """
    global _engine, _async_session_maker

    if _engine is not None:
        await _engine.dispose()
        _engine = None
        _async_session_maker = None
        logger.info("Database connections closed")


# Public exports
__all__ = [
    "get_engine",
    "get_session",
    "get_session_context",
    "init_db",
    "close_db",
]
