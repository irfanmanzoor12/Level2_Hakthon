# Todo App - Phase I Overview

## Project Information
- **Phase**: Phase I - In-Memory Python Console App
- **Hackathon**: Hackathon II - The Evolution of Todo
- **Points**: 100
- **Status**: In Development

## Purpose
Build a command-line todo application that stores tasks in memory using Claude Code and Spec-Kit Plus. This serves as the foundation for subsequent phases that will evolve this into a cloud-native AI system.

## Technology Stack
- **Language**: Python 3.13+
- **Package Manager**: UV
- **Development Approach**: Spec-Driven Development
- **Tools**: Claude Code, Spec-Kit Plus

## Features (Basic Level)

### ✅ Core Features
1. **Add Task** - Create new todo items with title and description
2. **View Tasks** - Display all tasks with status indicators
3. **Update Task** - Modify existing task details
4. **Delete Task** - Remove tasks from the list
5. **Mark Complete** - Toggle task completion status

## Project Structure
```
hackathon-todo-phase1/
├── .spec-kit/
│   └── config.yaml          # Spec-Kit configuration
├── specs/
│   ├── constitution.md       # High-level vision & principles
│   ├── overview.md          # This file
│   └── features/            # Feature specifications
│       ├── add-task.md
│       ├── view-tasks.md
│       ├── update-task.md
│       ├── delete-task.md
│       └── mark-complete.md
├── src/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── models.py            # Task data model
│   ├── storage.py           # In-memory storage management
│   └── ui.py                # User interface functions
├── CLAUDE.md                # Instructions for Claude Code
├── README.md                # Setup and usage instructions
└── pyproject.toml           # UV dependency management
```

## Data Model

### Task
```python
{
    "id": int,              # Unique identifier (auto-increment)
    "title": str,           # Task title (required, 1-200 chars)
    "description": str,     # Task description (optional, max 1000 chars)
    "completed": bool,      # Completion status (default: False)
    "created_at": datetime, # Creation timestamp
    "updated_at": datetime  # Last update timestamp
}
```

## User Interface Flow

```
┌─────────────────────────────────┐
│      TODO APP - MAIN MENU       │
├─────────────────────────────────┤
│ 1. Add Task                     │
│ 2. View All Tasks               │
│ 3. Update Task                  │
│ 4. Delete Task                  │
│ 5. Mark Task Complete/Incomplete│
│ 6. Exit                         │
└─────────────────────────────────┘
```

## Success Criteria
- ✅ All 5 basic features implemented
- ✅ Clean code following Python best practices
- ✅ Spec-driven development process documented
- ✅ Working console application with menu interface
- ✅ Proper error handling and user feedback
- ✅ Clear documentation (README, CLAUDE.md)

## Development Approach
This project follows **Spec-Driven Development**:
1. Specifications are written first (in /specs directory)
2. Claude Code generates implementation from specs
3. Code is tested and specs are refined as needed
4. No manual code writing - specifications drive everything

## Next Steps
After Phase I completion:
- **Phase II**: Transform into web application with Next.js + FastAPI
- **Phase III**: Add AI chatbot interface with OpenAI ChatKit
- **Phase IV**: Deploy on local Kubernetes (Minikube)
- **Phase V**: Cloud deployment on DigitalOcean with Kafka & Dapr

## Resources
- Hackathon Documentation: Provided by instructors
- Spec-Kit Plus: github.com/panaversity/spec-kit-plus
- Claude Code: claude.com/product/claude-code
- Python UV: docs.astral.sh/uv/
