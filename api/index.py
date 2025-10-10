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

# Import the FastAPI app from main.py
from main import app

# Export the ASGI application for Vercel
handler = app
