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
