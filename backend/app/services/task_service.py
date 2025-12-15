from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
import uuid
from ..models.task import Task, TaskCreate, TaskUpdate


class TaskService:
    """Service for task operations."""

    @staticmethod
    def get_all_tasks(session: Session, user_id: uuid.UUID) -> List[Task]:
        """Get all tasks for a user."""
        statement = select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
        return session.exec(statement).all()

    @staticmethod
    def get_task_by_id(session: Session, task_id: int, user_id: uuid.UUID) -> Optional[Task]:
        """Get a specific task by ID."""
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        return session.exec(statement).first()

    @staticmethod
    def create_task(session: Session, task_data: TaskCreate, user_id: uuid.UUID) -> Task:
        """Create a new task."""
        # Truncate description if too long
        description = task_data.description
        if description and len(description) > 1000:
            description = description[:1000]

        task = Task(
            user_id=user_id,
            title=task_data.title,
            description=description,
            completed=False,
            due_date=task_data.due_date,
            tags=task_data.tags if task_data.tags else []
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def update_task(
        session: Session,
        task_id: int,
        task_update: TaskUpdate,
        user_id: uuid.UUID
    ) -> Optional[Task]:
        """Update a task."""
        task = TaskService.get_task_by_id(session, task_id, user_id)
        if not task:
            return None

        # Update only provided fields
        update_data = task_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if field == "description" and value and len(value) > 1000:
                value = value[:1000]
            setattr(task, field, value)

        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def toggle_complete(session: Session, task_id: int, user_id: uuid.UUID) -> Optional[Task]:
        """Toggle task completion status."""
        task = TaskService.get_task_by_id(session, task_id, user_id)
        if not task:
            return None

        task.completed = not task.completed
        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def delete_task(session: Session, task_id: int, user_id: uuid.UUID) -> bool:
        """Delete a task."""
        task = TaskService.get_task_by_id(session, task_id, user_id)
        if not task:
            return False

        session.delete(task)
        session.commit()
        return True
