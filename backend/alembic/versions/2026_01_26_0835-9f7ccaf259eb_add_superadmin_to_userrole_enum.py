"""add_superadmin_to_userrole_enum (stub for Railway compatibility)

Revision ID: 9f7ccaf259eb
Revises: create_vehicle_types
Create Date: 2026-01-26 08:35:34.350647+08:00

This is a stub migration file to maintain compatibility with Railway database
which has this revision ID recorded in alembic_version table.
The original migration logic has been superseded by d17ae8e60130_force_fix_enum_lowercase.

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f7ccaf259eb'
down_revision = 'create_vehicle_types'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Original logic moved to d17ae8e60130
    # This stub exists only for Railway alembic_version compatibility
    pass


def downgrade() -> None:
    pass
