"""
Database validation script.

This script validates the database setup by performing:
1. Connection test
2. Table creation verification
3. Task insert operation
4. Task query operation
5. Cleanup (delete test data)

Usage:
    uv run python test_db.py

Prerequisites:
    - .env file with DATABASE_URL configured
    - Database tables created (run init_db.py first)
"""

import asyncio
import logging
import sys
from datetime import datetime, timezone

from sqlalchemy import text
from sqlmodel import select

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Test user ID for validation
TEST_USER_ID = "test_user_validation_script"


async def test_connection() -> bool:
    """Test database connection."""
    logger.info("Testing database connection...")

    try:
        from db import get_engine

        engine = get_engine()

        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            row = result.fetchone()
            assert row[0] == 1

        logger.info("✓ Connection test passed")
        return True

    except Exception as e:
        logger.error(f"✗ Connection test failed: {e}")
        return False


async def test_table_exists() -> bool:
    """Verify tasks table exists."""
    logger.info("Verifying tasks table exists...")

    try:
        from db import get_engine

        engine = get_engine()

        async with engine.connect() as conn:
            result = await conn.execute(
                text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables
                    WHERE table_name = 'tasks'
                )
                """)
            )
            exists = result.scalar()

        if exists:
            logger.info("✓ Tasks table exists")
            return True
        else:
            logger.error("✗ Tasks table does not exist")
            return False

    except Exception as e:
        logger.error(f"✗ Table verification failed: {e}")
        return False


async def test_insert_task() -> int | None:
    """Test inserting a task."""
    logger.info("Testing task insert...")

    try:
        from db import _get_session_maker
        from models import Task

        task = Task(
            user_id=TEST_USER_ID,
            title="Test Task from Validation Script",
            description="This is a test task created by test_db.py",
            completed=False
        )

        session_maker = _get_session_maker()
        async with session_maker() as session:
            session.add(task)
            await session.commit()
            await session.refresh(task)
            task_id = task.id

        logger.info(f"✓ Task inserted with ID: {task_id}")
        return task_id

    except Exception as e:
        logger.error(f"✗ Task insert failed: {e}")
        return None


async def test_query_task(task_id: int) -> bool:
    """Test querying a task by ID."""
    logger.info(f"Testing task query (ID: {task_id})...")

    try:
        from db import _get_session_maker
        from models import Task

        session_maker = _get_session_maker()
        async with session_maker() as session:
            statement = select(Task).where(Task.id == task_id)
            result = await session.execute(statement)
            task = result.scalar_one_or_none()

            if task is None:
                logger.error("✗ Task not found")
                return False

            # Verify task data
            assert task.user_id == TEST_USER_ID
            assert task.title == "Test Task from Validation Script"
            assert task.completed is False
            assert task.created_at is not None

            logger.info(f"✓ Task query passed: '{task.title}'")
            return True

    except AssertionError as e:
        logger.error(f"✗ Task data validation failed: {e}")
        return False
    except Exception as e:
        logger.error(f"✗ Task query failed: {e}")
        return False


async def test_query_by_user() -> bool:
    """Test querying tasks by user_id."""
    logger.info("Testing query by user_id...")

    try:
        from db import _get_session_maker
        from models import Task

        session_maker = _get_session_maker()
        async with session_maker() as session:
            statement = select(Task).where(Task.user_id == TEST_USER_ID)
            result = await session.execute(statement)
            tasks = result.scalars().all()

            if len(tasks) == 0:
                logger.error("✗ No tasks found for test user")
                return False

            logger.info(f"✓ Found {len(tasks)} task(s) for test user")
            return True

    except Exception as e:
        logger.error(f"✗ Query by user failed: {e}")
        return False


async def cleanup_test_data() -> bool:
    """Delete all test data created by this script."""
    logger.info("Cleaning up test data...")

    try:
        from db import _get_session_maker
        from models import Task

        session_maker = _get_session_maker()
        async with session_maker() as session:
            statement = select(Task).where(Task.user_id == TEST_USER_ID)
            result = await session.execute(statement)
            tasks = result.scalars().all()

            deleted_count = 0
            for task in tasks:
                await session.delete(task)
                deleted_count += 1

            await session.commit()

        logger.info(f"✓ Deleted {deleted_count} test task(s)")
        return True

    except Exception as e:
        logger.error(f"✗ Cleanup failed: {e}")
        return False


async def main() -> int:
    """
    Run all validation tests.

    Returns:
        int: Exit code (0 if all tests pass, 1 otherwise).
    """
    logger.info("=" * 50)
    logger.info("Database Validation Script")
    logger.info("=" * 50)

    tests_passed = 0
    tests_failed = 0

    try:
        # Test 1: Connection
        if await test_connection():
            tests_passed += 1
        else:
            tests_failed += 1
            logger.error("Stopping: Connection failed")
            return 1

        # Test 2: Table exists
        if await test_table_exists():
            tests_passed += 1
        else:
            tests_failed += 1
            logger.error("Run init_db.py first to create tables")
            return 1

        # Test 3: Insert
        task_id = await test_insert_task()
        if task_id:
            tests_passed += 1
        else:
            tests_failed += 1

        # Test 4: Query by ID
        if task_id and await test_query_task(task_id):
            tests_passed += 1
        else:
            tests_failed += 1

        # Test 5: Query by user
        if await test_query_by_user():
            tests_passed += 1
        else:
            tests_failed += 1

        # Cleanup
        if await cleanup_test_data():
            tests_passed += 1
        else:
            tests_failed += 1

    finally:
        # Close connections
        try:
            from db import close_db
            await close_db()
        except Exception:
            pass

    # Summary
    logger.info("=" * 50)
    logger.info("Validation Summary")
    logger.info("=" * 50)
    logger.info(f"Tests passed: {tests_passed}")
    logger.info(f"Tests failed: {tests_failed}")

    if tests_failed == 0:
        logger.info("=" * 50)
        logger.info("ALL TESTS PASSED! Database module is ready.")
        logger.info("=" * 50)
        return 0
    else:
        logger.error("=" * 50)
        logger.error("SOME TESTS FAILED. Check errors above.")
        logger.error("=" * 50)
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
