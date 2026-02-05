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
    import os

    host = os.getenv("DEVTRACKR_HOST", "127.0.0.1")
    port = int(os.getenv("DEVTRACKR_PORT", "8000"))

    uvicorn.run("src.main:app", host=host, port=port, reload=True)
