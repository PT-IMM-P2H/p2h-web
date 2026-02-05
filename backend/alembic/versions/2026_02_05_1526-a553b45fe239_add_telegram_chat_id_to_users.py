"""add_telegram_chat_id_to_users

Revision ID: a553b45fe239
Revises: add_custom_user_name
Create Date: 2026-02-05 15:26:00.960194+08:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a553b45fe239'
down_revision = 'add_custom_user_name'
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
