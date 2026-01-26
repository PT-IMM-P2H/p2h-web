"""add_superadmin_to_userrole_enum

Revision ID: 9f7ccaf259eb
Revises: create_vehicle_types
Create Date: 2026-01-26 08:35:34.350647+08:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f7ccaf259eb'
down_revision = 'create_vehicle_types'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add 'superadmin' value to userrole enum if it doesn't exist
    # PostgreSQL requires special handling for enum alterations
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_enum 
                WHERE enumlabel = 'superadmin' 
                AND enumtypid = (
                    SELECT oid FROM pg_type WHERE typname = 'userrole'
                )
            ) THEN
                ALTER TYPE userrole ADD VALUE 'superadmin';
            END IF;
        END
        $$;
    """)


def downgrade() -> None:
    # Note: PostgreSQL doesn't support removing enum values directly
    # This would require recreating the enum type, which is complex
    # For safety, we'll leave the enum value in place
    pass
