from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlmodel import Session
from typing import Annotated, List
import uuid
from ..database import get_session
from ..models.user import User
from ..models.task import Task, TaskCreate, TaskUpdate, TaskResponse
from ..middleware.auth import get_current_user
from ..services.task_service import TaskService

router = APIRouter(prefix="/api/{user_id}/tasks", tags=["Tasks"])


def verify_user_access(user_id: uuid.UUID, current_user: User):
    """Verify that the user_id in the URL matches the authenticated user."""
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own tasks"
        )


@router.get("/", response_model=dict)
def get_tasks(
    user_id: Annotated[uuid.UUID, Path()],
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)]
):
    """Get all tasks for the authenticated user."""
    verify_user_access(user_id, current_user)

    tasks = TaskService.get_all_tasks(session, user_id)

    return {
        "tasks": [TaskResponse.model_validate(task) for task in tasks],
        "total": len(tasks),
        "limit": 100,
        "offset": 0
    }


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    user_id: Annotated[uuid.UUID, Path()],
    task_data: TaskCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)]
):
    """Create a new task."""
    verify_user_access(user_id, current_user)

    task = TaskService.create_task(session, task_data, user_id)
    return TaskResponse.model_validate(task)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    user_id: Annotated[uuid.UUID, Path()],
    task_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)]
):
    """Get a specific task by ID."""
    verify_user_access(user_id, current_user)

    task = TaskService.get_task_by_id(session, task_id, user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return TaskResponse.model_validate(task)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task_full(
    user_id: Annotated[uuid.UUID, Path()],
    task_id: int,
    task_data: TaskCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)]
):
    """Update a task (replace all fields)."""
    verify_user_access(user_id, current_user)

    task_update = TaskUpdate(
        title=task_data.title,
        description=task_data.description,
        completed=False
    )

    task = TaskService.update_task(session, task_id, task_update, user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return TaskResponse.model_validate(task)


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task_partial(
    user_id: Annotated[uuid.UUID, Path()],
    task_id: int,
    task_update: TaskUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)]
):
    """Partially update a task."""
    verify_user_access(user_id, current_user)

    task = TaskService.update_task(session, task_id, task_update, user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return TaskResponse.model_validate(task)


@router.patch("/{task_id}/complete", response_model=TaskResponse)
def toggle_task_complete(
    user_id: Annotated[uuid.UUID, Path()],
    task_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)]
):
    """Toggle task completion status."""
    verify_user_access(user_id, current_user)

    task = TaskService.toggle_complete(session, task_id, user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return TaskResponse.model_validate(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    user_id: Annotated[uuid.UUID, Path()],
    task_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)]
):
    """Delete a task."""
    verify_user_access(user_id, current_user)

    success = TaskService.delete_task(session, task_id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return None
