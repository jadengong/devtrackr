#!/usr/bin/env python3
"""
DevTrackr Basic Demo
Demonstrates the core database models and basic functionality
"""

from demo_utils import setup_demo_imports

setup_demo_imports()


def demo_models():
    """Demonstrate the database models and relationships"""
    print("DATABASE MODELS DEMONSTRATION")
    print("=" * 50)

    try:
        from models import (
            Task,
            User,
            TimeEntry,
            ActivityLog,
            TaskStatus,
            TaskPriority,
            ActivityType,
        )

        print("Successfully imported all models")

        print("\nCore Models:")
        print(f"  - User: {User.__tablename__}")
        print(f"  - Task: {Task.__tablename__}")
        print(f"  - TimeEntry: {TimeEntry.__tablename__}")
        print(f"  - ActivityLog: {ActivityLog.__tablename__}")

        print("\nTask Status Options:")
        for status in TaskStatus:
            print(f"  - {status.value}")

        print("\nTask Priority Levels:")
        for priority in TaskPriority:
            print(f"  - {priority.value}")

        print("\nActivity Types:")
        for activity_type in ActivityType:
            print(f"  - {activity_type.value}")

    except Exception as e:
        print(f"Error importing models: {e}")


def demo_schemas():
    """Demonstrate the Pydantic schemas"""
    print("\nPYDANTIC SCHEMAS DEMONSTRATION")
    print("=" * 50)

    try:
        from schemas import TaskCreate, TaskUpdate, UserCreate, TaskOut

        print("Successfully imported schemas")

        # Example task creation
        task_data = {
            "title": "Implement user authentication",
            "description": "Add JWT-based authentication to the API",
            "category": "backend",
            "priority": "high",
            "estimated_minutes": 240,
        }

        print("\nExample Task Creation Schema:")
        print(f"  Title: {task_data['title']}")
        print(f"  Category: {task_data['category']}")
        print(f"  Priority: {task_data['priority']}")
        print(f"  Estimated Time: {task_data['estimated_minutes']} minutes")

    except Exception as e:
        print(f"Error with schemas: {e}")


def demo_activity_logger():
    """Demonstrate the activity logger service"""
    print("\nACTIVITY LOGGER DEMONSTRATION")
    print("=" * 50)

    try:
        from services.activity_logger import ActivityLogger

        print("Successfully imported ActivityLogger")

        print("\nActivity Logger Methods:")
        methods = [
            "log_task_created",
            "log_task_updated",
            "log_task_deleted",
            "log_task_archived",
            "log_timer_started",
            "log_timer_stopped",
        ]

        for method in methods:
            print(f"  - {method}")

    except Exception as e:
        print(f"Error with activity logger: {e}")


def demo_api_structure():
    """Demonstrate the API endpoints structure"""
    print("\nAPI ENDPOINTS STRUCTURE")
    print("=" * 50)

    endpoints = {
        "Authentication": ["POST /auth/register", "POST /auth/login", "GET /auth/me"],
        "Task Management": [
            "GET /tasks",
            "POST /tasks",
            "PATCH /tasks/{id}",
            "DELETE /tasks/{id}",
        ],
        "Time Tracking": ["POST /time-tracking/start", "POST /time-tracking/stop"],
        "Analytics": ["GET /metrics/summary", "GET /metrics/categories"],
    }

    for category, routes in endpoints.items():
        print(f"\n{category}:")
        for route in routes:
            print(f"  - {route}")


if __name__ == "__main__":
    print("DEVTRACKR BASIC DEMONSTRATION")
    print("=" * 60)

    demo_models()
    demo_schemas()
    demo_activity_logger()
    demo_api_structure()

    print("\nDEMONSTRATION COMPLETE!")
    print("DevTrackr provides:")
    print("- JWT-based authentication")
    print("- Task management with priorities")
    print("- Time tracking capabilities")
    print("- Activity logging for audit trails")
    print("- Analytics and metrics")
