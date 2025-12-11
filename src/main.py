"""
Todo App - Main Entry Point

Command-line todo application with menu-driven interface.

Implements: @specs/constitution.md and @specs/overview.md
"""

from storage import TaskStorage
from ui import (
    show_main_menu,
    add_task_ui,
    view_tasks_ui,
    update_task_ui,
    delete_task_ui,
    mark_complete_ui
)


def main():
    """
    Main application loop.

    Displays menu and handles user choices until exit.
    """
    # Initialize storage
    storage = TaskStorage()

    # Welcome message
    print("\n" + "="*50)
    print("  Welcome to Todo App - Phase I")
    print("  Spec-Driven Development with Claude Code")
    print("="*50)

    # Main loop
    while True:
        choice = show_main_menu()

        if choice == 1:
            add_task_ui(storage)
        elif choice == 2:
            view_tasks_ui(storage)
        elif choice == 3:
            update_task_ui(storage)
        elif choice == 4:
            delete_task_ui(storage)
        elif choice == 5:
            mark_complete_ui(storage)
        elif choice == 6:
            print("\n✓ Thank you for using Todo App!")
            print("Goodbye!\n")
            break
        else:
            print("\n❌ Invalid choice. Please enter a number from 1 to 6.\n")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()
