"""gabungkan branch yang konflik

Revision ID: efe1c8d232b9
Revises: create_vehicle_types, 98a0e7fba3a3
Create Date: 2026-01-30 11:37:17.223695+08:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'efe1c8d232b9'
down_revision = ('create_vehicle_types', '98a0e7fba3a3')
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
