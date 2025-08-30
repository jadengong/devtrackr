import os
import pytest
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from dotenv import load_dotenv
from sqlalchemy import inspect

# Load environment variables from .env file
load_dotenv()

# Import your app and database components
from main import app
from db import Base
from deps import get_db, get_current_active_user
from models import User, Task

# Load test database URL from environment
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "sqlite:///./test.db")

# Create test engine with in-memory SQLite for faster tests
test_engine = create_engine(
    TEST_DATABASE_URL,
    poolclass=StaticPool,  # Use static pool for testing
    connect_args={"check_same_thread": False} if "sqlite" in TEST_DATABASE_URL else {},
)

# Create test session factory
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session")
def db_engine():
    """Create database engine once per test session."""
    # Use a completely in-memory SQLite database for testing
    # This ensures no file conflicts and completely fresh state each time
    from sqlalchemy import create_engine

    # Use :memory: for completely in-memory database
    temp_engine = create_engine("sqlite:///:memory:")

    # Drop all tables first to avoid index conflicts
    Base.metadata.drop_all(bind=temp_engine)

    # Create all tables fresh
    Base.metadata.create_all(bind=temp_engine)

    yield temp_engine

    # Clean up: close engine (no file to delete for in-memory)
    temp_engine.dispose()


@pytest.fixture(scope="function")
def db_session(db_engine) -> Generator[Session, None, None]:
    """Create a new database session for each test with automatic rollback."""
    connection = db_engine.connect()
    transaction = connection.begin()

    # Create a session bound to the transaction
    session = TestingSessionLocal(bind=connection)

    yield session

    # Rollback the transaction after each test
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def test_user(db_session) -> User:
    """Create a test user for authentication."""
    from deps import get_password_hash

    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=get_password_hash("testpassword123"),
        is_active=True,
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


@pytest.fixture(scope="function")
def client(db_session, test_user) -> Generator[TestClient, None, None]:
    """Create a test client with overridden database dependency and authentication."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass  # Don't close the session here, it's managed by the fixture

    def override_get_current_active_user():
        """Override authentication to return our test user."""
        return test_user

    # Override the dependencies
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_active_user] = override_get_current_active_user

    with TestClient(app) as test_client:
        yield test_client

    # Clear the dependency overrides
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def sample_task_data():
    """Provide sample task data for testing."""
    return {"title": "Test Task", "description": "This is a test task", "priority": 3}


@pytest.fixture(scope="function")
def sample_task(db_session, test_user, sample_task_data):
    """Create a sample task in the database for testing."""
    from models import Task, TaskStatus

    task = Task(
        title=sample_task_data["title"],
        description=sample_task_data["description"],
        status=TaskStatus.todo,
        priority=3,
        owner_id=test_user.id,
    )

    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    return task


@pytest.fixture(scope="function")
def multiple_tasks(db_session, test_user):
    """Create multiple tasks for testing list operations."""
    from models import Task, TaskStatus

    tasks = [
        Task(title="Task 1", status=TaskStatus.todo, priority=1, owner_id=test_user.id),
        Task(
            title="Task 2",
            status=TaskStatus.in_progress,
            priority=2,
            owner_id=test_user.id,
        ),
        Task(title="Task 3", status=TaskStatus.done, priority=3, owner_id=test_user.id),
    ]

    for task in tasks:
        db_session.add(task)

    db_session.commit()

    # Refresh all tasks to get their IDs
    for task in tasks:
        db_session.refresh(task)

    return tasks
