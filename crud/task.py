from sqlalchemy.orm import Session
from fastapi import HTTPException

from db.models.task import Task
from schemas.task import TaskCreate, TaskUpdate


def create_task(db: Session, task: TaskCreate):
    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_tasks(db: Session):
    return db.query(Task).all()


def get_task(db: Session, task_id: int):
    db_task = db.query(Task).filter(Task.id == task_id).first()

    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return db_task


def update_task(db: Session, task_id: int, task: TaskUpdate):
    db_task = db.query(Task).filter(Task.id == task_id).first()

    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in task.model_dump(exclude_unset=True).items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = db.query(Task).filter(Task.id == task_id).first()

    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(db_task)
    db.commit()
    return db_task

def import_tasks_from_csv(db: Session, csv_reader):
    allowed_statuses = {"todo", "doing", "done"}

    total_rows =0
    created_count = 0
    skipped_count = 0
    error_count = 0
    errors = []

    existing_titles = {
        task.title.strip().lower()
        for task in db.query(Task).all()
        if task.title
    }
    seen_titles = set(existing_titles)

    for row_index, row in enumerate(csv_reader, start=2):
        total_rows += 1

        title = (row.get("title") or "").strip()
        description = (row.get("description") or "").strip()
        status = (row.get("status") or "todo").strip().lower()

        if not title:
            error_count += 1
            errors.append({
                "row": row_index,
                "reason": "title is required"
            })
            continue

        if not status:
            status = "todo"

        if status not in allowed_statuses:
            error_count += 1
            errors.append({
                "row": row_index,
                "reason": "status must be one of: todo, doing, done"
            })
            continue

        normalized_title = title.lower()

        if normalized_title in seen_titles:
            skipped_count += 1
            continue

        db_task = Task(
            title=title,
            description=description,
            status=status,
        )
        db.add(db_task)
        seen_titles.add(normalized_title)
        created_count += 1

    db.commit()

    return {
        "total_rows": total_rows,
        "created_count": created_count,
        "skipped_count": skipped_count,
        "error_count": error_count,
        "errors": errors,
    }