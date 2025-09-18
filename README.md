# DevTrackr API

A comprehensive task management API built with FastAPI, featuring user authentication, task priorities, and analytics. This is a backend-only project that provides a robust REST API for task management.

## 🚀 **CI/CD Pipeline Status**

This project now includes a complete CI/CD pipeline with:
- **Code Quality Checks**: Black, flake8, mypy, bandit, safety
- **Automated Testing**: pytest with coverage reporting
- **Database Migrations**: Automated validation and backup
- **Multi-Environment Deployment**: Staging and production with health checks

## 🏗️ **Architecture**

- **Backend**: FastAPI with SQLAlchemy ORM
- **Database**: PostgreSQL with Alembic migrations
- **Authentication**: JWT-based user authentication
- **Containerization**: Docker with health checks
- **CI/CD**: GitHub Actions workflows

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.8 or higher
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

- **Database connection issues**: Ensure Docker is running and the database container is healthy
- **Port already in use**: Change the port with `--port 8001` or stop the service using port 8000
- **Migration errors**: Check that the database is running and accessible
- **Import errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`

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
```

### **Alternative Startup Methods**

**Using Python directly (not recommended for development):**
```bash
python main.py
```

**Using uvicorn with custom settings:**
```bash
# Development with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production settings
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 🧪 **Testing**

Run the test suite:
```bash
python run_tests.py
```

## 🐳 **Docker**

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

### **Docker Compose for Full Stack**

The `docker-compose.yml` file includes:
- PostgreSQL database with persistent storage
- Health checks for database readiness
- Proper networking between services

## 📊 **Features**

- **Task Management**: Create, read, update, delete tasks with full CRUD operations
- **Full-Text Search**: Powerful search across task titles and descriptions with relevance ranking
- **Cursor-Based Pagination**: Efficient pagination for large task datasets
- **User Authentication**: JWT-based secure authentication
- **Task Priorities**: Low, Medium, High, Urgent priority levels
- **Time Tracking**: Estimate and track actual time spent with detailed analytics
- **Analytics**: Comprehensive metrics and productivity insights
- **Categories**: Organize tasks by category
- **Archiving**: Soft delete functionality
- **Advanced Filtering**: Filter tasks by status, category, priority, and date ranges

## 🔧 **API Endpoints**

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

### **Analytics**
- `GET /metrics/summary` - Task summary
- `GET /metrics/categories` - Category breakdown
- `GET /metrics/weekly` - Weekly statistics
- `GET /metrics/time-efficiency` - Time tracking metrics
- `GET /metrics/productivity-trends` - Productivity trends

### **Health**
- `GET /health` - API health status

## 🔍 **Search Examples**

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
- **Relevance ranking** - most relevant results first
- **Advanced filtering** - combine search with status, category, priority filters
- **Search suggestions** - get suggestions based on existing content
- **Performance optimized** - uses PostgreSQL GIN indexes
- **Query normalization** - handles special characters automatically

## 🚀 **CI/CD Pipeline**

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

## 📝 **Development**

### **Code Quality**
```bash
# Format code
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

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and quality checks
5. Submit a pull request

## 📄 **License**

This project is licensed under the MIT License.
