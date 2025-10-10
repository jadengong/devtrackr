"""
Database migration script for Vercel deployment.
Run this once after deployment to set up your database.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to Python path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

# Set Vercel environment
os.environ["VERCEL"] = "1"

import subprocess
from config.config import Config


def run_migrations():
    """Run database migrations"""
    try:
        print("Starting database migrations...")
        print(f"Database URL: {Config.get_database_url()}")
        
        # Run alembic upgrade
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            capture_output=True,
            text=True,
            cwd=parent_dir
        )
        
        if result.returncode == 0:
            print("✅ Database migrations completed successfully!")
            print(result.stdout)
        else:
            print("❌ Migration failed!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error running migrations: {e}")
        return False
    
    return True


if __name__ == "__main__":
    success = run_migrations()
    sys.exit(0 if success else 1)
