"""add custom_user_name to vehicles

Revision ID: add_custom_user_name
Revises: d17ae8e60130
Create Date: 2026-02-03 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_custom_user_name'
down_revision = 'd17ae8e60130'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add custom_user_name column to vehicles table
    op.add_column('vehicles', sa.Column('custom_user_name', sa.String(100), nullable=True))


def downgrade() -> None:
    # Remove custom_user_name column from vehicles table
    op.drop_column('vehicles', 'custom_user_name')
