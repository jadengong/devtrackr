"""Add full-text search index for tasks

Revision ID: add_fulltext_search_index
Revises: 
Create Date: 2024-01-15 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_fulltext_search_index'
down_revision = None  # Update this to the latest revision
branch_labels = None
depends_on = None


def upgrade():
    """Add full-text search index for tasks."""
    # Create a GIN index for full-text search on title and description
    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_tasks_fulltext_search 
        ON tasks USING gin(to_tsvector('english', title || ' ' || COALESCE(description, '')))
    """)
    
    # Create a separate index for case-insensitive search
    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_tasks_title_description_gin 
        ON tasks USING gin((title || ' ' || COALESCE(description, '')) gin_trgm_ops)
    """)


def downgrade():
    """Remove full-text search indexes."""
    op.execute("DROP INDEX IF EXISTS idx_tasks_fulltext_search")
    op.execute("DROP INDEX IF EXISTS idx_tasks_title_description_gin")
