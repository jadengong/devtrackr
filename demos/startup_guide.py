#!/usr/bin/env python3
"""
DevTrackr Startup Guide Demo
Shows how to set up and run the DevTrackr application
"""


def demo_startup_process():
    print("DEVTRACKR APPLICATION STARTUP DEMONSTRATION")
    print("=" * 60)

    print("\n1. PREREQUISITES CHECK")
    print("-" * 30)
    print("- Python 3.11+ installed")
    print("- Dependencies installed (pip install -r requirements.txt)")
    print("- PostgreSQL database available")
    print("- Docker (optional, for database)")

    print("\n2. DATABASE SETUP")
    print("-" * 20)
    print("Option A - Docker (Recommended):")
    print("  docker-compose up -d db")
    print("  # Starts PostgreSQL on localhost:5432")

    print("\nOption B - Local PostgreSQL:")
    print("  # Install PostgreSQL locally")
    print("  # Create database: devtrackr")
    print("  # Set environment variables")

    print("\n3. ENVIRONMENT CONFIGURATION")
    print("-" * 35)
    print("Set these environment variables:")
    print("  DATABASE_URL=postgresql+psycopg2://dev:dev@localhost:5432/devtrackr")
    print("  SECRET_KEY=your-secret-key-here")
    print("  LOG_LEVEL=INFO")

    print("\n4. DATABASE MIGRATIONS")
    print("-" * 30)
    print("Run database migrations:")
    print("  python -m alembic upgrade head")
    print("  # Creates all tables and indexes")

    print("\n5. START THE APPLICATION")
    print("-" * 30)
    print("Development mode:")
    print("  uvicorn main:app --host 0.0.0.0 --port 8000 --reload")

    print("\nProduction mode:")
    print("  uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4")

    print("\n6. ACCESS THE API")
    print("-" * 20)
    print("API Documentation (Swagger UI):")
    print("  http://localhost:8000/docs")

    print("\nAlternative API Docs (ReDoc):")
    print("  http://localhost:8000/redoc")

    print("\nHealth Check:")
    print("  http://localhost:8000/health")

    print("\n7. TESTING")
    print("-" * 15)
    print("Run the test suite:")
    print("  python run_tests.py")

    print("\nRun specific tests:")
    print("  python -m pytest tests/test_tasks_api.py -v")


def demo_docker_setup():
    print("\n8. DOCKER SETUP (ALTERNATIVE)")
    print("-" * 35)

    print("Full stack with Docker Compose:")
    print("  docker-compose up")
    print("  # Starts both database and application")

    print("\nBuild and run application container:")
    print("  docker build -t devtrackr .")
    print("  docker run -d -p 8000:8000 --name devtrackr-api devtrackr")

    print("\nCheck container health:")
    print("  docker ps")
    print("  curl http://localhost:8000/health")


def demo_quick_start():
    print("\n9. QUICK START COMMANDS")
    print("-" * 30)

    commands = [
        "# Clone and setup",
        "git clone <repository-url>",
        "cd devtrackr-repo",
        "",
        "# Start database",
        "docker-compose up -d db",
        "",
        "# Install dependencies",
        "pip install -r requirements.txt",
        "",
        "# Run migrations",
        "python -m alembic upgrade head",
        "",
        "# Start application",
        "uvicorn main:app --reload",
        "",
        "# Access API docs",
        "# Open http://localhost:8000/docs",
    ]

    for cmd in commands:
        print(f"  {cmd}")


def demo_troubleshooting():
    print("\n10. TROUBLESHOOTING")
    print("-" * 25)

    print("Common Issues and Solutions:")

    issues = [
        ("Database connection error", "Check if PostgreSQL is running and accessible"),
        ("Import errors", "Run: pip install -r requirements.txt"),
        ("Port already in use", "Change port: uvicorn main:app --port 8001"),
        (
            "Migration errors",
            "Check database connection and run: python -m alembic upgrade head",
        ),
        ("Authentication errors", "Check SECRET_KEY environment variable"),
        ("Docker issues", "Ensure Docker is running and containers are healthy"),
    ]

    for issue, solution in issues:
        print(f"\n  Problem: {issue}")
        print(f"  Solution: {solution}")


def demo_health_checks():
    print("\n11. HEALTH CHECKS")
    print("-" * 20)

    print("Health Check Endpoints:")

    health_endpoints = [
        ("/health", "Basic health status"),
        ("/live", "Liveness probe (lightweight)"),
        ("/ready", "Readiness probe with uptime"),
        ("/info", "Runtime and configuration info"),
    ]

    for endpoint, description in health_endpoints:
        print(f"  GET {endpoint}: {description}")

    print("\nExample Health Check Response:")
    print("  {")
    print('    "status": "healthy",')
    print('    "service": "DevTrackr API",')
    print('    "version": "1.0.2",')
    print('    "timestamp": "2024-01-15T10:30:00Z"')
    print("  }")


if __name__ == "__main__":
    demo_startup_process()
    demo_docker_setup()
    demo_quick_start()
    demo_troubleshooting()
    demo_health_checks()

    print("\n" + "=" * 60)
    print("READY TO USE DEVTRACKR!")
    print("The API will be available at http://localhost:8000")
    print("Interactive documentation at http://localhost:8000/docs")
    print("=" * 60)
