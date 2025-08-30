# DevTrackr Learning Log

This document tracks my progress as I build DevTrackr, a FastAPI-based task tracking API.

---

## Day 1 — Project Kickoff
- Set up FastAPI app with:
  - `/` → homepage
  - `/hello` → hello world
  - `/time?format=iso|seconds` → UTC time with query parameter
- Learned:
  - How FastAPI routes are defined with decorators
  - What `Literal` does for query params (`"iso" | "seconds"`)
  - Difference between path params, query params, and request body
- Challenge:
  - Didn't understand why `utcnow()` was flagged → learned to use `datetime.now(timezone.utc)`
- Next:
  - Add `POST /tasks` with in-memory storage

---

## Day 2 — Tasks CRUD Begins
- Added:
  - `POST /tasks` → create task (with id, title, description, category, status)
  - `GET /tasks` → list all tasks
- Learned:
  - How to use Pydantic models (`BaseModel`) for input validation
  - Why `.venv` should be ignored in Git with `.gitignore`
  - FastAPI automatically returns 422 on validation errors
- Challenge:
  - My tasks disappeared after restart → realized in-memory data clears on reload
  - PowerShell JSON escaping with curl was tricky
- Next:
  - Add `GET /tasks/{id}` for fetching a single task

---

## Day 3 — Full CRUD + Data Structure Upgrade
- Added:
  - `GET /tasks/{id}` → fetch single task by id (404 if not found)
  - `PATCH /tasks/{id}` → partial update using `model_dump(exclude_unset=True)`
  - `DELETE /tasks/{id}` → delete a task (204 No Content)
  - Switched storage from list to dict for O(1) lookups
- Learned:
  - What `HTTPException` is and why to raise it instead of returning an error JSON
  - Difference between "unset" vs "None" in PATCH requests
  - Dict lookups make code much cleaner than list loops
- Challenge:
  - At first I put `raise HTTPException` inside the loop → realized it needs to be after the loop
  - Needed to understand why `.model_dump(exclude_unset=True)` is crucial for PATCH
- Next:
  - Add filters to `GET /tasks` (e.g. `?status=todo&category=work`)
  - Prepare for database (PostgreSQL) integration later

## Day 4 — Filtering and Preparation for Tests
- Added:
  - Query parameter filters to `GET /tasks` (by `status` and `category`)
  - Restricted `status` filter with `Literal["todo", "doing", "done"]` so invalid values return 422
- Learned:
  - How query parameters can modify list endpoints
  - How `Literal` enforces valid choices and automatically rejects bad inputs
  - Why filtering logic usually starts with the full dataset and then applies conditions step by step
- Challenge:
  - Needed to understand the difference between "optional param not provided" vs. "param provided with bad value"
- Next:
  - Add basic tests with pytest to check `/time` and full task lifecycle

## Day 5 — Testing
- Added:
  - Basic pytest setup with `TestClient`
  - Tests for `/time` endpoint
  - Tests for tasks lifecycle (`POST`, `GET`, `GET by id`)
- Learned:
  - How to structure tests in a separate `tests/` folder
  - Why a reset helper is needed so tests don't interfere with each other
  - How `pytest` automatically discovers and runs test files
- Challenge:
  - Initially ran into import errors (`ModuleNotFoundError`) and a SyntaxError from `_reset_state_for_test`
  - Fixed by cleaning up `main.py` and keeping test code in its own files
- Next:
  - Consider adding pagination (`limit`, `offset`) to `GET /tasks`
  - Or move on to database integration with PostgreSQL and SQLAlchemy
  - Think that database integration is best for now to move on from the in-memory

## Day 6 — DB Integration Progress

- Added:
  - `.env` with `DATABASE_URL` and updated `db.py` for SQLAlchemy engine, `SessionLocal`, and `Base`.
  - `Task` ORM model in `models.py` with `TaskStatus` enum, timestamps, defaults, and indexes.
  - Alembic setup and first migration (`tasks` table + `task_status` enum).
  - Updated `main.py`, `routers/tasks.py`, `schemas.py`, and `deps.py` for DB-backed CRUD.
  - Verified endpoints via Swagger UI at `/docs`.

