from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Task Management API is running"
    }


def test_create_user():
    response = client.post(
        "/users",
        headers={
            "X-API-Key": "my-secret-key"
        },
        json={
            "name": "Test User",
            "email": "testuser@example.com"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Test User"
    assert data["email"] == "testuser@example.com"
    assert "id" in data


def test_create_task():
    response = client.post(
        "/tasks",
        headers={
            "X-API-Key": "my-secret-key"
        },
        json={
            "title": "Test Task",
            "description": "Testing task creation",
            "status": "pending",
            "user_id": 1
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Test Task"
    assert data["description"] == "Testing task creation"
    assert data["status"] == "pending"
    assert data["user_id"] == 1
    assert "id" in data


def test_create_task_with_invalid_api_key():
    response = client.post(
        "/tasks",
        headers={
            "X-API-Key": "wrong-key"
        },
        json={
            "title": "Unauthorized Task",
            "description": "This should not be created",
            "status": "pending",
            "user_id": 1
        },
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Invalid or missing API key"
    }


def test_get_tasks():
    response = client.get(
        "/tasks",
        params={
            "offset": 0,
            "limit": 10
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_get_task():
    create_response = client.post(
        "/tasks",
        headers={
            "X-API-Key": "my-secret-key"
        },
        json={
            "title": "Task for Get Test",
            "description": "Testing get task",
            "status": "pending",
            "user_id": 1
        },
    )

    assert create_response.status_code == 200

    task_id = create_response.json()["id"]

    response = client.get(
        f"/tasks/{task_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task_id
    assert data["title"] == "Task for Get Test"
    assert data["status"] == "pending"


def test_update_task():
    create_response = client.post(
        "/tasks",
        headers={
            "X-API-Key": "my-secret-key"
        },
        json={
            "title": "Task for Update Test",
            "description": "Testing task update",
            "status": "pending",
            "user_id": 1
        },
    )

    assert create_response.status_code == 200

    task_id = create_response.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        headers={
            "X-API-Key": "my-secret-key"
        },
        json={
            "status": "completed"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task_id
    assert data["status"] == "completed"


def test_delete_task():
    create_response = client.post(
        "/tasks",
        headers={
            "X-API-Key": "my-secret-key"
        },
        json={
            "title": "Task for Delete Test",
            "description": "Testing task deletion",
            "status": "pending",
            "user_id": 1
        },
    )

    assert create_response.status_code == 200

    task_id = create_response.json()["id"]

    response = client.delete(
        f"/tasks/{task_id}",
        headers={
            "X-API-Key": "my-secret-key"
        },
    )

    assert response.status_code == 200

    assert response.json() == {
        "message": "Task deleted successfully"
    }


def test_get_nonexistent_task():
    response = client.get("/tasks/99999")

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Task not found"
    }