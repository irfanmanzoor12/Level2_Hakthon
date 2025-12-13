"""
One-time database migrations for adding new columns.
This runs on app startup to ensure schema is up-to-date.
"""
from sqlalchemy import text, inspect
from .database import engine


def run_migrations():
    """Run pending database migrations."""
    print("Checking for pending migrations...")

    with engine.connect() as conn:
        inspector = inspect(engine)

        # Check if tasks table exists
        if 'tasks' in inspector.get_table_names():
            columns = {col['name'] for col in inspector.get_columns('tasks')}

            # Add due_date column if missing
            if 'due_date' not in columns:
                print("Adding due_date column to tasks table...")
                conn.execute(text(
                    "ALTER TABLE tasks ADD COLUMN due_date DATE"
                ))
                conn.commit()
                print("✓ Added due_date column")

            # Add tags column if missing
            if 'tags' not in columns:
                print("Adding tags column to tasks table...")
                conn.execute(text(
                    "ALTER TABLE tasks ADD COLUMN tags JSON DEFAULT '[]'::json"
                ))
                conn.commit()
                print("✓ Added tags column")

        print("✓ Migrations complete")