- Learned:
  - Alembic only detects models if they are imported in `env.py` (`import models`).
  - Why `server_default` is useful to keep defaults consistent between Python and Postgres.
  - How absolute imports (`from db import Base`) avoid `ImportError` compared to relative imports.
  - Swagger is a fast way to smoke-test new DB-backed endpoints.

- Challenge:
  - First Alembic revision was empty because models weren't imported.
  - Hit `ImportError` (`attempted relative import`) until switching to absolute paths.
  - Router collision (`tasks` dict vs `tasks` module) caused `"dict has no attribute router"`.

- Next:
  - Add pytest suite that uses a clean Postgres test DB.
  - Automate CRUD tests (`POST`, `GET`, `PATCH`, `DELETE`) instead of only Swagger.
  - Consider pagination (`limit`, `offset`) for `GET /tasks`.

## Day 7 — Authentication System & Testing Infrastructure

- Added:
  - **Complete JWT Authentication System:**
    - `User` model with secure password hashing using bcrypt
    - JWT token generation and validation with `python-jose`
    - Protected routes requiring authentication
    - User registration (`POST /auth/register`) and login (`POST /auth/login`)
  - **Enhanced Task Management:**
    - User ownership for all tasks (users can only see their own tasks)
    - Time tracking fields (`estimated_minutes`, `actual_minutes`)
    - Timer endpoints (`POST /tasks/{id}/start-timer`, `POST /tasks/{id}/stop-timer`)
    - Authorization checks (403 errors for unauthorized access)
  - **Robust Testing Infrastructure:**
    - `conftest.py` with database fixtures and authentication overrides
    - Test database isolation with automatic rollback
    - Authentication fixtures for testing protected endpoints
    - Comprehensive end-to-end API tests

- Learned:
  - **Security Best Practices:**
    - How to hash passwords with bcrypt and verify them securely
    - JWT token structure and expiration handling
    - Why `get_current_active_user` dependency protects routes
  - **Database Relationships:**
    - How to set up foreign keys between `User` and `Task` models
    - Cascade behavior for user deletion
    - Indexing strategies for performance (`ix_tasks_owner_status`)
  - **Testing with Authentication:**
    - How to override FastAPI dependencies in tests
    - Database transaction management for test isolation
    - Creating test users and tasks with proper relationships
  - **Command Line Tools:**
    - Using `python -m` for tools not in PATH (`python -m pytest`, `python -m alembic`)
    - Docker Compose for PostgreSQL database management

- Challenge:
  - **Authentication Integration:**
    - Initially all tests failed with 403 errors because endpoints required authentication
    - Had to understand how FastAPI dependency injection works for testing
    - Needed to override both `get_db` and `get_current_active_user` dependencies
  - **Database Setup:**
    - Docker Desktop wasn't running initially, causing connection errors
    - Alembic needed the database to be running to generate migrations
    - Had to learn the proper sequence: start Docker → run migration → test
  - **Import Dependencies:**
    - Added new packages (`bcrypt`, `python-jose`, `email-validator`, `passlib`)
    - Had to update requirements.txt and install all dependencies

- Next:
  - **Metrics & Analytics Endpoints:**
    - Task completion rates and time tracking analytics
    - Category breakdowns and weekly productivity reports
    - Performance dashboards for users
  - **Advanced Features:**
    - Task categories and tags for better organization
    - Due date management with reminders
    - Team collaboration features
  - **Production Readiness:**
    - Environment configuration management
    - Security hardening (rate limiting, CORS)
    - CI/CD pipeline with GitHub Actions

---

## Day 8 — Comprehensive Metrics & Analytics System

