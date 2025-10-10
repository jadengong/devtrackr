"""
Vercel serverless function entry point for DevTrackr API.
This file adapts the FastAPI application for Vercel's serverless environment.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to Python path so we can import our modules
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

# Set Vercel environment flag
os.environ["VERCEL"] = "1"

try:
    # Import the FastAPI app from main.py
    from main import app

    # Export the ASGI application for Vercel
    handler = app

except ImportError as e:
    # If import fails, create a simple error handler
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse

    error_app = FastAPI()

    @error_app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        return JSONResponse(
            status_code=500,
            content={
                "error": "Import Error",
                "message": f"Failed to import main application: {str(e)}",
                "path": str(parent_dir),
                "python_path": sys.path[:3],  # Show first 3 paths for debugging
            },
        )

    handler = error_app
