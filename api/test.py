"""
Simple test endpoint for debugging Vercel deployment issues.
"""

from fastapi import FastAPI

app = FastAPI(title="DevTrackr Test API")


@app.get("/")
async def root():
    """Simple test endpoint"""
    return {"message": "DevTrackr Test API is working!", "status": "success"}


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Test API is running"}


@app.get("/debug")
async def debug():
    """Debug endpoint to check environment"""
    import os
    import sys

    return {
        "python_version": sys.version,
        "python_path": sys.path[:5],  # First 5 paths
        "environment_variables": {
            "VERCEL": os.getenv("VERCEL"),
            "PYTHONPATH": os.getenv("PYTHONPATH"),
            "NODE_ENV": os.getenv("NODE_ENV"),
        },
        "working_directory": os.getcwd(),
        "files_in_current_dir": (
            os.listdir(".") if os.path.exists(".") else "Directory not accessible"
        ),
    }


# Export for Vercel
handler = app
