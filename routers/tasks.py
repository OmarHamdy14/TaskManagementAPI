from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc
from typing import List, Optional
from database import SessionLocal
import schemas, models

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/info", tags=["Root"])
def root():
    return {
        "message": "Welcome to Task Management API",
        "endpoints": [
            "POST /tasks/",
            "GET /tasks/",
            "GET /tasks/{task_id}",
            "PUT /tasks/{task_id}",
            "DELETE /tasks/{task_id}",
            "GET /tasks/status/{status}",
            "GET /tasks/priority/{priority}",
            "DELETE /tasks/bulk",
            "PUT /tasks/bulk",
            "GET /tasks/info",
            "GET /tasks/health"
        ]
    }

@router.get("/health", tags=["Health"])
def health():
    return {"status": "Success"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/", response_model=List[schemas.TaskOut], status_code=status.HTTP_200_OK)
def list_tasks(
    skip: int = 0,
    limit: int = 10,
    status_filter: Optional[models.TaskStatus] = None,
    priority_filter: Optional[models.TaskPriority] = None,
    assigned_to: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: Optional[str] = Query("created_at"),
    sort_order: Optional[str] = Query("desc"),
    db: Session = Depends(get_db)
):
    query = db.query(models.Task)

    if status_filter:
        query = query.filter(models.Task.status == status_filter)
    if priority_filter:
        query = query.filter(models.Task.priority == priority_filter)
    if assigned_to:
        query = query.filter(models.Task.assigned_to.ilike(f"%{assigned_to}%"))
    if search:
        query = query.filter(
            or_(
                models.Task.title.ilike(f"%{search}%"),
                models.Task.description.ilike(f"%{search}%")
            )
        )

    if sort_order == "desc":
        query = query.order_by(desc(getattr(models.Task, sort_by, models.Task.created_at)))
    else:
        query = query.order_by(asc(getattr(models.Task, sort_by, models.Task.created_at)))

    return query.offset(skip).limit(limit).all()

@router.get("/{task_id}", response_model=schemas.TaskOut, status_code=status.HTTP_200_OK)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=schemas.TaskOut, status_code=status.HTTP_200_OK)
def update_task(task_id: int, update: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    for key, value in update.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"detail": "Task deleted"}

@router.get("/status/{status}", response_model=List[schemas.TaskOut], status_code=status.HTTP_200_OK)
def filter_by_status(status: models.TaskStatus, db: Session = Depends(get_db)):
    return db.query(models.Task).filter(models.Task.status == status).all()

@router.get("/priority/{priority}", response_model=List[schemas.TaskOut], status_code=status.HTTP_200_OK)
def filter_by_priority(priority: models.TaskPriority, db: Session = Depends(get_db)):
    return db.query(models.Task).filter(models.Task.priority == priority).all()

@router.delete("/bulk", status_code=status.HTTP_200_OK)
def bulk_delete(task_ids: List[int], db: Session = Depends(get_db)):
    tasks = db.query(models.Task).filter(models.Task.id.in_(task_ids)).all()
    if not tasks:
        raise HTTPException(status_code=404, detail="No matching tasks found")
    for task in tasks:
        db.delete(task)
    db.commit()
    return {"detail": f"Deleted {len(tasks)} tasks"}

@router.put("/bulk", response_model=List[schemas.TaskOut], status_code=status.HTTP_200_OK)
def bulk_update(task_ids: List[int], update: schemas.TaskUpdate, db: Session = Depends(get_db)):
    tasks = db.query(models.Task).filter(models.Task.id.in_(task_ids)).all()
    if not tasks:
        raise HTTPException(status_code=404, detail="No matching tasks found")
    for task in tasks:
        for key, value in update.model_dump(exclude_unset=True).items():
            setattr(task, key, value)
    db.commit()
    return tasks
