from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import sys
import os
from pathlib import Path

# 1. Pastikan path mengarah ke root directory (backend) agar modul 'app' terbaca
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import settings
from app.database import Base

# 2. IMPORT SEMUA MODEL DI SINI
# Ini sangat penting agar Alembic mendeteksi tabel untuk 'autogenerate'
from app.models.user import User, Company, Department, Position, WorkStatus
from app.models.vehicle import Vehicle
from app.models.checklist import ChecklistTemplate
from app.models.p2h import P2HReport, P2HDetail, P2HDailyTracker
from app.models.notification import TelegramNotification

# this is the Alembic Config object
config = context.config

# ==================================================================================
# 3. LOGIKA PERBAIKAN URL (FIX ASYNC DRIVER & RAILWAY)
# ==================================================================================
def get_db_url():
    """
    Mengambil URL dari settings dan membersihkannya agar kompatibel dengan Alembic.
    Alembic butuh driver SYNC (psycopg2), bukan ASYNC (asyncpg).
    """
    url = settings.DATABASE_URL
    
    if not url:
        return ""

    # FIX 1: Hapus driver async (+asyncpg) agar menjadi sync standar
    # Mengubah 'postgresql+asyncpg://...' menjadi 'postgresql://...'
    if "postgresql+asyncpg://" in url:
        url = url.replace("postgresql+asyncpg://", "postgresql://")
    
    # FIX 2: Handle format legacy Railway/Heroku
    # Mengubah 'postgres://...' menjadi 'postgresql://...'
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
        
    return url

# Set URL database yang sudah diperbaiki ke konfigurasi Alembic
config.set_main_option("sqlalchemy.url", get_db_url())

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 4. Ambil metadata dari Base yang sudah merekam semua model di atas
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    # Ambil URL yang sudah difix oleh fungsi get_db_url() via config
    url = config.get_main_option("sqlalchemy.url")
    
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode with retry logic for Railway."""
    import time
    from sqlalchemy import text, inspect as sa_inspect
    
    # Ambil section konfigurasi dari file .ini
    configuration = config.get_section(config.config_ini_section) or {}
    
    # PAKSA URL menggunakan yang sudah kita fix (Sync driver)
    # Ini memastikan engine_from_config tidak membaca ulang URL async yang salah
    db_url = get_db_url()
    configuration["sqlalchemy.url"] = db_url
    
    # Log connection attempt
    print(f"Attempting database connection...")
    print(f"URL format check: {'postgresql://' in db_url if db_url else 'URL is empty'}")

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    # =========================================================
    # FIX: Handle problematic alembic versions BEFORE migration
    # =========================================================
    def fix_problematic_versions(connection):
        """Remove alembic versions that no longer exist in migration files"""
        try:
            inspector = sa_inspect(connection)
            tables = inspector.get_table_names()
            
            if "alembic_version" not in tables:
                return  # No alembic_version table yet
            
            # List of problematic versions that might exist in DB but not in files
            problematic_versions = [
                'telegram_users_001',
                'create_telegram_users',
            ]
            
            result = connection.execute(text("SELECT version_num FROM alembic_version"))
            current_versions = [row[0] for row in result.fetchall()]
            
            for version in current_versions:
                if version in problematic_versions:
                    print(f"⚠️  Found problematic alembic version: {version}")
                    connection.execute(
                        text("DELETE FROM alembic_version WHERE version_num = :version"),
                        {"version": version}
                    )
                    connection.commit()
                    print(f"✅ Deleted problematic version: {version}")
                    
                    # Check if we need to insert a valid version
                    result = connection.execute(text("SELECT COUNT(*) FROM alembic_version"))
                    count = result.scalar()
                    
                    if count == 0:
                        # Insert the last known good version
                        connection.execute(
                            text("INSERT INTO alembic_version (version_num) VALUES ('a553b45fe239')")
                        )
                        connection.commit()
                        print("✅ Stamped to 'a553b45fe239' (last known good version)")
        except Exception as e:
            print(f"⚠️  Could not fix alembic versions: {str(e)}")

    # Retry logic for Railway internal networking
    max_retries = 3
    retry_delay = 5  # seconds
    
    # First, try to fix any problematic versions before running migrations
    try:
        with connectable.connect() as connection:
            fix_problematic_versions(connection)
    except Exception as e:
        print(f"⚠️  Pre-migration fix attempt failed: {e}")
    
    for attempt in range(max_retries):
        try:
            with connectable.connect() as connection:
                # Fix problematic versions again in case first attempt failed
                fix_problematic_versions(connection)
                
                context.configure(
                    connection=connection, 
                    target_metadata=target_metadata
                )

                with context.begin_transaction():
                    context.run_migrations()
            print("Migration completed successfully!")
            return  # Success, exit the function
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Connection attempt {attempt + 1} failed: {e}")
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print(f"All {max_retries} connection attempts failed.")
                raise


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()