#!/usr/bin/env python3
"""
DevTrackr Activity Logging Demo
Demonstrates the activity logging system and audit trail features
"""

from demo_utils import setup_demo_imports

setup_demo_imports()


def demo_activity_logger():
    print("ACTIVITY LOGGING SYSTEM DEMONSTRATION")
    print("=" * 60)

    try:
        from services.activity_logger import ActivityLogger
        from core.models import ActivityType

        print("Successfully imported ActivityLogger and ActivityType")

        print("\nActivity Logger Methods:")
        methods = [
            ("log_task_created", "Log when a new task is created"),
            ("log_task_updated", "Log when a task is modified"),
            ("log_task_deleted", "Log when a task is deleted/archived"),
            ("log_task_archived", "Log when a task is archived"),
            ("log_timer_started", "Log when time tracking starts"),
            ("log_timer_stopped", "Log when time tracking stops"),
        ]

        for method, description in methods:
            print(f"  - {method}: {description}")

    except Exception as e:
        print(f"Error importing activity logger: {e}")


def demo_activity_types():
    print("\nACTIVITY TYPES DEMONSTRATION")
    print("-" * 35)

    try:
        from core.models import ActivityType

        print("Available Activity Types:")
        for activity_type in ActivityType:
            print(f"  - {activity_type.value}")

        print("\nActivity Type Usage Examples:")
        examples = [
            ("task_created", "User creates a new task"),
            ("task_updated", "User modifies task details"),
            ("task_deleted", "User deletes/archives a task"),
            ("task_archived", "User archives a completed task"),
            ("timer_started", "User starts time tracking"),
            ("timer_stopped", "User stops time tracking"),
        ]

        for activity_type, description in examples:
            print(f"  - {activity_type}: {description}")

    except Exception as e:
        print(f"Error with activity types: {e}")


def demo_activity_log_structure():
    print("\nACTIVITY LOG STRUCTURE DEMONSTRATION")
    print("-" * 40)

    print("ActivityLog Database Fields:")
    fields = [
        ("id", "Primary key"),
        ("user_id", "ID of the user performing the action"),
        ("activity_type", "Type of activity (enum)"),
        ("entity_type", "Type of entity affected (e.g., 'task')"),
        ("entity_id", "ID of the affected entity"),
        ("description", "Human-readable description"),
        ("activity_metadata", "Additional data (JSON)"),
        ("created_at", "Timestamp of the activity"),
    ]

    for field, description in fields:
        print(f"  - {field}: {description}")

    print("\nExample Activity Log Entry:")
    example_entry = {
        "id": 789,
        "user_id": 123,
        "activity_type": "task_created",
        "entity_type": "task",
        "entity_id": 456,
        "description": "Created task: Implement user authentication",
        "activity_metadata": {"task_title": "Implement user authentication"},
        "created_at": "2024-01-15T10:30:00Z",
    }

    print("  {")
    for key, value in example_entry.items():
        if key == "activity_metadata":
            print(f'    "{key}": {{')
            for meta_key, meta_value in value.items():
                print(f'      "{meta_key}": "{meta_value}"')
            print("    }")
        else:
            print(f'    "{key}": "{value}"')
    print("  }")


def demo_activity_workflow():
    print("\nACTIVITY LOGGING WORKFLOW DEMONSTRATION")
    print("-" * 45)

    print("Complete User Workflow with Activity Logging:")

    workflow_steps = [
        (
            "1. User creates task",
            "ActivityLogger.log_task_created()",
            "Logs: 'Created task: Fix authentication bug'",
        ),
        (
            "2. User starts timer",
            "ActivityLogger.log_timer_started()",
            "Logs: 'Started timer for: Fix authentication bug'",
        ),
        (
            "3. User works for 2 hours",
            "Time tracked automatically",
            "No activity log (time tracking is separate)",
        ),
        (
            "4. User stops timer",
            "ActivityLogger.log_timer_stopped()",
            "Logs: 'Stopped timer for: Fix authentication bug (120 minutes)'",
        ),
        (
            "5. User updates task",
            "ActivityLogger.log_task_updated()",
            "Logs: 'Updated task: Fix authentication bug' with changes metadata",
        ),
        (
            "6. User completes task",
            "ActivityLogger.log_task_updated()",
            "Logs: 'Updated task: Fix authentication bug' with status change",
        ),
        (
            "7. User archives task",
            "ActivityLogger.log_task_archived()",
            "Logs: 'Archived task: Fix authentication bug'",
        ),
    ]

    for step, method, log_description in workflow_steps:
        print(f"\n  {step}")
        print(f"    Method: {method}")
        print(f"    Logs: {log_description}")


if __name__ == "__main__":
    demo_activity_logger()
    demo_activity_types()
    demo_activity_log_structure()
    demo_activity_workflow()

    print("\n" + "=" * 60)
    print("ACTIVITY LOGGING SUMMARY:")
    print("- Automatic logging of all user actions")
    print("- Rich metadata for detailed tracking")
    print("- Complete audit trail for compliance")
    print("- Support for task lifecycle tracking")
    print("- Time tracking integration")
    print("- JSON metadata for flexible data storage")
    print("=" * 60)
