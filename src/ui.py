"""
User Interface Functions

Handles all user input/output according to:
- @specs/constitution.md
- @specs/features/*.md
"""

from typing import Optional
from models import (
    Task,
    validate_title,
    validate_description,
    truncate_description,
    format_task_display,
    get_status_text
)
from storage import TaskStorage


def clear_screen():
    """Clear the console screen (simple version - just print newlines)."""
    print("\n" * 2)


def print_header(title: str):
    """
    Print a formatted header.

    Args:
        title: Header text
    """
    print(f"\n=== {title} ===\n")


def print_success(message: str):
    """
    Print a success message.

    Args:
        message: Success message
    """
    print(f"✓ {message}")


def print_error(message: str):
    """
    Print an error message.

    Args:
        message: Error message
    """
    print(f"❌ Error: {message}")


def print_warning(message: str):
    """
    Print a warning message.

    Args:
        message: Warning message
    """
    print(message)


def wait_for_enter():
    """Wait for user to press Enter to continue."""
    input("\nPress Enter to return to main menu...")


def get_input(prompt: str) -> str:
    """
    Get user input with a prompt.

    Args:
        prompt: Prompt to display

    Returns:
        User input as string
    """
    return input(prompt)


def get_int_input(prompt: str) -> Optional[int]:
    """
    Get integer input from user.

    Args:
        prompt: Prompt to display

    Returns:
        Integer if valid, None if invalid
    """
    try:
        return int(get_input(prompt))
    except ValueError:
        return None


def show_main_menu() -> int:
    """
    Display main menu and get user choice.

    Returns:
        User's menu choice (1-6)
    """
    print_header("TODO APP - MAIN MENU")
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Task Complete/Incomplete")
    print("6. Exit")

    choice = get_int_input("\nEnter your choice (1-6): ")
    return choice if choice else 0


def add_task_ui(storage: TaskStorage):
    """
    Add task user interface.

    Implements: @specs/features/add-task.md

    Args:
        storage: Task storage instance
    """
    print_header("ADD NEW TASK")

    # Get and validate title
    while True:
        title = get_input("Enter task title: ")
        is_valid, error_msg = validate_title(title)

        if is_valid:
            break
        else:
            print_error(error_msg)

    # Get and validate description
    description = get_input("Enter task description (press Enter to skip): ")
    is_valid, warning_msg = validate_description(description)

    if warning_msg:
        print_warning(warning_msg)

    description = truncate_description(description)

    # Add task
    task = storage.add_task(title, description)

    # Confirmation
    print()
    print_success("Task added successfully!")
    print(f"  ID: {task['id']}")
    print(f"  Title: {task['title']}")
    print(f"  Status: {get_status_text(task['completed'])}")

    wait_for_enter()


def view_tasks_ui(storage: TaskStorage):
    """
    View tasks user interface.

    Implements: @specs/features/view-tasks.md

    Args:
        storage: Task storage instance
    """
    print_header("YOUR TASKS")

    if storage.is_empty():
        print("No tasks yet. Add your first task to get started!\n")
        wait_for_enter()
        return

    # Get counts
    counts = storage.count_tasks()
    print(f"Total: {counts['total']} tasks ({counts['completed']} completed, {counts['pending']} pending)\n")

    # Display all tasks
    tasks = storage.get_all_tasks()
    for task in tasks:
        print(format_task_display(task))
        print()  # Blank line between tasks

    wait_for_enter()


