"""create telegram_subscribers table for multi-user notifications

Revision ID: b7a2c3d4e5f6
Revises: a553b45fe239
Create Date: 2026-02-05 17:00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b7a2c3d4e5f6'
down_revision: Union[str, None] = 'a553b45fe239'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create telegram_subscribers table
    op.create_table(
        'telegram_subscribers',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('chat_id', sa.String(100), nullable=False),
        sa.Column('telegram_user_id', sa.BigInteger(), nullable=True),
        sa.Column('telegram_username', sa.String(255), nullable=True),
        sa.Column('full_name', sa.String(255), nullable=True),
        sa.Column('chat_type', sa.String(50), nullable=False, server_default='private'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('subscribed_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('unsubscribed_at', sa.DateTime(), nullable=True),
        sa.Column('last_notified_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('chat_id')
    )
    
    # Create index on chat_id for faster lookups
    op.create_index('ix_telegram_subscribers_chat_id', 'telegram_subscribers', ['chat_id'])
    
    # Create index on is_active for filtering active subscribers
    op.create_index('ix_telegram_subscribers_is_active', 'telegram_subscribers', ['is_active'])


def downgrade() -> None:
    op.drop_index('ix_telegram_subscribers_is_active', table_name='telegram_subscribers')
    op.drop_index('ix_telegram_subscribers_chat_id', table_name='telegram_subscribers')
    op.drop_table('telegram_subscribers')
