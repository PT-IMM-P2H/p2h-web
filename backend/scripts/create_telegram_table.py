"""
Script untuk memastikan tabel telegram_subscribers dibuat dengan benar.
Jalankan manual jika migrasi tidak berhasil membuat tabel.
"""
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text, inspect
from app.config import settings

def create_telegram_subscribers_table():
    """Buat tabel telegram_subscribers secara manual jika belum ada"""
    
    print("=" * 60)
    print("CREATE TELEGRAM_SUBSCRIBERS TABLE MANUALLY")
    print("=" * 60)
    
    engine = create_engine(settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://"))
    
    with engine.connect() as conn:
        # Check if table exists
        inspector = inspect(conn)
        tables = inspector.get_table_names()
        
        print(f"\n📋 Current tables: {tables}")
        
        if 'telegram_subscribers' not in tables:
            print("\n⚠️  Table 'telegram_subscribers' not found. Creating manually...")
            
            # Create table with exact same structure as migration
            create_sql = """
            CREATE TABLE telegram_subscribers (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                chat_id VARCHAR(100) NOT NULL UNIQUE,
                telegram_user_id BIGINT,
                telegram_username VARCHAR(255),
                full_name VARCHAR(255),
                chat_type VARCHAR(50) NOT NULL DEFAULT 'private',
                is_active BOOLEAN NOT NULL DEFAULT true,
                notes TEXT,
                subscribed_at TIMESTAMP NOT NULL DEFAULT now(),
                unsubscribed_at TIMESTAMP,
                last_notified_at TIMESTAMP
            );
            """
            
            conn.execute(text(create_sql))
            
            # Create indexes
            conn.execute(text(
                "CREATE INDEX ix_telegram_subscribers_chat_id ON telegram_subscribers (chat_id);"
            ))
            conn.execute(text(
                "CREATE INDEX ix_telegram_subscribers_is_active ON telegram_subscribers (is_active);"
            ))
            
            conn.commit()
            print("✅ Table 'telegram_subscribers' created successfully!")
            
            # Update alembic_version to latest
            conn.execute(text(
                "UPDATE alembic_version SET version_num = 'b7a2c3d4e5f6'"
            ))
            conn.commit()
            print("✅ Alembic version updated to 'b7a2c3d4e5f6'")
            
        else:
            print("\n✅ Table 'telegram_subscribers' already exists")
        
        # Final verification
        inspector = inspect(conn)
        tables = inspector.get_table_names()
        
        if 'telegram_subscribers' in tables:
            # Get table info
            columns = inspector.get_columns('telegram_subscribers')
            indexes = inspector.get_indexes('telegram_subscribers')
            
            print(f"\n📋 Table structure:")
            for col in columns:
                print(f"  - {col['name']}: {col['type']}")
            
            print(f"\n📋 Indexes:")
            for idx in indexes:
                print(f"  - {idx['name']}")
                
            print("\n" + "=" * 60)
            print("✅ SUCCESS: telegram_subscribers table ready!")
            print("=" * 60)
        else:
            print("\n❌ ERROR: Table creation failed")

if __name__ == "__main__":
    create_telegram_subscribers_table()