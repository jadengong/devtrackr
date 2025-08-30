# DevTrackr

A comprehensive task management API built with FastAPI, featuring user authentication, task priorities, and analytics.

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

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/devtrackr-repo.git
   cd devtrackr-repo
   ```

2. **Set up environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Database setup**
   ```bash
   # Run migrations
   python -m alembic upgrade head
   ```

4. **Start the API**
   ```bash
   python main.py
   ```

5. **Access the API**
   - **API Documentation**: http://localhost:8000/docs
   - **Health Check**: http://localhost:8000/health

## 🧪 **Testing**

Run the test suite:
```bash
python run_tests.py
```

## 🐳 **Docker**

Build and run with Docker:
```bash
# Build image
docker build -t devtrackr .

# Run container
docker run -d -p 8000:8000 --name devtrackr-api devtrackr

# Check health
curl http://localhost:8000/health
```

## 📊 **Features**

- **Task Management**: Create, read, update, delete tasks
- **User Authentication**: JWT-based secure authentication
- **Task Priorities**: Low, Medium, High, Urgent priority levels
- **Time Tracking**: Estimate and track actual time spent
- **Analytics**: Comprehensive metrics and productivity insights
- **Categories**: Organize tasks by category
- **Archiving**: Soft delete functionality

## 🔧 **API Endpoints**

### **Authentication**
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user

### **Tasks**
- `GET /tasks` - List user's tasks
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
