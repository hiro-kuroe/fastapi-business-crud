# FastAPI-business-crud

Minimal business CRUD API built with FastAPI.

This repository provides a simple backend structure with authentication,
database integration, and task management endpoints.

---

## Stack

- FastAPI
- SQLAlchemy
- SQLite
- JWT Authentication
- Docker

---

## Run (Local)

```bash
uvicorn main:app --reload
```

Swagger UI

```
http://localhost:8000/docs
```

---

## Run with Docker

Build image

```bash
docker build -t fastapi-business-crud .
```

Run container

```bash
docker run -p 8000:8000 fastapi-business-crud
```

Swagger

```
http://localhost:8000/docs
```

---

## Authentication

Login endpoint

```
POST /token
```

Demo credentials

```
username: demo
password: demo123
```

Use the returned token in Swagger **Authorize**

```
Bearer <access_token>
```

---

## Endpoints

Tasks API

```
GET     /tasks
POST    /tasks
GET     /tasks/{task_id}
PATCH   /tasks/{task_id}
DELETE  /tasks/{task_id}
```

---

## Purpose

Minimal example of a business-style CRUD API using FastAPI.