def update_task_ui(storage: TaskStorage):
    """
    Update task user interface.

    Implements: @specs/features/update-task.md

    Args:
        storage: Task storage instance
    """
    print_header("UPDATE TASK")

    # Check if storage is empty
    if storage.is_empty():
        print_error("No tasks available to update.")
        wait_for_enter()
        return

    # Get task ID
    task_id = get_int_input("Enter task ID to update: ")

    if task_id is None:
        print_error("Please enter a valid task ID (number).")
        wait_for_enter()
        return

    # Get task
    task = storage.get_task(task_id)
    if not task:
        print_error(f"Task with ID {task_id} not found.")
        wait_for_enter()
        return

    # Display current task
    print("\nCurrent task:")
    print(format_task_display(task))

    # Show update options
    print("\nWhat would you like to update?")
    print("1. Title only")
    print("2. Description only")
    print("3. Both title and description")
    print("4. Cancel")

    choice = get_int_input("\nEnter your choice (1-4): ")

    if choice == 4:
        print("Operation cancelled. Returning to main menu.")
        wait_for_enter()
        return

    new_title = None
    new_description = None

    # Get new values based on choice
    if choice in [1, 3]:  # Update title
        print(f"\nCurrent title: {task['title']}")
        while True:
            if choice == 3:
                title_input = get_input("Enter new title (or press Enter to keep current): ")
                if not title_input:  # Keep current
                    break
            else:
                title_input = get_input("Enter new title: ")

            is_valid, error_msg = validate_title(title_input) if title_input else (True, "")

            if is_valid:
                new_title = title_input if title_input else None
                break
            else:
                print_error(error_msg)

    if choice in [2, 3]:  # Update description
        print(f"\nCurrent description: {task['description']}")
        desc_input = get_input("Enter new description (or press Enter to keep current): ")

        if desc_input or choice == 2:  # If something entered or description-only mode
            is_valid, warning_msg = validate_description(desc_input)
            if warning_msg:
                print_warning(warning_msg)
            new_description = truncate_description(desc_input)

    if choice not in [1, 2, 3]:
        print_error("Invalid choice.")
        wait_for_enter()
        return

    # Update task
    updated_task = storage.update_task(task_id, new_title, new_description)

    # Confirmation
    print()
    print_success("Task updated successfully!")
    print(f"  ID: {updated_task['id']}")
    print(f"  Title: {updated_task['title']}")
    print(f"  Description: {updated_task['description']}")
    print(f"  Status: {get_status_text(updated_task['completed'])}")

    wait_for_enter()


def delete_task_ui(storage: TaskStorage):
    """
    Delete task user interface.

    Implements: @specs/features/delete-task.md

    Args:
        storage: Task storage instance
    """
    print_header("DELETE TASK")

    # Check if storage is empty
    if storage.is_empty():
        print_error("No tasks available to delete.")
        wait_for_enter()
        return

    # Get task ID
    task_id = get_int_input("Enter task ID to delete: ")

    if task_id is None:
        print_error("Please enter a valid task ID (number).")
        wait_for_enter()
        return

    # Get task
    task = storage.get_task(task_id)
    if not task:
        print_error(f"Task with ID {task_id} not found.")
        wait_for_enter()
        return

    # Display task to be deleted
    print("\nTask to be deleted:")
    print(format_task_display(task))

    # Confirmation
    print("\n⚠ Are you sure you want to delete this task? This cannot be undone.")
    confirmation = get_input("Type 'yes' or 'y' to confirm, or anything else to cancel: ")

    if confirmation.lower() not in ['yes', 'y']:
        print("\nDeletion cancelled. Task was not deleted.")
        wait_for_enter()
        return

    # Delete task
    deleted_task = storage.delete_task(task_id)

    # Confirmation
    print()
    print_success("Task deleted successfully!")
    print(f"  ID: {deleted_task['id']}")
    print(f"  Title: {deleted_task['title']}")

    wait_for_enter()


def mark_complete_ui(storage: TaskStorage):
    """
    Mark task complete/incomplete user interface.

    Implements: @specs/features/mark-complete.md

    Args:
        storage: Task storage instance
    """
    print_header("MARK TASK COMPLETE/INCOMPLETE")

    # Check if storage is empty
    if storage.is_empty():
        print_error("No tasks available to update.")
        wait_for_enter()
        return

    # Get task ID
    task_id = get_int_input("Enter task ID: ")

    if task_id is None:
        print_error("Please enter a valid task ID (number).")
        wait_for_enter()
        return

    # Get task
    task = storage.get_task(task_id)
    if not task:
        print_error(f"Task with ID {task_id} not found.")
        wait_for_enter()
        return

    # Display current task
    print("\nCurrent task:")
    print(format_task_display(task))
    print(f"Status: {get_status_text(task['completed'])}")

    # Toggle completion
    updated_task = storage.toggle_complete(task_id)

    # Confirmation
    print()
    if updated_task["completed"]:
        print_success("Task marked as complete!")
    else:
        print_success("Task marked as incomplete!")

    print(f"  ID: {updated_task['id']}")
    print(f"  Title: {updated_task['title']}")
    print(f"  New Status: {get_status_text(updated_task['completed'])}")

    wait_for_enter()
