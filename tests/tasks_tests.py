import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

task_example = {
    "title": "Test1",
    "description": "testing",
    "status": "pending",
    "priority": "medium",
    "assigned_to": "omar"
}

def test_create_task():
    response = client.post("/tasks/", json=task_example)
    assert response.status_code == 201
    assert response.json()["title"] == task_example["title"]

def test_get_all_tasks():
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_task_by_id():
    create_response = client.post("/tasks/", json=task_example)
    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id

def test_update_task():
    create_response = client.post("/tasks/", json=task_example)
    task_id = create_response.json()["id"]
    update_data = {"title": "Updated Task"}

    response = client.put(f"/tasks/{task_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Task"

def test_delete_task():
    create_response = client.post("/tasks/", json=task_example)
    task_id = create_response.json()["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "Task deleted"

def test_filter_by_priority():
    response = client.get("/tasks/priority/medium")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
