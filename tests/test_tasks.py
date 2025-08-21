from fastapi.testclient import TestClient
import main

client = TestClient(main.app)

def setup_function():
    main._reset_state_for_test()

def test_create_and_list_tasks():
    # create
    resp = client.post("/tasks", json={"title": "First", "category": "study"})
    assert resp.status_code == 201
    created = resp.json()
    assert "id" in created and created["status"] == "todo"

    # list
    resp = client.get("/tasks")
    assert resp.status_code == 200
    items = resp.json()
    assert any(t["id"] == created["id"] for t in items)

def test_get_nonexistent_task_returns_404():
    resp = client.get("/tasks/9999")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Task not found"

def test_patch_status_validation_and_delete():
    # create
    c = client.post("/tasks", json={"title": "Change me"}).json()
    tid = c["id"]

    # invalid status -> 422
    resp = client.patch(f"/tasks/{tid}", json={"status": "fake"})
    assert resp.status_code == 422

    # valid status -> 200
    resp = client.patch(f"/tasks/{tid}", json={"status": "doing"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "doing"

    # delete -> 204
    resp = client.delete(f"/tasks/{tid}")
    assert resp.status_code == 204

    # get after delete -> 404
    resp = client.get(f"/tasks/{tid}")
    assert resp.status_code == 404