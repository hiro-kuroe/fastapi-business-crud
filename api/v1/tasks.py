from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import csv
import io

from db.session import get_db
from schemas.task import TaskCreate, TaskUpdate, TaskOut
from crud.task import(
    create_task,
    get_tasks,
    get_task,
    update_task,
    delete_task,
    import_tasks_from_csv,
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


@router.post("/import")
def import_tasks(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="CSV file only")
    
    content = file.file.read()

    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="File must be UTF-8 encoded CSV"
        )
    
    csv_reader = csv.DictReader(io.StringIO(text))

    required_columns = {"title", "description", "status"}
    if not csv_reader.fieldnames:
        raise HTTPException(status_code=400, detail="CSV header is missing")
    
    missing = required_columns - set(csv_reader.fieldnames)
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"Missing columns: {', '.join(sorted(missing))}"
        )
    
    return import_tasks_from_csv(db, csv_reader)