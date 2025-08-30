# DevTrackr

A FastAPI-based task tracking API (Python).

- ✅ CRUD for tasks with validation and clean error handling
- ✅ Automated tests with pytest + TestClient + coverage reporting
- 📓 Progress log: see [LEARNING.md](./LEARNING.md)

## Quick start
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1    # Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

## Testing

The project includes comprehensive testing with pytest and coverage reporting:

### Quick Test Commands
```bash
# Run tests with coverage (default)
python -m pytest

# Run tests with coverage reporting
python -m pytest --cov=. --cov-report=term-missing

# Generate HTML coverage report
python -m pytest --cov-report=html

# Use the test runner script
python run_tests.py --coverage html
python run_tests.py --fast  # No coverage, fast execution
```

### Coverage Reports
- **Terminal**: Shows missing lines and coverage percentage
- **HTML**: Interactive report in `htmlcov/index.html`
- **XML**: For CI/CD integration
- **Target**: 80% minimum coverage (configured in pytest.ini)
