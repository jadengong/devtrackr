# DevTrackr Learning Log

This document tracks my progress as I build DevTrackr, a FastAPI-based task tracking API.

---

## Day 1 — Project Kickoff
- **Added:** Basic FastAPI app with `/`, `/hello`, and `/time?format=iso|seconds`.
- **Learned:** How to define routes, use `Literal` for query params, and handle UTC time correctly.
- **Challenge:** Confusion over `utcnow()` warning → fixed with `datetime.now(timezone.utc)`.
- **Next:** Add `POST /tasks` with in-memory storage.

---

## Day 2 — Tasks CRUD Begins
- **Added:** `POST /tasks` to create tasks and `GET /tasks` to list them.
- **Learned:** Using Pydantic models for validation, Gitignore for `.venv`, and FastAPI’s automatic 422 errors.
- **Challenge:** Tasks reset on reload (in-memory), JSON escaping in PowerShell was tricky.
- **Next:** Add `GET /tasks/{id}`.

---

## Day 3 — Full CRUD + Dict Storage
- **Added:** `GET /tasks/{id}`, `PATCH /tasks/{id}`, `DELETE /tasks/{id}`. Switched to dict storage for O(1) lookups.
- **Learned:** Why to use `HTTPException`, difference between unset vs None in PATCH, and efficiency of dict lookups.
- **Challenge:** Raised exceptions in wrong place at first; needed `model_dump(exclude_unset=True)` for PATCH.
- **Next:** Add filters and start prepping for DB integration.

---

## Day 4 — Filtering & Prep for Tests
- **Added:** Filters for `GET /tasks` (status, category) with `Literal` validation.
- **Learned:** How optional vs invalid query params are handled and step-by-step filtering logic.
- **Challenge:** Handling optional vs invalid params.
- **Next:** Add pytest tests for `/time` and tasks.

---

## Day 5 — Testing
- **Added:** Pytest setup with `TestClient`. Tests for `/time` and task lifecycle.
- **Learned:** Organizing tests in `tests/`, why reset helpers are needed, and pytest discovery rules.
- **Challenge:** Import errors and SyntaxError in `_reset_state_for_test`; fixed by cleaning up `main.py`.
- **Next:** Add pagination or move to Postgres integration (chose Postgres).

---

## Day 6 — DB Integration
- **Added:** `.env` with `DATABASE_URL`, SQLAlchemy engine/session/Base, `Task` ORM model, Alembic migration for tasks table + enum. Updated app to use DB CRUD. Verified in Swagger.
- **Learned:** Alembic requires importing models in `env.py`, value of `server_default`, why absolute imports matter, and quick Swagger smoke testing.
- **Challenge:** Empty migration until models imported, relative import errors, router name collision.
- **Next:** Add pytest suite with Postgres DB, automate CRUD tests, and consider pagination.

---

## Day 7 — Authentication & Testing Infrastructure
- **Added:** JWT auth with user registration/login, bcrypt password hashing, protected routes. Tasks now owned by users, with authorization checks. Timer endpoints for tasks. Built pytest setup with DB + auth overrides.
- **Learned:** Password hashing/verification, JWTs (structure + expiration), setting up foreign keys + cascade, and dependency overrides in tests.
- **Challenge:** All tests failed (403s) until overrides added, Docker had to be running for Alembic, new packages required updates.
- **Next:** Build metrics endpoints, add categories/tags, due dates, and prep production config/CI.

---

## Day 8 — Metrics & Analytics
- **Added:** Metrics router with summary, categories, weekly trends, time efficiency, and productivity trend endpoints. Added `category` field + migration + indexes.
- **Learned:** SQLAlchemy aggregations, date grouping, indexing strategies, and BI-style analytics design.
- **Challenge:** Writing/optimizing queries and migration handling.
- **Next:** Add frontend charts, refine metrics and indexing.

---

## Day 9 — Test Coverage & Runner
- **Added:** pytest-cov integration, coverage thresholds, multiple formats, `run_tests.py`, pytest.ini, .coveragerc.
- **Learned:** Enforcing coverage gates, excluding utility code, and integrating coverage tools.
- **Challenge:** Duplicate indexes and noisy coverage configs.
- **Next:** Raise coverage to 85%+, test auth + error handling.

---

## Day 10 — Router Integration
- **Added:** Integrated tasks, auth, metrics routers into `main.py`. All endpoints visible in Swagger with tags.
- **Learned:** Router inclusion, explicit imports, and Swagger tagging.
- **Challenge:** Endpoints invisible until routers explicitly included.
- **Next:** End-to-end testing of auth + metrics, validate edge cases.

---

## Day 11 — Priority Enum
- **Added:** `TaskPriority` enum (`low|medium|high|urgent`). Custom migration to convert int→enum. Updated schemas, API, and indexes.
- **Learned:** Complex migrations, enum defaults, validation, and indexing enums.
- **Challenge:** Auto-gen migration failed → needed custom casting + ordered migration.
- **Next:** Add priority filtering/sorting, analytics, and notifications.

---

## Day 12 — CI/CD Pipeline
- **Added:** GitHub Actions workflows for tests/lint/type/security, Docker build, migrations, and multi-env deploy skeleton.
- **Learned:** Multi-stage Docker, non-root containers, health checks, and CI quality gates.
- **Challenge:** Tool conflicts, PowerShell vs Bash syntax differences, healthcheck timing.
- **Next:** Configure real deployment targets + secrets, add load testing, blue-green deploy.

---

## Day 13 — CI/CD Fixes
- **Added:** Stable workflows: fixed flake8 duplication, added `__init__.py` for routers, added `alembic` to requirements, made mypy non-blocking.
- **Learned:** Treat workflows as code, test locally first, and fix incrementally.
- **Challenge:** Chasing tool/import errors across CI jobs.
- **Next:** Add conditional jobs, parallel builds, monitoring/alerts, security scans.

---

## Project Status
- **Done:** FastAPI + Postgres (SQLAlchemy/Alembic), JWT auth, task ownership, timers, metrics, Postgres-based tests, CI/CD, priority enum.
- **Now:** Expand test coverage, add pagination (cursor) on `/tasks`, clean repo + move into `app/` package.
- **Next Big Rocks:** Frontend dashboard, production deployment, CI/CD hardening, observability.
