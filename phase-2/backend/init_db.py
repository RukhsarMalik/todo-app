"""
Database initialization script.

Run this script to create all database tables in Neon PostgreSQL.
The script is idempotent - safe to run multiple times.

Usage:
    uv run python init_db.py

Prerequisites:
    - .env file with DATABASE_URL configured
    - Neon database provisioned and accessible
"""

import asyncio
import logging
import sys

# Configure logging before imports
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main() -> int:
    """
    Initialize the database tables.

    Returns:
        int: Exit code (0 for success, 1 for failure).
    """
    try:
        # Import here to ensure logging is configured first
        from db import init_db, close_db

        # Import models to register them with SQLModel metadata
        # This is required for create_all() to know about our tables
        from models import Task  # noqa: F401

        logger.info("Starting database initialization...")
        logger.info(f"Task model loaded: {Task.__tablename__}")

        # Create all tables
        await init_db()

        logger.info("=" * 50)
        logger.info("Database initialization completed successfully!")
        logger.info("=" * 50)
        logger.info("Tables created:")
        logger.info("  - tasks (with indexes on user_id and completed)")
        logger.info("")
        logger.info("Next steps:")
        logger.info("  1. Check Neon console to verify table exists")
        logger.info("  2. Run test_db.py to validate operations")
        logger.info("=" * 50)

        return 0

    except ValueError as e:
        # Configuration errors (missing DATABASE_URL, etc.)
        logger.error(f"Configuration error: {e}")
        return 1

    except Exception as e:
        # Database connection or creation errors
        logger.error(f"Database initialization failed: {e}")

        # Provide helpful message for FK constraint warning
        if "users" in str(e).lower():
            logger.warning(
                "Note: Foreign key to 'users' table will work after "
                "Module 3 (Authentication) creates the users table."
            )

        return 1

    finally:
        # Always clean up connections
        try:
            from db import close_db
            await close_db()
        except Exception:
            pass  # Ignore cleanup errors


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
