from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import time


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None)
    user_id: str = Field(index=True)  # Using string for user_id as it could be UUID
    completed: bool = Field(default=False)


class TaskCreate(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)


class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None)
    completed: Optional[str] = Field(default=None)


class Task(TaskBase, table=True):
    __tablename__ = "task"
    __table_args__ = {'extend_existing': True}  # Allow extending existing table
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
