"""
Vercel-specific configuration for DevTrackr API.
This handles the differences between local development and Vercel deployment.
"""

import os
from config.config import Config


class VercelConfig(Config):
    """Vercel-specific configuration overrides"""
    
    @classmethod
    def get_database_url(cls) -> str:
        """
        Get database URL for Vercel deployment.
        For Vercel, we'll use a serverless database or SQLite.
        """
        # Try to get Vercel-specific database URL
        vercel_db_url = os.getenv("DATABASE_URL")
        
        if vercel_db_url:
            return vercel_db_url
        
        # Fallback to SQLite for serverless (though not ideal for production)
        return "sqlite:///./devtrackr.db"
    
    @classmethod
    def is_vercel(cls) -> bool:
        """Check if running on Vercel"""
        return os.getenv("VERCEL") == "1"
    
    @classmethod
    def get_cors_origins(cls) -> list:
        """Get CORS origins for Vercel deployment"""
        if cls.is_vercel():
            # Allow your Vercel domain and common origins
            vercel_url = os.getenv("VERCEL_URL")
            if vercel_url:
                return [
                    f"https://{vercel_url}",
                    "http://localhost:3000",
                    "http://localhost:8000",
                    "*"
                ]
        
        return super().get_cors_origins()
