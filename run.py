"""
Simple entry point to run the DevTrackr API.

Usage:
    python run.py
    or
    uvicorn run:app --reload
"""

from src.main import app

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)
