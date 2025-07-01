from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from models import TaskStatus, TaskPriority

class TaskCreate(BaseModel):
    title: str = Field(..., max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: TaskStatus = TaskStatus.pending
    priority: TaskPriority = TaskPriority.medium
    due_date: Optional[datetime] = None
    assigned_to: Optional[str] = Field(None, max_length=100)

    @field_validator("title")
    @classmethod
    def validate_title(cls, v):
        if not v.strip():
            raise ValueError("Title must not be empty or whitespace only")
        return v.strip()

    @field_validator("due_date")
    @classmethod
    def validate_due_date(cls, v):
        if v and v <= datetime.utcnow():
            raise ValueError("Due date must be in the future")
        return v

class TaskUpdate(TaskCreate):
    title: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None

class TaskOut(TaskCreate):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
