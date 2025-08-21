# DevTrackr

A FastAPI-based task tracking API (Python).

- ✅ CRUD for tasks with validation and clean error handling
- ✅ Automated tests with pytest + TestClient
- 📓 Progress log: see [LEARNING.md](./LEARNING.md)

## Quick start
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1    # Windows
pip install -r requirements.txt
uvicorn main:app --reload
