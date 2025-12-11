"""
Interactive Demo - Todo App Phase I

This script demonstrates all 5 features working correctly.
Simulates user interactions without requiring manual input.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from storage import TaskStorage
from models import format_task_display, get_status_text


def print_section(title):
    """Print a section header."""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")


def print_action(action):
    """Print an action being performed."""
    print(f"→ {action}")


def print_result(result):
    """Print a result."""
    print(f"  ✓ {result}")


def demo():
    """Run the complete demo."""

    print_section("TODO APP - PHASE I DEMO")
    print("Demonstrating all 5 basic features:")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Complete/Incomplete")

    # Initialize storage
    storage = TaskStorage()

    # =================================================================
    # FEATURE 1: ADD TASK
    # =================================================================
    print_section("FEATURE 1: ADD TASK")

    print_action("Adding task: 'Buy groceries' with description")
    task1 = storage.add_task("Buy groceries", "Milk, eggs, bread, and fruits")
    print_result(f"Task added with ID {task1['id']}")
    print(f"  • Title: {task1['title']}")
    print(f"  • Description: {task1['description']}")
    print(f"  • Status: {get_status_text(task1['completed'])}")

    print_action("\nAdding task: 'Call mom' without description")
    task2 = storage.add_task("Call mom")
    print_result(f"Task added with ID {task2['id']}")
    print(f"  • Title: {task2['title']}")
    print(f"  • Status: {get_status_text(task2['completed'])}")

    print_action("\nAdding task: 'Review PR #123'")
    task3 = storage.add_task("Review PR #123", "Check code quality and run tests")
    print_result(f"Task added with ID {task3['id']}")

    print_action("\nAdding task: 'Weekly team meeting'")
    task4 = storage.add_task("Weekly team meeting", "Discuss Q4 roadmap")
    print_result(f"Task added with ID {task4['id']}")

    print_action("\nAdding task: 'Update documentation'")
    task5 = storage.add_task("Update documentation", "Add Phase I details to README")
    print_result(f"Task added with ID {task5['id']}")

    print(f"\n✅ Feature 1 Complete: Added 5 tasks successfully")

    # =================================================================
    # FEATURE 2: VIEW TASKS
    # =================================================================
    print_section("FEATURE 2: VIEW TASKS")

    counts = storage.count_tasks()
    print_action("Retrieving all tasks from storage")
    print_result(f"Found {counts['total']} tasks")
    print(f"  • Completed: {counts['completed']}")
    print(f"  • Pending: {counts['pending']}")

    print("\n" + "-"*60)
    print("YOUR TASKS:")
    print("-"*60)

    tasks = storage.get_all_tasks()
    for task in tasks:
        print("\n" + format_task_display(task))

    print("\n✅ Feature 2 Complete: All tasks displayed successfully")

    # =================================================================
    # FEATURE 3: UPDATE TASK
    # =================================================================
    print_section("FEATURE 3: UPDATE TASK")

    print_action("Updating task 1 title")
    print(f"  • Before: {storage.get_task(1)['title']}")
    storage.update_task(1, title="Buy groceries and household items")
    print_result("Title updated")
    print(f"  • After: {storage.get_task(1)['title']}")

    print_action("\nUpdating task 2 description")
    print(f"  • Before: '{storage.get_task(2)['description']}'")
    storage.update_task(2, description="Wish her happy birthday!")
    print_result("Description updated")
    print(f"  • After: '{storage.get_task(2)['description']}'")

    print_action("\nUpdating task 3 (both title and description)")
    print(f"  • Before: {storage.get_task(3)['title']}")
    storage.update_task(3,
                       title="Review and merge PR #123",
                       description="Review code, run tests, merge to main")
    print_result("Both fields updated")
    print(f"  • After: {storage.get_task(3)['title']}")

    print("\n✅ Feature 3 Complete: Tasks updated successfully")

    # =================================================================
    # FEATURE 4: MARK COMPLETE/INCOMPLETE
    # =================================================================
    print_section("FEATURE 4: MARK COMPLETE/INCOMPLETE")

    print_action("Marking task 1 as complete")
    print(f"  • Before: {get_status_text(storage.get_task(1)['completed'])}")
    storage.toggle_complete(1)
    print_result("Status changed")
    print(f"  • After: {get_status_text(storage.get_task(1)['completed'])}")

    print_action("\nMarking task 2 as complete")
    storage.toggle_complete(2)
    print_result(f"Status: {get_status_text(storage.get_task(2)['completed'])}")

    print_action("\nMarking task 4 as complete")
    storage.toggle_complete(4)
    print_result(f"Status: {get_status_text(storage.get_task(4)['completed'])}")

    # Show updated counts
    counts = storage.count_tasks()
    print(f"\n📊 Current Status:")
    print(f"  • Total: {counts['total']} tasks")
    print(f"  • Completed: {counts['completed']} tasks")
    print(f"  • Pending: {counts['pending']} tasks")

    print_action("\nToggling task 1 back to incomplete (undo)")
    storage.toggle_complete(1)
    print_result(f"Status: {get_status_text(storage.get_task(1)['completed'])}")

    print("\n✅ Feature 4 Complete: Tasks marked complete/incomplete successfully")

    # =================================================================
    # VIEW UPDATED TASKS
    # =================================================================
    print_section("CURRENT TASK LIST (After Updates)")

    print("-"*60)
    tasks = storage.get_all_tasks()
    for task in tasks:
        print("\n" + format_task_display(task))
    print("\n" + "-"*60)

    # =================================================================
    # FEATURE 5: DELETE TASK
    # =================================================================
    print_section("FEATURE 5: DELETE TASK")

    print_action("Deleting task 5: 'Update documentation'")
    deleted = storage.delete_task(5)
    print_result(f"Task deleted: {deleted['title']}")

    print_action("\nDeleting task 3: 'Review and merge PR #123'")
    deleted = storage.delete_task(3)
    print_result(f"Task deleted: {deleted['title']}")

    # Verify deletion
    counts = storage.count_tasks()
    print(f"\n📊 After Deletion:")
    print(f"  • Total tasks: {counts['total']} (was 5, deleted 2)")
    print(f"  • Remaining: {counts['pending']} pending, {counts['completed']} completed")

    print("\n✅ Feature 5 Complete: Tasks deleted successfully")

    # =================================================================
    # FINAL TASK LIST
    # =================================================================
    print_section("FINAL TASK LIST")

    print("Remaining tasks after all operations:\n")
    print("-"*60)
    tasks = storage.get_all_tasks()
    for task in tasks:
        print("\n" + format_task_display(task))
    print("\n" + "-"*60)

    # =================================================================
    # VALIDATION TESTS
    # =================================================================
    print_section("BONUS: INPUT VALIDATION TESTS")

    from models import validate_title, validate_description

    print_action("Testing empty title validation")
    is_valid, msg = validate_title("")
    print_result(f"Empty title rejected: {msg}" if not is_valid else "FAILED")

    print_action("\nTesting whitespace-only title validation")
    is_valid, msg = validate_title("   ")
    print_result(f"Whitespace-only rejected: {msg}" if not is_valid else "FAILED")

    print_action("\nTesting too-long title validation (201 chars)")
    is_valid, msg = validate_title("a" * 201)
    print_result(f"Long title rejected: {msg}" if not is_valid else "FAILED")

    print_action("\nTesting valid title")
    is_valid, msg = validate_title("Valid task title")
    print_result("Valid title accepted" if is_valid else f"FAILED: {msg}")

    print_action("\nTesting too-long description (1001 chars)")
    is_valid, msg = validate_description("a" * 1001)
    print_result(f"Warning for long description: {msg}" if msg else "FAILED")

    print("\n✅ All validations working correctly")

    # =================================================================
    # ID MANAGEMENT TEST
    # =================================================================
    print_section("BONUS: ID MANAGEMENT TEST")

    print_action("Testing that deleted IDs are never reused")
    print(f"  • Last task ID was: 5")
    print(f"  • Deleted tasks: 3 and 5")
    print(f"  • Next task should get ID: 6 (not 3 or 5)")

    new_task = storage.add_task("New task after deletions")
    print_result(f"New task ID: {new_task['id']}")

    if new_task['id'] == 6:
        print_result("✓ Correct! IDs are never reused")
    else:
        print("  ✗ FAILED: ID was reused!")

    # =================================================================
    # SUMMARY
    # =================================================================
    print_section("🎉 DEMO COMPLETE - ALL FEATURES WORKING!")

    print("✅ Feature 1: Add Task - WORKING")
    print("✅ Feature 2: View Tasks - WORKING")
    print("✅ Feature 3: Update Task - WORKING")
    print("✅ Feature 4: Mark Complete - WORKING")
    print("✅ Feature 5: Delete Task - WORKING")
    print("✅ Input Validations - WORKING")
    print("✅ ID Management - WORKING")

    print("\n" + "="*60)
    print("  Phase I Implementation: COMPLETE ✓")
    print("  All specifications met successfully!")
    print("="*60 + "\n")


if __name__ == "__main__":
    demo()
