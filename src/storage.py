"""
In-Memory Task Storage

Manages task storage and CRUD operations according to:
- @specs/constitution.md
- @specs/features/*.md
"""

from datetime import datetime
from typing import Optional
from models import Task, create_task


class TaskStorage:
    """
    In-memory storage for tasks.

    Features:
    - Auto-incrementing IDs
    - Never reuses deleted task IDs
    - Maintains task list during program execution
    """

    def __init__(self):
        """Initialize empty task storage."""
        self.tasks: dict[int, Task] = {}
        self.next_id: int = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Add a new task to storage.

        Args:
            title: Task title (already validated)
            description: Task description (already validated)

        Returns:
            Created Task object
        """
        task = create_task(self.next_id, title, description)
        self.tasks[self.next_id] = task
        self.next_id += 1
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Get a task by ID.

        Args:
            task_id: Task ID to retrieve

        Returns:
            Task if found, None otherwise
        """
        return self.tasks.get(task_id)

    def get_all_tasks(self) -> list[Task]:
        """
        Get all tasks in order of creation (by ID).

        Returns:
            List of all tasks, sorted by ID
        """
        return [self.tasks[task_id] for task_id in sorted(self.tasks.keys())]

    def update_task(self, task_id: int, title: Optional[str] = None,
                    description: Optional[str] = None) -> Optional[Task]:
        """
        Update a task's title and/or description.

        Args:
            task_id: Task ID to update
            title: New title (None to keep current)
            description: New description (None to keep current)

        Returns:
            Updated Task if found, None otherwise
        """
        task = self.get_task(task_id)
        if not task:
            return None

        # Update fields
        if title is not None:
            task["title"] = title
        if description is not None:
            task["description"] = description

        # Update timestamp
        task["updated_at"] = datetime.now().isoformat()

        return task

    def delete_task(self, task_id: int) -> Optional[Task]:
        """
        Delete a task from storage.

        Note: Deleted task IDs are NEVER reused.

        Args:
            task_id: Task ID to delete

        Returns:
            Deleted Task if found, None otherwise
        """
        if task_id not in self.tasks:
            return None

        task = self.tasks[task_id]
        del self.tasks[task_id]
        return task

    def toggle_complete(self, task_id: int) -> Optional[Task]:
        """
        Toggle a task's completion status.

        Args:
            task_id: Task ID to toggle

        Returns:
            Updated Task if found, None otherwise
        """
        task = self.get_task(task_id)
        if not task:
            return None

        # Toggle completion status
        task["completed"] = not task["completed"]

        # Update timestamp
        task["updated_at"] = datetime.now().isoformat()

        return task

    def count_tasks(self) -> dict[str, int]:
        """
        Count total, completed, and pending tasks.

        Returns:
            Dictionary with counts: {"total": n, "completed": n, "pending": n}
        """
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks.values() if task["completed"])
        pending = total - completed

        return {
            "total": total,
            "completed": completed,
            "pending": pending
        }

    def is_empty(self) -> bool:
        """
        Check if storage is empty.

        Returns:
            True if no tasks exist, False otherwise
        """
        return len(self.tasks) == 0
