#!/usr/bin/env python3
"""
DevTrackr API Examples Demo
Shows detailed API endpoint examples with request/response formats
"""

def demo_api_examples():
    print("API ENDPOINTS DEMONSTRATION WITH EXAMPLES")
    print("=" * 60)
    
    # Authentication Examples
    print("\n1. AUTHENTICATION ENDPOINTS")
    print("-" * 30)
    
    print("User Registration:")
    print("POST /auth/register")
    print("Body: {")
    print('  "email": "developer@example.com",')
    print('  "username": "johndoe",')
    print('  "password": "securepassword123"')
    print("}")
    
    print("\nUser Login:")
    print("POST /auth/login")
    print("Body: {")
    print('  "email": "developer@example.com",')
    print('  "password": "securepassword123"')
    print("}")
    print("Response: {")
    print('  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",')
    print('  "token_type": "bearer"')
    print("}")
    
    # Task Management Examples
    print("\n2. TASK MANAGEMENT ENDPOINTS")
    print("-" * 35)
    
    print("Create Task:")
    print("POST /tasks")
    print("Headers: Authorization: Bearer <token>")
    print("Body: {")
    print('  "title": "Implement user authentication",')
    print('  "description": "Add JWT-based authentication to the API",')
    print('  "category": "backend",')
    print('  "priority": "high",')
    print('  "estimated_minutes": 240,')
    print('  "due_date": "2024-01-20T17:00:00Z"')
    print("}")
    
    print("\nGet Tasks with Filtering:")
    print("GET /tasks?status=todo&priority=high&category=backend&limit=10")
    print("Headers: Authorization: Bearer <token>")
    
    print("\nUpdate Task:")
    print("PATCH /tasks/123")
    print("Headers: Authorization: Bearer <token>")
    print("Body: {")
    print('  "status": "in_progress",')
    print('  "actual_minutes": 120')
    print("}")
    
    # Search Examples
    print("\n3. SEARCH FUNCTIONALITY")
    print("-" * 25)
    
    print("Full-text Search:")
    print("GET /tasks/search?q=authentication")
    print("Headers: Authorization: Bearer <token>")
    
    print("\nSearch with Filters:")
    print("GET /tasks/search?q=bug&status=todo&priority=urgent")
    
    print("\nSearch with Date Range:")
    print("GET /tasks/search?q=deadline&due_after=2024-01-01&due_before=2024-12-31")
    
    # Time Tracking Examples
    print("\n4. TIME TRACKING ENDPOINTS")
    print("-" * 30)
    
    print("Start Timer:")
    print("POST /time-tracking/start")
    print("Headers: Authorization: Bearer <token>")
    print("Body: {")
    print('  "task_id": 123,')
    print('  "description": "Working on authentication implementation"')
    print("}")
    
    print("\nStop Timer:")
    print("POST /time-tracking/stop")
    print("Headers: Authorization: Bearer <token>")
    print("Body: {")
    print('  "task_id": 123')
    print("}")
    
    # Analytics Examples
    print("\n5. ANALYTICS ENDPOINTS")
    print("-" * 25)
    
    print("Task Summary:")
    print("GET /metrics/summary")
    print("Headers: Authorization: Bearer <token>")
    print("Response: {")
    print('  "total_tasks": 45,')
    print('  "completed_tasks": 12,')
    print('  "in_progress_tasks": 8,')
    print('  "todo_tasks": 25,')
    print('  "completion_rate": 0.27')
    print("}")
    
    print("\nCategory Breakdown:")
    print("GET /metrics/categories")
    print("Response: {")
    print('  "categories": [')
    print('    {"name": "backend", "count": 15, "completed": 5},')
    print('    {"name": "frontend", "count": 12, "completed": 4},')
    print('    {"name": "testing", "count": 8, "completed": 3}')
    print('  ]')
    print("}")

def demo_workflow():
    print("\n6. COMPLETE USER WORKFLOW")
    print("-" * 30)
    
    steps = [
        "1. Register: POST /auth/register",
        "2. Login: POST /auth/login -> Get JWT token",
        "3. Create task: POST /tasks -> Activity logged",
        "4. Start timer: POST /time-tracking/start -> Activity logged",
        "5. Work for 2 hours...",
        "6. Stop timer: POST /time-tracking/stop -> Activity logged",
        "7. Update task: PATCH /tasks/{id} -> Activity logged",
        "8. Complete task: PATCH /tasks/{id} (status: done)",
        "9. View analytics: GET /metrics/summary",
        "10. Search tasks: GET /tasks/search?q=authentication"
    ]
    
    for step in steps:
        print(f"   {step}")

if __name__ == "__main__":
    demo_api_examples()
    demo_workflow()
    
    print("\n" + "=" * 60)
    print("KEY FEATURES DEMONSTRATED:")
    print("- JWT Authentication with secure token handling")
    print("- Full CRUD operations for task management")
    print("- Advanced search with PostgreSQL full-text search")
    print("- Time tracking with start/stop functionality")
    print("- Comprehensive activity logging for audit trails")
    print("- Analytics and metrics for productivity insights")
    print("- Production-ready features (health checks, error handling)")
    print("=" * 60)
