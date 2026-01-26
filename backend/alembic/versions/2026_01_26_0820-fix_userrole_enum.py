"""fix_userrole_enum_add_superadmin

Revision ID: fix_userrole_enum
Revises: 2026_01_19_1000
Create Date: 2026-01-26 08:20:00.000000+08:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fix_userrole_enum'
down_revision = '104cef69ee26'  # Last migration
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Add 'superadmin' value to userrole enum if it doesn't exist
    """
    # Check if superadmin already exists, if not add it
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_enum 
                WHERE enumlabel = 'superadmin' 
                AND enumtypid = (SELECT oid FROM pg_type WHERE typname = 'userrole')
            ) THEN
                ALTER TYPE userrole ADD VALUE 'superadmin';
            END IF;
        END$$;
    """)


def downgrade() -> None:
    """
    Note: PostgreSQL doesn't support removing enum values directly.
    You would need to recreate the enum type to remove a value.
    """
    pass
