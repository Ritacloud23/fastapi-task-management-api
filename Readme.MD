# FastAPI Task Management API

A RESTful Task Management API built with **FastAPI**, **SQLModel**, and **SQLite**. The project demonstrates backend API development, database persistence, authentication, validation, pagination, and background task processing.

## Features

- User creation and retrieval
- Task creation, retrieval, update, and deletion
- SQLite database persistence
- SQLModel ORM
- API key authentication
- Request validation with Pydantic/SQLModel
- Pagination with offset and limit
- HTTP status code handling
- 404 error handling
- Background task processing
- Interactive Swagger API documentation
- Automated API testing with Pytest

## Tech Stack

- Python
- FastAPI
- SQLModel
- SQLite
- Uvicorn
- Pytest
- HTTPX

## Project Structure

```text

Task_Management_API/
│
├── main.py
├── models.py
├── database.py
├── dependencies.py
├── requirements.txt
├── pyproject.toml
├── README.md
├── .gitignore
│
├── tests/
│   ├── __init__.py
│   └── test_main.py
│
└── task_management.db
```

## API Endpoints

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /users | Create a new user |
| GET | /users | Get all users |
| GET | /users/{user_id} | Get a user by ID |

### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|

| POST | /tasks | Create a task |
| GET | /tasks | Get all tasks |
| GET | /tasks/{task_id} | Get a task by ID |
| PUT | /tasks/{task_id} | Update a task |
| DELETE | /tasks/{task_id} | Delete a task |

## Authentication

Protected endpoints require an API key in the request header.

```
X-API-Key: my-secret-key
```

Example:

```bash
curl -X POST "http://127.0.0.1:8000/tasks" \
  -H "X-API-Key: my-secret-key" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete FastAPI project",
    "description": "Finish and test the Task Management API",
    "status": "pending",
    "user_id": 1
  }'
```

## Pagination

The task and user listing endpoints support pagination.


Example:

```
GET /tasks?offset=0&limit=10
```

- `offset` determines where results start.
- `limit` determines the maximum number of results returned.
- `limit` is restricted to a maximum of 100.

## Background Tasks

When a task is updated to:

```json
{
  "status": "completed"
}
```

FastAPI schedules a background task that generates a completion report.

## Running the Project

### 1. Clone the repository

```bash
git clone <repository-url>
cd Task_Management_API
```

### 2. Install dependencies


Using Poetry:

```bash
poetry install
```

Or using requirements.txt:

```bash
pip install -r requirements.txt
```

### 3. Start the API

```bash
uvicorn main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

## API Documentation

FastAPI automatically provides interactive API documentation.

Swagger UI:

```

http://127.0.0.1:8000/docs
```

ReDoc:

```
http://127.0.0.1:8000/redoc
```

## Running Tests

Run the complete test suite with:

```bash
poetry run pytest
```

The project includes tests covering:

- Root endpoint
- User creation
- Task creation
- API key authentication
- Task retrieval
- Task updates
- Task deletion
- 404 error handling

## Example Response

### Create Task


```json
{
  "id": 1,
  "title": "Complete FastAPI project",
  "description": "Finish and test the Task Management API",
  "status": "pending",
  "user_id": 1
}
```

## What I Practiced

This project strengthened my understanding of:

- Building REST APIs with FastAPI
- Dependency injection
- Annotated dependencies
- API key authentication
- Database sessions
- SQLModel models
- CRUD operations
- Request and response validation
- Pagination
- HTTP status codes
- Background tasks
- Automated API testing

## Author

**Rita Nnenna**

**Cloud & DevOps Engineer | Full-Stack Engineer**