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
  - Didn’t understand why `utcnow()` was flagged → learned to use `datetime.now(timezone.utc)`
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
  - Difference between “unset” vs “None” in PATCH requests
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
  - Needed to understand the difference between “optional param not provided” vs. “param provided with bad value”
- Next:
  - Add basic tests with pytest to check `/time` and full task lifecycle

## Day 5 — Testing
- Added:
  - Basic pytest setup with `TestClient`
  - Tests for `/time` endpoint
  - Tests for tasks lifecycle (`POST`, `GET`, `GET by id`)
- Learned:
  - How to structure tests in a separate `tests/` folder
  - Why a reset helper is needed so tests don’t interfere with each other
  - How `pytest` automatically discovers and runs test files
- Challenge:
  - Initially ran into import errors (`ModuleNotFoundError`) and a SyntaxError from `_reset_state_for_test`
  - Fixed by cleaning up `main.py` and keeping test code in its own files
- Next:
  - Consider adding pagination (`limit`, `offset`) to `GET /tasks`
  - Or move on to database integration with PostgreSQL and SQLAlchemy
  - Think that database integration is best for now to move on from the in-memory

## Day 6 — DB Integration Progress

- Set up `.env` with `DATABASE_URL` and configured `db.py` (SQLAlchemy engine, SessionLocal, Base).
- Defined `Task` ORM model in `models.py` with enum `TaskStatus`, timestamps, defaults, and indexes.
- Installed & configured Alembic:
  - Fixed `alembic/env.py` to load `.env`, import `Base`, and include models.
  - First autogenerate didn’t pick up `Task` → fixed imports and re-ran.
  - Successfully generated migration with `tasks` table + enum type.
  - Verified in Postgres (`\dt`, `\d tasks`) that schema is correct.
- Updated `main.py`, `routers/tasks.py`, `schemas.py`, and `deps.py` for DB-backed CRUD.
- Swagger UI at `/docs` shows full CRUD API, tested endpoints manually.
- Next steps (tomorrow): add pytest suite with a clean test DB to automate CRUD checks.

**Challenges solved:**
- Relative imports vs absolute (`from db import Base` instead of `from .db import Base`).
- Alembic not detecting models until we explicitly `import models` in `env.py`.
- Conflicts between old in-memory code and new DB-backed router.

**Takeaway:** Got full end-to-end DB integration working — FastAPI ↔ SQLAlchemy ↔ Alembic ↔ Postgres 🚀
