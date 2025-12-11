"""
Test script to verify all features work according to specs.

This script programmatically tests all core functionality without user interaction.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from storage import TaskStorage
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from models import validate_title, validate_description


def test_add_task():
    """Test adding tasks."""
    print("Testing: Add Task...")
    storage = TaskStorage()

    # Test valid task
    task1 = storage.add_task("Buy groceries", "Milk and eggs")
    assert task1["id"] == 1
    assert task1["title"] == "Buy groceries"
    assert task1["description"] == "Milk and eggs"
    assert task1["completed"] is False

    # Test task without description
    task2 = storage.add_task("Call mom")
    assert task2["id"] == 2
    assert task2["description"] == ""

    print("✓ Add Task: PASSED")
    return storage


def test_view_tasks(storage):
    """Test viewing tasks."""
    print("Testing: View Tasks...")

    tasks = storage.get_all_tasks()
    assert len(tasks) == 2
    assert tasks[0]["id"] == 1
    assert tasks[1]["id"] == 2

    counts = storage.count_tasks()
    assert counts["total"] == 2
    assert counts["pending"] == 2
    assert counts["completed"] == 0

    print("✓ View Tasks: PASSED")


def test_update_task(storage):
    """Test updating tasks."""
    print("Testing: Update Task...")

    # Update title
    updated = storage.update_task(1, title="Buy groceries and fruits")
    assert updated["title"] == "Buy groceries and fruits"
    assert updated["description"] == "Milk and eggs"  # Description unchanged

    # Update description
    updated = storage.update_task(1, description="Milk, eggs, and apples")
    assert updated["title"] == "Buy groceries and fruits"  # Title unchanged
    assert updated["description"] == "Milk, eggs, and apples"

    # Update both
    updated = storage.update_task(2, title="Call mom tonight", description="Wish happy birthday")
    assert updated["title"] == "Call mom tonight"
    assert updated["description"] == "Wish happy birthday"

    print("✓ Update Task: PASSED")


def test_mark_complete(storage):
    """Test marking tasks complete/incomplete."""
    print("Testing: Mark Complete...")

    # Mark as complete
    task = storage.toggle_complete(1)
    assert task["completed"] is True

    # Mark as incomplete (toggle back)
    task = storage.toggle_complete(1)
    assert task["completed"] is False

    # Mark another task complete
    task = storage.toggle_complete(2)
    assert task["completed"] is True

    counts = storage.count_tasks()
    assert counts["completed"] == 1
    assert counts["pending"] == 1

    print("✓ Mark Complete: PASSED")


def test_delete_task(storage):
    """Test deleting tasks."""
    print("Testing: Delete Task...")

    # Delete task
    deleted = storage.delete_task(1)
    assert deleted["id"] == 1
    assert deleted["title"] == "Buy groceries and fruits"

    # Verify deleted
    task = storage.get_task(1)
    assert task is None

    # Verify count
    counts = storage.count_tasks()
    assert counts["total"] == 1

    # Verify remaining tasks
    tasks = storage.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0]["id"] == 2

    print("✓ Delete Task: PASSED")


def test_validations():
    """Test input validations."""
    print("Testing: Validations...")

    # Title validations
    is_valid, msg = validate_title("")
    assert not is_valid

    is_valid, msg = validate_title("   ")
    assert not is_valid

    is_valid, msg = validate_title("a" * 201)
    assert not is_valid

    is_valid, msg = validate_title("Valid title")
    assert is_valid

    # Description validations
    is_valid, msg = validate_description("")
    assert is_valid

    is_valid, msg = validate_description("a" * 1001)
    assert is_valid  # Valid but with warning

    print("✓ Validations: PASSED")


def test_id_management():
    """Test ID management (no reuse of deleted IDs)."""
    print("Testing: ID Management...")

    storage = TaskStorage()

    # Add 3 tasks
    task1 = storage.add_task("Task 1")
    task2 = storage.add_task("Task 2")
    task3 = storage.add_task("Task 3")

    assert task1["id"] == 1
    assert task2["id"] == 2
    assert task3["id"] == 3

    # Delete task 2
    storage.delete_task(2)

    # Add new task - should get ID 4, not 2
    task4 = storage.add_task("Task 4")
    assert task4["id"] == 4

    print("✓ ID Management: PASSED")


def main():
    """Run all tests."""
    print("\n" + "="*50)
    print("  Todo App Phase I - Test Suite")
    print("="*50 + "\n")

    try:
        # Run tests in sequence
        storage = test_add_task()
        test_view_tasks(storage)
        test_update_task(storage)
        test_mark_complete(storage)
        test_delete_task(storage)
        test_validations()
        test_id_management()

        print("\n" + "="*50)
        print("  ✓ ALL TESTS PASSED!")
        print("="*50 + "\n")

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}\n")
        raise


if __name__ == "__main__":
    main()
