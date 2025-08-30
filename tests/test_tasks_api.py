import pytest
from fastapi import status
from models import TaskStatus


class TestTasksAPI:
    """End-to-end tests for the /tasks API endpoints."""

    def test_create_and_get_task(self, client, db_session):
        """Test POST /tasks with {title, description, priority}, then GET /tasks/{id}."""

        # Create task data
        task_data = {
            "title": "Test Task Title",
            "description": "This is a test task description",
            "priority": 2,
        }

        # POST /tasks - Create the task
        response = client.post("/tasks", json=task_data)

        # Assert response status and structure
        assert response.status_code == status.HTTP_201_CREATED
        created_task = response.json()

        # Assert key fields in created task
        assert "id" in created_task
        assert created_task["title"] == task_data["title"]
        assert created_task["description"] == task_data["description"]
        assert created_task["priority"] == task_data["priority"]
        assert created_task["status"] == "todo"  # Default status
        assert created_task["is_archived"] is False
        assert "created_at" in created_task
        assert "updated_at" in created_task

        # Store the task ID for GET request
        task_id = created_task["id"]

        # GET /tasks/{id} - Retrieve the created task
        response = client.get(f"/tasks/{task_id}")

        # Assert response status and structure
        assert response.status_code == status.HTTP_200_OK
        retrieved_task = response.json()

        # Assert the retrieved task matches the created task
        assert retrieved_task["id"] == task_id
        assert retrieved_task["title"] == task_data["title"]
        assert retrieved_task["description"] == task_data["description"]
        assert retrieved_task["priority"] == task_data["priority"]
        assert retrieved_task["status"] == "todo"
        assert retrieved_task["is_archived"] is False

    def test_list_filter_patch_delete(self, client, db_session):
        """Test creating 3 tasks, listing, patching, soft deleting, and confirming archived state."""

        # Create 3 tasks with different statuses
        tasks_data = [
            {
                "title": "Todo Task",
                "description": "Task in todo status",
                "status": "todo",
                "priority": 3,
            },
            {
                "title": "In Progress Task",
                "description": "Task in progress",
                "status": "in_progress",
                "priority": 2,
            },
            {
                "title": "Done Task",
                "description": "Completed task",
                "status": "done",
                "priority": 1,
            },
        ]

        created_tasks = []

        # Create all 3 tasks
        for task_data in tasks_data:
            response = client.post("/tasks", json=task_data)
            assert response.status_code == status.HTTP_201_CREATED
            created_tasks.append(response.json())

        # GET /tasks - List all tasks
        response = client.get("/tasks")
        assert response.status_code == status.HTTP_200_OK
        all_tasks = response.json()

        # Assert we have 3 tasks
        assert len(all_tasks) == 3

        # Verify all created tasks are in the list
        created_ids = {task["id"] for task in created_tasks}
        listed_ids = {task["id"] for task in all_tasks}
        assert created_ids == listed_ids

        # PATCH one task to update status and priority
        task_to_update = created_tasks[0]  # First task
        update_data = {"status": "in_progress", "priority": 1}

        response = client.patch(f"/tasks/{task_to_update['id']}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        updated_task = response.json()

        # Assert the task was updated correctly
        assert updated_task["id"] == task_to_update["id"]
        assert updated_task["title"] == task_to_update["title"]  # Unchanged
        assert updated_task["status"] == "in_progress"  # Updated
        assert updated_task["priority"] == 1  # Updated
        assert updated_task["is_archived"] is False

        # DELETE one task (soft delete)
        task_to_delete = created_tasks[1]  # Second task
        response = client.delete(f"/tasks/{task_to_delete['id']}")
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # GET the deleted task to confirm it's still retrievable but archived
        response = client.get(f"/tasks/{task_to_delete['id']}")
        assert response.status_code == status.HTTP_200_OK
        deleted_task = response.json()

        # Assert the task is marked as archived
        assert deleted_task["id"] == task_to_delete["id"]
        assert deleted_task["title"] == task_to_delete["title"]
        assert deleted_task["is_archived"] is True

        # Verify the task still exists in the database but is archived
        assert deleted_task["status"] == task_to_delete["status"]
        assert deleted_task["priority"] == task_to_delete["priority"]

    def test_get_nonexistent_task(self, client):
        """Test GET /tasks/{id} with non-existent task ID."""
        response = client.get("/tasks/99999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Task not found"

    def test_update_nonexistent_task(self, client):
        """Test PATCH /tasks/{id} with non-existent task ID."""
        update_data = {"title": "Updated Title"}
        response = client.patch("/tasks/99999", json=update_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Task not found"

    def test_delete_nonexistent_task(self, client):
        """Test DELETE /tasks/{id} with non-existent task ID."""
        response = client.delete("/tasks/99999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Task not found"

    def test_create_task_with_minimal_data(self, client, db_session):
        """Test POST /tasks with only required fields."""
        task_data = {"title": "Minimal Task"}

        response = client.post("/tasks", json=task_data)
        assert response.status_code == status.HTTP_201_CREATED

        created_task = response.json()
        assert created_task["title"] == "Minimal Task"
        assert created_task["description"] is None
        assert created_task["priority"] == 3  # Default priority
        assert created_task["status"] == "todo"  # Default status
        assert created_task["is_archived"] is False

    def test_list_tasks_with_status_filter(self, client, db_session):
        """Test GET /tasks with status filter."""
        # Create tasks with different statuses
        tasks_data = [
            {"title": "Task 1", "status": "todo"},
            {"title": "Task 2", "status": "in_progress"},
            {"title": "Task 3", "status": "done"},
        ]

        for task_data in tasks_data:
            response = client.post("/tasks", json=task_data)
            assert response.status_code == status.HTTP_201_CREATED

        # Filter by todo status
        response = client.get("/tasks?status=todo")
        assert response.status_code == status.HTTP_200_OK
        todo_tasks = response.json()
        assert len(todo_tasks) == 1
        assert all(task["status"] == "todo" for task in todo_tasks)

        # Filter by in_progress status
        response = client.get("/tasks?status=in_progress")
        assert response.status_code == status.HTTP_200_OK
        in_progress_tasks = response.json()
        assert len(in_progress_tasks) == 1
        assert all(task["status"] == "in_progress" for task in in_progress_tasks)
