from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.task import TaskCreate, TaskUpdate, TaskOut
from crud.task import(
    create_task,
    get_tasks,
    get_task,
    update_task,
    delete_task,
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskOut)
def create(task: TaskCreate, db: Session = Depends(get_db)):
    return create_task(db, task)


@router.get("/", response_model=list[TaskOut])
def read_all(db: Session = Depends(get_db)):
    return get_tasks(db)


@router.get("/{task_id}", response_model=TaskOut)
def read(task_id: int, db: Session = Depends(get_db)):
    return get_task(db, task_id)


@router.patch("/{task_id}", response_model=TaskOut)
def update(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    return update_task(db, task_id, task)


@router.delete("/{task_id}")
def delete(task_id: int, db: Session = Depends(get_db)):
    return delete_task(db, task_id)