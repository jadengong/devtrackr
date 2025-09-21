"""Add full-text search index for tasks

Revision ID: add_fulltext_search_index
Revises:
Create Date: 2024-01-15 12:00:00.000000

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "add_fulltext_search_index"
down_revision = "d195cb179a74"  # Links to the time tracking migration
branch_labels = None
depends_on = None


def upgrade():
    """Add full-text search index for tasks."""
    import os

    # Skip PostgreSQL-specific features if not using PostgreSQL
    skip_postgres_features = (
        os.getenv("SKIP_POSTGRES_FEATURES", "false").lower() == "true"
    )

    if skip_postgres_features:
        print("Skipping PostgreSQL-specific full-text search indexes (using SQLite)")
        return

    # Create a GIN index for full-text search on title and description
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_tasks_fulltext_search 
        ON tasks USING gin(to_tsvector('english', title || ' ' || COALESCE(description, '')))
    """
    )

    # Create a separate index for case-insensitive search
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_tasks_title_description_gin 
        ON tasks USING gin((title || ' ' || COALESCE(description, '')) gin_trgm_ops)
    """
    )


def downgrade():
    """Remove full-text search indexes."""
    import os

    # Skip PostgreSQL-specific features if not using PostgreSQL
    skip_postgres_features = (
        os.getenv("SKIP_POSTGRES_FEATURES", "false").lower() == "true"
    )

    if skip_postgres_features:
        print(
            "Skipping PostgreSQL-specific full-text search index removal (using SQLite)"
        )
        return

    op.execute("DROP INDEX IF EXISTS idx_tasks_fulltext_search")
    op.execute("DROP INDEX IF EXISTS idx_tasks_title_description_gin")
