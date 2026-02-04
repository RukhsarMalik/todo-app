"""
Migration script to add Phase V columns to the existing tasks table.
Run this once to update the schema without losing existing data.
"""

import asyncio
import os
from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

async def migrate():
    """Add Phase V columns to tasks table."""
    engine = create_async_engine(DATABASE_URL, echo=True)

    async with engine.begin() as conn:
        # Check if priority column exists
        result = await conn.execute(text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'tasks' AND column_name = 'priority'
        """))

        if result.fetchone() is None:
            print("Adding Phase V columns to tasks table...")

            # Add priority column
            await conn.execute(text("""
                ALTER TABLE tasks
                ADD COLUMN IF NOT EXISTS priority VARCHAR(10) DEFAULT 'medium'
            """))
            print("  - Added priority column")

            # Add due_date column
            await conn.execute(text("""
                ALTER TABLE tasks
                ADD COLUMN IF NOT EXISTS due_date TIMESTAMP
            """))
            print("  - Added due_date column")

            # Add reminder_offset column
            await conn.execute(text("""
                ALTER TABLE tasks
                ADD COLUMN IF NOT EXISTS reminder_offset INTEGER DEFAULT 60
            """))
            print("  - Added reminder_offset column")

            # Add recurrence_rule column (JSON)
            await conn.execute(text("""
                ALTER TABLE tasks
                ADD COLUMN IF NOT EXISTS recurrence_rule JSONB
            """))
            print("  - Added recurrence_rule column")

            # Add next_occurrence column
            await conn.execute(text("""
                ALTER TABLE tasks
                ADD COLUMN IF NOT EXISTS next_occurrence TIMESTAMP
            """))
            print("  - Added next_occurrence column")

            # Add parent_task_id column (self-referencing FK)
            await conn.execute(text("""
                ALTER TABLE tasks
                ADD COLUMN IF NOT EXISTS parent_task_id INTEGER REFERENCES tasks(id) ON DELETE SET NULL
            """))
            print("  - Added parent_task_id column")

            # Create index on priority
            await conn.execute(text("""
                CREATE INDEX IF NOT EXISTS ix_tasks_priority ON tasks(priority)
            """))
            print("  - Created priority index")

            # Create index on due_date
            await conn.execute(text("""
                CREATE INDEX IF NOT EXISTS ix_tasks_due_date ON tasks(due_date)
            """))
            print("  - Created due_date index")

            # Create index on parent_task_id
            await conn.execute(text("""
                CREATE INDEX IF NOT EXISTS ix_tasks_parent_task_id ON tasks(parent_task_id)
            """))
            print("  - Created parent_task_id index")

            print("\nPhase V migration completed successfully!")
        else:
            print("Phase V columns already exist. No migration needed.")

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(migrate())
