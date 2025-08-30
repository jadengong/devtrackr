import os
import pytest
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import your app and database components
from main import app
from db import Base
from deps import get_db

# Load test database URL from environment
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "sqlite:///./test.db")

# Create test engine with in-memory SQLite for faster tests
test_engine = create_engine(
    TEST_DATABASE_URL,
    poolclass=StaticPool,  # Use static pool for testing
    connect_args={"check_same_thread": False} if "sqlite" in TEST_DATABASE_URL else {}
)

# Create test session factory
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session")
def db_engine():
    """Create database engine once per test session."""
    # Create all tables
    Base.metadata.create_all(bind=test_engine)
    yield test_engine
    # Drop all tables after all tests
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def db_session(db_engine) -> Generator[Session, None, None]:
    """Create a new database session for each test with automatic rollback."""
    connection = test_engine.connect()
    transaction = connection.begin()
    
    # Create a session bound to the transaction
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    # Rollback the transaction after each test
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session) -> Generator[TestClient, None, None]:
    """Create a test client with overridden database dependency."""
    
    def override_get_db():
        try:
            yield db_session
        finally:
            pass  # Don't close the session here, it's managed by the fixture
    
    # Override the get_db dependency
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Clear the dependency override
    app.dependency_overrides.clear()
