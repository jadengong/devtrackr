import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Prefer single DATABASE_URL, fall back to individual pieces if absent
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    user = os.getenv("POSTGRES_USER", "dev")
    pw = os.getenv("POSTGRES_PASSWORD", "dev")
    name = os.getenv("POSTGRES_DB", "devtrackr")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    DATABASE_URL = f"postgresql+psycopg2://{user}:{pw}@{host}:{port}/{name}"

# Manage connections/pool to psql
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Create short-lived sessions per req
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# All ORM models inherit from this so Alembic can find metadata
Base = declarative_base()
