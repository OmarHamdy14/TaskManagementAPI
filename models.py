from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.sql import func
from database import Base
import enum

class TaskStatus(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"

class TaskPriority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=True)
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.pending)
    priority = Column(Enum(TaskPriority), nullable=False, default=TaskPriority.medium)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    due_date = Column(DateTime, nullable=True)
    assigned_to = Column(String(100), nullable=True)
