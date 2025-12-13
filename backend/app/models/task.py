from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON
from typing import Optional, List
from datetime import datetime, date
import uuid


class Task(SQLModel, table=True):
    """Task model for todo items."""
    __tablename__ = "tasks"

    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )
    user_id: uuid.UUID = Field(
        foreign_key="users.id",
        nullable=False,
        index=True
    )
    title: str = Field(
        max_length=200,
        min_length=1,
        nullable=False
    )
    description: Optional[str] = Field(
        default=None
    )
    completed: bool = Field(
        default=False,
        nullable=False,
        index=True
    )
    due_date: Optional[date] = Field(
        default=None,
        nullable=True
    )
    tags: List[str] = Field(
        default_factory=list,
        sa_column=Column(JSON)
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False
    )


class TaskCreate(SQLModel):
    """Schema for creating a task."""
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None
    due_date: Optional[date] = None
    tags: List[str] = Field(default_factory=list)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "due_date": "2025-12-20",
                "tags": ["shopping", "urgent"]
            }
        }


class TaskUpdate(SQLModel):
    """Schema for updating a task."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    completed: Optional[bool] = None
    due_date: Optional[date] = None
    tags: Optional[List[str]] = None


class TaskResponse(SQLModel):
    """Schema for task response."""
    id: int
    user_id: uuid.UUID
    title: str
    description: Optional[str]
    completed: bool
    due_date: Optional[date]
    tags: List[str]
    created_at: datetime
    updated_at: datetime
