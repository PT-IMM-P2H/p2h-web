from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
import sys

# Validate DATABASE_URL before creating engine
if not settings.DATABASE_URL:
    print("ERROR: DATABASE_URL environment variable is not set!", file=sys.stderr)
    print("Please set DATABASE_URL in your environment variables.", file=sys.stderr)
    print("Example: postgresql://user:password@host:5432/database", file=sys.stderr)
    sys.exit(1)

# Create database engine
try:
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,  # Verify connections before using
        pool_size=5,  # Connection pool size
        max_overflow=10,  # Max additional connections
        pool_timeout=30,  # Timeout for getting connection from pool
        pool_recycle=1800,  # Recycle connections after 30 minutes
        echo=not settings.is_production  # Log SQL in development
    )
except Exception as e:
    print(f"ERROR: Failed to create database engine: {e}", file=sys.stderr)
    print(f"DATABASE_URL format check - starts with 'postgresql': {settings.DATABASE_URL.startswith('postgresql') if settings.DATABASE_URL else False}", file=sys.stderr)
    sys.exit(1)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()


# Dependency to get database session
def get_db():
    """
    Dependency function to get database session.
    Yields a session and closes it after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
