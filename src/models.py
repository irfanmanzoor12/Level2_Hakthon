"""
Task Data Model

Defines the Task data structure and validation logic according to:
- @specs/constitution.md
- @specs/features/*.md
"""

from datetime import datetime
from typing import TypedDict

class Task(TypedDict):
    """
    Task data structure.

    Attributes:
        id: Unique identifier (auto-increment, never reused)
        title: Task title (1-200 characters, required)
        description: Task description (0-1000 characters, optional)
        completed: Completion status (default: False)
        created_at: Creation timestamp (ISO format)
        updated_at: Last update timestamp (ISO format)
    """
    id: int
    title: str
    description: str
    completed: bool
    created_at: str
    updated_at: str


def create_task(task_id: int, title: str, description: str = "") -> Task:
    """
    Create a new Task object with validated fields.

    Args:
        task_id: Unique task identifier
        title: Task title (already validated)
        description: Task description (already validated)

    Returns:
        Task object with all required fields
    """
    now = datetime.now().isoformat()

    return Task(
        id=task_id,
        title=title,
        description=description,
        completed=False,
        created_at=now,
        updated_at=now
    )


def validate_title(title: str) -> tuple[bool, str]:
    """
    Validate task title according to spec.

    Rules:
    - Required (cannot be empty)
    - 1-200 characters
    - Must contain at least one non-whitespace character

    Args:
        title: Title to validate

    Returns:
        Tuple of (is_valid, error_message)
        - If valid: (True, "")
        - If invalid: (False, "error message")
    """
    # Check if empty
    if not title:
        return False, "Title cannot be empty. Please try again."

    # Check if only whitespace
    if not title.strip():
        return False, "Title cannot be only whitespace. Please enter a valid title."

    # Check length
    if len(title) > 200:
        return False, "Title is too long (max 200 characters). Please enter a shorter title."

    return True, ""


def validate_description(description: str) -> tuple[bool, str]:
    """
    Validate task description according to spec.

    Rules:
    - Optional (can be empty)
    - Maximum 1000 characters (truncate with warning if longer)

    Args:
        description: Description to validate

    Returns:
        Tuple of (is_valid, warning_message)
        - If valid: (True, "")
        - If truncated: (True, "warning message")
    """
    if len(description) > 1000:
        return True, "⚠ Warning: Description truncated to 1000 characters."

    return True, ""


def truncate_description(description: str) -> str:
    """
    Truncate description to 1000 characters if needed.

    Args:
        description: Description to truncate

    Returns:
        Truncated description (max 1000 chars)
    """
    return description[:1000] if len(description) > 1000 else description


def format_task_display(task: Task, show_description: bool = True) -> str:
    """
    Format task for display.

    Args:
        task: Task to format
        show_description: Whether to include description

    Returns:
        Formatted task string
    """
    # Status indicator
    status = "✓" if task["completed"] else "○"

    # Truncate title if too long for display
    title = task["title"]
    if len(title) > 50:
        title = title[:50] + "..."

    # Build display string
    display = f"[{task['id']}] {status} {title}"

    if show_description and task["description"]:
        desc = task["description"]
        if len(desc) > 100:
            desc = desc[:100] + "..."
        display += f"\n    {desc}"

    return display


def get_status_text(completed: bool) -> str:
    """
    Get human-readable status text.

    Args:
        completed: Task completion status

    Returns:
        "Completed" or "Pending"
    """
    return "Completed" if completed else "Pending"
