# DevTrackr API

A task management API built with FastAPI. Handles user auth, search, time tracking, and some basic analytics.


## **Architecture**

- **Backend**: FastAPI with SQLAlchemy ORM
- **Database**: PostgreSQL with Alembic migrations
- **Authentication**: JWT-based user authentication
- **Containerization**: Docker with health checks
- **CI/CD**: GitHub Actions workflows
- **Testing**: pytest with coverage reporting
- **Code Quality**: Black, flake8, mypy, bandit, safety

## **Project Structure**

```
devtrackr-repo/
├── core/                    # Core application components
│   ├── models.py           # SQLAlchemy ORM models
│   ├── schemas.py          # Pydantic request/response models
│   ├── db.py               # Database configuration
│   └── deps.py             # Dependency injection
├── config/                  # Configuration and middleware
│   ├── config.py           # Application settings
│   └── middleware.py       # Custom middleware
├── routers/                 # API route handlers
│   ├── auth.py             # Authentication endpoints
│   ├── tasks.py            # Task management endpoints
│   ├── time_tracking.py    # Time tracking endpoints
│   ├── metrics.py          # Analytics endpoints
│   └── activity.py         # Activity logging endpoints
├── services/                # Business logic services
│   └── activity_logger.py  # Activity logging service
├── utils/                   # Utility functions
│   ├── pagination.py       # Cursor-based pagination
│   ├── search_utils.py     # Full-text search utilities
│   └── utils.py            # General utilities
├── tests/                   # Unit tests
│   ├── test_tasks_api.py   # Task API tests
│   └── test_time_tracking.py # Time tracking tests
├── manual_tests/            # Integration tests (manual)
│   ├── pagination_integration_test.py
│   └── search_integration_test.py
├── demos/                   # Demo scripts and examples
├── docs/                    # Documentation
├── scripts/                 # Utility scripts
└── main.py                  # Application entry point
```

## **Quick Start**

### **Prerequisites**
- Python 3.11 or higher
- Docker and Docker Compose (for database)
- Git

### **Step-by-Step Setup**

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/devtrackr-repo.git
   cd devtrackr-repo
   ```

2. **Start the PostgreSQL database**
   ```bash
   # Start PostgreSQL using Docker Compose
   docker-compose up -d db
   
   # Verify database is running
   docker ps
   ```

3. **Set up Python environment**
   ```bash
   # Create virtual environment (recommended)
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```bash
   # Run database migrations
   python -m alembic upgrade head
   ```

5. **Start the FastAPI application**
   ```bash
   # Start the development server
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

6. **Access the API**
   - **API Documentation (Swagger UI)**: http://localhost:8000/docs
   - **Alternative API Docs (ReDoc)**: http://localhost:8000/redoc
   - **Health Check**: http://localhost:8000/health
   - **Root Endpoint**: http://localhost:8000/

### **Troubleshooting**

- **Database connection issues**: Check Docker is running and the database container is healthy
- **Port already in use**: Change the port with `--port 8001` or stop the service using port 8000
- **Migration errors**: Check that the database is running and accessible
- **Import errors**: Check that all dependencies are installed with `pip install -r requirements.txt`

### **Environment Variables**

The application uses the following environment variables (with defaults):

```bash
# Database Configuration
DATABASE_URL=postgresql+psycopg2://dev:dev@localhost:5432/devtrackr
POSTGRES_USER=dev
POSTGRES_PASSWORD=dev
POSTGRES_DB=devtrackr
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# JWT Configuration
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Testing
TEST_DATABASE_URL=sqlite:///:memory:
```

## **Testing**

### **Unit Tests**
Run the comprehensive test suite:
```bash
# Run all unit tests
python -m pytest

# Run tests with coverage
python -m pytest --cov=.

# Run specific test file
python -m pytest tests/test_tasks_api.py -v
```

### **Manual Integration Tests**
For testing API endpoints with a running server:
```bash
# Install requests (if not already installed)
pip install requests

