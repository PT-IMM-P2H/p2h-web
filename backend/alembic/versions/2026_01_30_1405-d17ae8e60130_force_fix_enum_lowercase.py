"""force_fix_enum_lowercase

Revision ID: (biarkan kode acak bawaan file ini)
Revises: 9f7ccaf259eb
Create Date: 2026-01-30 ...

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '...' # JANGAN UBAH INI (Biarkan bawaan file)
down_revision = '9f7ccaf259eb' # INI KUNCINYA! Kita sambung manual ke posisi Railway.
branch_labels = None
depends_on = None

def upgrade() -> None:
    # 1. Ubah kolom role jadi TEXT sementara agar data aman & fleksibel
    op.execute("ALTER TABLE users ALTER COLUMN role TYPE VARCHAR(50)")

    # 2. Hancurkan tipe ENUM lama yang bermasalah (entah isinya apa, kita reset)
    op.execute("DROP TYPE IF EXISTS userrole CASCADE")

    # 3. Buat tipe ENUM baru yang BENAR (Lowercase semua: 'user', bukan 'User')
    op.execute("CREATE TYPE userrole AS ENUM('superadmin', 'admin', 'user', 'viewer')")

    # 4. Kembalikan kolom ke tipe ENUM baru
    # FUNGSI LOWER() akan mengubah 'User' jadi 'user' otomatis.
    op.execute("""
        ALTER TABLE users 
        ALTER COLUMN role TYPE userrole 
        USING LOWER(role::text)::userrole
    """)

    # 5. Set default agar aman kedepannya
    op.execute("ALTER TABLE users ALTER COLUMN role SET DEFAULT 'user'::userrole")

def downgrade() -> None:
    # Rollback logic (semoga tidak perlu dipakai)
    op.execute("ALTER TABLE users ALTER COLUMN role TYPE VARCHAR(50)")
    op.execute("DROP TYPE IF EXISTS userrole CASCADE")
    # Kembalikan ke asumsi lama (Mixed Case)
    op.execute("CREATE TYPE userrole AS ENUM('superadmin', 'admin', 'User', 'Viewer')")
    op.execute("""
        ALTER TABLE users 
        ALTER COLUMN role TYPE userrole 
        USING role::text::userrole
    """)