- Added:
  - **Complete Metrics Router** (`routers/metrics.py`) with 5 powerful analytics endpoints:
    - `GET /metrics/summary` → Task summary dashboard with completion rates and time totals
    - `GET /metrics/categories` → Category performance breakdown with time efficiency
    - `GET /metrics/weekly` → Weekly productivity trends with scoring algorithm (0-100 scale)
    - `GET /metrics/time-efficiency` → Time estimation accuracy analysis
    - `GET /metrics/productivity-trends` → Daily productivity tracking with trend analysis
  - **Enhanced Database Schema:**
    - Added `category` field to Task model with proper indexing
    - Created new database migration using Alembic
    - Enhanced table indexes for optimal query performance
  - **Advanced SQL Features:**
    - Complex aggregations using SQLAlchemy `func` module (`func.count()`, `func.sum()`, `func.avg()`)
    - Date-based grouping and filtering for trend analysis
    - Statistical calculations (completion rates, efficiency ratios, accuracy percentages)
    - Performance optimization with proper database indexing

- Learned:
  - **Advanced SQLAlchemy Techniques:**
    - How to use `func` module for complex database aggregations
    - Date/time handling in SQL queries for trend analysis
    - Proper indexing strategies for performance optimization
    - Database migration best practices with Alembic
  - **Business Intelligence Development:**
    - How to design meaningful metrics that provide actionable insights
    - Implementing scoring algorithms that balance multiple factors
    - Creating trend analysis that helps users track progress over time
    - Building category performance analysis for strategic decision making
  - **API Design Excellence:**
    - Comprehensive endpoint coverage for all analytics needs
    - Flexible query parameters allowing customizable analysis periods
    - Rich response models with detailed metrics and interpretations
    - Professional-grade documentation with clear endpoint descriptions

- Challenge:
  - **Database Schema Updates:**
    - Had to create and apply new Alembic migration for category field
    - Ensured backward compatibility for existing data
    - Tested migration process with Docker database
  - **Advanced SQL Queries:**
    - Initially struggled with complex aggregations and date grouping
    - Had to learn proper SQLAlchemy `func` syntax for statistical calculations
    - Needed to optimize queries for performance with proper indexing
  - **Business Logic Implementation:**
    - Designing meaningful productivity scoring algorithms
    - Balancing multiple metrics (completion rate, time efficiency, accuracy)
    - Creating trend analysis that provides actionable insights

- Next:
  - **Frontend Dashboard:**
    - React or Vue web interface for metrics visualization
    - Charts and graphs for productivity trends
    - Interactive dashboards for real-time insights
  - **Advanced Analytics:**
    - Machine learning insights and predictive modeling
    - Personalized productivity recommendations
    - Team collaboration and shared analytics
  - **Production Features:**
    - Rate limiting and CORS configuration
    - Monitoring and logging for analytics endpoints
    - CI/CD pipeline with automated testing

---

## Project Status Summary

### ✅ **Completed Features:**
- **Core API:** FastAPI with automatic OpenAPI documentation
- **Database:** PostgreSQL + SQLAlchemy ORM with Alembic migrations
- **Authentication:** JWT-based user system with secure password hashing
- **Task Management:** Full CRUD operations with user ownership
- **Time Tracking:** Estimated vs actual time tracking with timer endpoints
- **Testing:** Comprehensive test suite with authentication and database fixtures
- **Infrastructure:** Docker containerization and dependency management

### 🎯 **Current Architecture:**
- **Backend:** FastAPI with modular router structure
- **Database:** PostgreSQL with SQLAlchemy 2.0
- **Authentication:** JWT tokens with bcrypt password hashing
- **Testing:** pytest with database isolation and authentication overrides
- **Documentation:** Auto-generated OpenAPI/Swagger at `/docs`

### 🚀 **Ready for Production:**
- Secure user authentication and authorization
- Database-driven architecture with proper relationships
- Comprehensive test coverage
- Containerized deployment with Docker
- Clean, maintainable code structure

### 📚 **Skills Demonstrated:**
- **Backend Development:** FastAPI, SQLAlchemy, PostgreSQL
- **Security:** JWT authentication, password hashing, authorization
- **Testing:** pytest, test fixtures, database testing
- **DevOps:** Docker, Docker Compose, dependency management
- **API Design:** RESTful endpoints, validation, error handling

