# fastapi-business-crud

Minimal business-style CRUD API built with FastAPI.

This repository provides a simple backend structure with JWT authentication,
database integration, task management endpoints, and CSV import support.

It is designed as a practical backend template for small business systems,
internal tools, and API-based services.

---

## Stack

- FastAPI
- SQLAlchemy
- SQLite
- JWT Authentication
- Docker

---

## Features

- JWT-based authentication
- Task CRUD API
- CSV import endpoint for bulk task creation
- Validation with row-level error reporting
- 404 handling for missing task IDs
- Simple local and Docker execution

---

## Run (Local)

    uvicorn main:app --reload

Swagger UI

    http://localhost:8000/docs

---

## Run with Docker

Build image

    docker build -t fastapi-business-crud .

Run container

    docker run -p 8000:8000 -e SECRET_KEY=your-secret-key -e ALGORITHM=HS256 fastapi-business-crud

Swagger UI

    http://localhost:8000/docs

---

## Authentication

Login endpoint

    POST /token

Demo credentials

    username: demo
    password: demo123

Use the returned token in Swagger **Authorize**

    Bearer <access_token>

---

## Endpoints

### Tasks API

    GET     /tasks
    POST    /tasks
    GET     /tasks/{task_id}
    PATCH   /tasks/{task_id}
    DELETE  /tasks/{task_id}
    POST    /tasks/import

---

## CSV Import

The API supports bulk task creation via CSV upload.

Endpoint

    POST /tasks/import

Upload format

- `multipart/form-data`
- file field: `file`

Supported columns

    title,description,status

Example CSV

    title,description,status
    Task A,first task,todo
    Task B,second task,doing
    Task C,third task,done
    Task A,duplicate task,todo
    ,missing title,todo
    Task D,bad status,waiting

Validation rules

- `title` is required
- `description` is optional
- `status` must be one of:
  - `todo`
  - `doing`
  - `done`
- duplicate titles in the same import are skipped

Example response

    {
      "total_rows": 6,
      "created_count": 3,
      "skipped_count": 1,
      "error_count": 2,
      "errors": [
        {
          "row": 6,
          "reason": "title is required"
        },
        {
          "row": 7,
          "reason": "status must be one of: todo, doing, done"
        }
      ]
    }

This makes the import flow easier to debug because invalid rows are returned
with their CSV row numbers.

---

## Error Handling

When a task does not exist, the API returns a proper `404 Not Found`
response instead of failing internally.

Example

    {
      "detail": "Task not found"
    }

This behavior is applied to:

- `GET /tasks/{task_id}`
- `PATCH /tasks/{task_id}`
- `DELETE /tasks/{task_id}`

---

## Purpose

This project is a minimal but practical example of a business-style CRUD API.

Instead of only showing basic create/read/update/delete operations, it also
demonstrates common backend concerns such as authentication, bulk data import,
input validation, and proper error handling.