# Start the server first
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Run integration tests (in separate terminal)
python manual_tests/pagination_integration_test.py
python manual_tests/search_integration_test.py
```

### **Test Runner Script**
Use the convenient test runner:
```bash
python scripts/run_tests.py
```

## 📊 **Features**

### **Core Functionality**
- **Task Management**: Full CRUD operations with priorities, categories, and status tracking
- **User Authentication**: JWT-based secure authentication with registration and login
- **Time Tracking**: Estimate and track actual time spent with detailed analytics
- **Activity Logging**: Comprehensive audit trail for all user actions

### **Advanced Features**
- **Full-Text Search**: PostgreSQL-powered search with relevance ranking and suggestions
- **Cursor-Based Pagination**: Efficient pagination for large datasets
- **Advanced Filtering**: Filter by status, category, priority, and date ranges
- **Analytics & Metrics**: Comprehensive productivity insights and reporting
- **Task Archiving**: Soft delete functionality for data retention

### **Developer Experience**
- **Auto-generated Documentation**: Interactive API docs with Swagger UI and ReDoc
- **Type Safety**: Full type hints with Pydantic models and SQLAlchemy ORM
- **Code Quality**: Automated formatting, linting, and security scanning
- **Comprehensive Testing**: Unit tests with coverage reporting
- **Docker Support**: Easy deployment with Docker and Docker Compose

## **API Endpoints**

### **Authentication**
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user

### **Tasks**
- `GET /tasks` - List user's tasks (with pagination and filtering)
- `GET /tasks/search` - Full-text search across tasks
- `POST /tasks` - Create new task
- `GET /tasks/{task_id}` - Get specific task
- `PATCH /tasks/{task_id}` - Update task
- `DELETE /tasks/{task_id}` - Delete task
- `POST /tasks/{task_id}/archive` - Archive task

### **Time Tracking**
- `POST /time-tracking/start` - Start timer for task
- `POST /time-tracking/stop` - Stop active timer
- `GET /time-tracking/active` - Get active timer
- `GET /time-tracking/entries` - List time entries
- `GET /time-tracking/summary` - Time tracking summary

### **Analytics**
- `GET /metrics/summary` - Task summary statistics
- `GET /metrics/categories` - Category breakdown
- `GET /metrics/weekly` - Weekly statistics
- `GET /metrics/time-efficiency` - Time tracking metrics
- `GET /metrics/productivity-trends` - Productivity trends

### **Activity Logging**
- `GET /activity` - Get user activity log

### **Health**
- `GET /health` - API health status
- `GET /utils/demo` - Utility functions demo

## **Search Examples**

DevTrackr includes powerful full-text search capabilities:

```bash
# Basic search
GET /tasks/search?q=API documentation

# Search with filters
GET /tasks/search?q=review&status=todo&priority=high

# Search with date filters
GET /tasks/search?q=deadline&due_after=2024-01-01&due_before=2024-12-31

# Search with suggestions
GET /tasks/search?q=doc&include_suggestions=true
```

**Search Features:**
- **Relevance ranking** - Most relevant results first
- **Advanced filtering** - Combine search with status, category, priority filters
- **Search suggestions** - Get suggestions based on existing content
- **Performance optimized** - Uses PostgreSQL GIN indexes
- **Query normalization** - Handles special characters automatically

## **Docker**

### **Development with Docker Compose (Recommended)**

The easiest way to run the entire application stack:

```bash
# Start both database and application
docker-compose up

# Or run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

### **Production Docker Build**

Build and run the application container:

```bash
# Build the application image
docker build -t devtrackr .

# Run the container
docker run -d -p 8000:8000 --name devtrackr-api devtrackr

# Check health
curl http://localhost:8000/health

# View logs
docker logs devtrackr-api

# Stop container
docker stop devtrackr-api
```

## **CI/CD Pipeline**

The project includes automated workflows for:

1. **Code Quality** (`.github/workflows/quality.yml`)
   - Formatting with Black
   - Linting with flake8
   - Type checking with mypy
   - Security scanning with bandit
   - Dependency vulnerability checks with safety

2. **Database Migrations** (`.github/workflows/migrations.yml`)
   - Migration validation
   - History tracking
   - Backup creation

3. **Deployment** (`.github/workflows/deploy.yml`)
   - Multi-environment deployment
   - Health checks
   - Rollback capabilities

## **Development**

### **Code Quality**
```bash
# Format code with Black
python -m black .

# Check linting
python -m flake8 .

# Type checking
python -m mypy .

# Security scan
python -m bandit -r .
```

### **Database Migrations**
```bash
# Create new migration
python -m alembic revision --autogenerate -m "description"

# Apply migrations
python -m alembic upgrade head

# Rollback migration
python -m alembic downgrade -1
```

### **Demo Scripts**
Explore the API with interactive demos:
```bash
# Run comprehensive demo
python demos/demo_summary.py

# Explore specific features
python demos/basic_demo.py
python demos/search_capabilities.py
python demos/activity_logging.py
```

## **Documentation**

- **API Documentation**: Auto-generated at `/docs` and `/redoc`
- **Development Guide**: `docs/DEVELOPMENT.md`
- **Demo Examples**: `demos/` directory with working examples
- **Manual Tests**: `manual_tests/` directory for integration testing

## **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and quality checks
5. Submit a pull request

### **Development Workflow**
```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests
python -m pytest

# Format code
python -m black .

# Check code quality
python -m flake8 .
```

## **License**

This project is licensed under the MIT License.

---

**DevTrackr** - A comprehensive, production-ready task management API built with modern Python technologies.