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
    # Add telegram integration fields to users table
    op.add_column('users', sa.Column('telegram_chat_id', sa.String(length=100), nullable=True))
    op.add_column('users', sa.Column('telegram_username', sa.String(length=100), nullable=True))
    op.add_column('users', sa.Column('telegram_linked_at', sa.DateTime(), nullable=True))
    
    # Create unique index for telegram_chat_id
    op.create_index(op.f('ix_users_telegram_chat_id'), 'users', ['telegram_chat_id'], unique=True)


def downgrade() -> None:
    # Remove index and columns
    op.drop_index(op.f('ix_users_telegram_chat_id'), table_name='users')
    op.drop_column('users', 'telegram_linked_at')
    op.drop_column('users', 'telegram_username')
    op.drop_column('users', 'telegram_chat_id')
