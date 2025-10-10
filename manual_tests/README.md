# Manual Integration Tests

This directory contains manual integration test scripts that require a running DevTrackr server.

## Requirements

These tests require:
- DevTrackr server running on `http://localhost:8000`
- `requests` library installed
- Valid authentication (you may need to adjust auth tokens in the scripts)

## Running Manual Tests

1. **Start the DevTrackr server:**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Install requests (if not already installed):**
   ```bash
   pip install requests
   ```

3. **Run individual test scripts:**
   ```bash
   # Test pagination functionality
   python manual_tests/pagination_integration_test.py
   
   # Test search functionality  
   python manual_tests/search_integration_test.py
   ```

## Note

These are **integration tests**, not unit tests. They:
- Require a running server
- Make HTTP requests to test API endpoints
- Are excluded from the pytest test suite
- Should be run manually when testing integration scenarios

For automated unit tests, see the `tests/` directory.
