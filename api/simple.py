"""
Ultra-simple FastAPI app for testing Vercel deployment without any dependencies.
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Create a minimal FastAPI app
app = FastAPI(
    title="DevTrackr Simple API",
    description="Minimal test API for Vercel deployment",
    version="1.0.0",
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "DevTrackr Simple API is working!", "status": "success"}


@app.get("/health")
async def health():
    """Health check"""
    return {"status": "healthy", "message": "Simple API is running"}


@app.get("/info")
async def info():
    """Basic info endpoint"""
    return {
        "app": "DevTrackr Simple API",
        "version": "1.0.0",
        "status": "running",
        "message": "This is a minimal FastAPI app for testing Vercel deployment",
    }


# Export for Vercel
handler = app
