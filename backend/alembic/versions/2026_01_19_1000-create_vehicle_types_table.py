"""create vehicle_types table

Revision ID: create_vehicle_types
Revises: 104cef69ee26
Create Date: 2026-01-19 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid

# revision identifiers, used by Alembic.
revision = 'create_vehicle_types'
down_revision = '104cef69ee26'
branch_labels = None
depends_on = None


def upgrade():
    # Create vehicle_types table
    op.create_table('vehicle_types',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('name', sa.String(length=100), nullable=False, unique=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
    )
    
    # Create index for name
    op.create_index('ix_vehicle_types_name', 'vehicle_types', ['name'])
    op.create_index('ix_vehicle_types_is_active', 'vehicle_types', ['is_active'])
    
    # Seed existing vehicle types from enum
    op.execute("""
        INSERT INTO vehicle_types (id, name, description, is_active, created_at, updated_at) VALUES
        (gen_random_uuid(), 'Light Vehicle', 'Kendaraan ringan untuk penggunaan umum', true, NOW(), NOW()),
        (gen_random_uuid(), 'Electric Vehicle', 'Kendaraan listrik ramah lingkungan', true, NOW(), NOW()),
        (gen_random_uuid(), 'Double Cabin', 'Kendaraan double cabin', true, NOW(), NOW()),
        (gen_random_uuid(), 'Single Cabin', 'Kendaraan single cabin', true, NOW(), NOW()),
        (gen_random_uuid(), 'Bus', 'Kendaraan bus penumpang', true, NOW(), NOW()),
        (gen_random_uuid(), 'Ambulance', 'Kendaraan ambulans medis', true, NOW(), NOW()),
        (gen_random_uuid(), 'Fire Truck', 'Kendaraan pemadam kebakaran', true, NOW(), NOW()),
        (gen_random_uuid(), 'Komando', 'Kendaraan komando', true, NOW(), NOW()),
        (gen_random_uuid(), 'Truk Sampah', 'Kendaraan pengangkut sampah', true, NOW(), NOW())
    """)


def downgrade():
    op.drop_index('ix_vehicle_types_is_active', table_name='vehicle_types')
    op.drop_index('ix_vehicle_types_name', table_name='vehicle_types')
    op.drop_table('vehicle_types')
