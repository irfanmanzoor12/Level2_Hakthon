# Claude Code Instructions for Todo App Phase I

## Project Context
This is a **Spec-Driven Development** project for Hackathon II. All code must be generated from specifications - manual coding is not allowed per hackathon rules.

## Repository Structure
```
hackathon-todo-phase1/
├── .spec-kit/
│   └── config.yaml          # Spec-Kit configuration
├── specs/
│   ├── constitution.md       # High-level vision & principles
│   ├── overview.md          # Project overview
│   └── features/            # Feature specifications
│       ├── add-task.md      # Add new tasks
│       ├── view-tasks.md    # Display all tasks
│       ├── update-task.md   # Modify existing tasks
│       ├── delete-task.md   # Remove tasks
│       └── mark-complete.md # Toggle completion status
├── src/
│   ├── __init__.py
│   ├── main.py              # Application entry point with menu
│   ├── models.py            # Task data model and validation
│   ├── storage.py           # In-memory storage management
│   └── ui.py                # User interface and display functions
├── CLAUDE.md                # This file
├── README.md                # User-facing documentation
└── pyproject.toml           # UV dependency configuration
```

## How to Use This Project

### Reading Specifications
Before implementing any feature, ALWAYS read the relevant specification:

```markdown
@specs/constitution.md       # Understand vision and principles
@specs/overview.md           # Understand project structure
@specs/features/[feature].md # Understand specific feature requirements
```

### Implementation Order
1. Read Constitution and Overview first
2. Implement in this order:
   - models.py (Task data structure)
   - storage.py (In-memory storage)
   - ui.py (Display and input functions)
   - main.py (Menu and application flow)

### Generating Code from Specs

#### Example: Implement Add Task
```
User: "Claude, implement the add-task feature according to @specs/features/add-task.md"

Claude: [Reads spec, generates code in src/ following all requirements]
```

#### Example: Implement All Features
```
User: "Claude, implement all features from the specs folder"

Claude: [Reads all specs, generates complete implementation]
```

### Testing and Iteration
If generated code doesn't meet requirements:
1. **DON'T** manually fix code
2. **DO** refine the specification
3. Ask Claude to regenerate from updated spec

## Technical Guidelines

### Python Style
- Use Python 3.13+ features
- Follow PEP 8 style guide
- Use type hints for all functions
- Clear, descriptive variable names
- Docstrings for modules and complex functions

### Data Model
```python
Task = {
    "id": int,              # Auto-increment, never reuse
    "title": str,           # 1-200 chars, required
    "description": str,     # 0-1000 chars, optional
    "completed": bool,      # Default False
    "created_at": datetime, # ISO format
    "updated_at": datetime  # ISO format
}
```

### Storage
- Use Python list or dict for in-memory storage
- Track highest ID used (never reuse deleted IDs)
- Implement functions: add, get, update, delete, list

### User Interface
- Clear menu with numbered options
- Validate all user inputs
- Provide helpful error messages
- Confirm all state-changing operations
- Use symbols: ○ for pending, ✓ for completed

### Error Handling
- Validate inputs before processing
- Handle invalid IDs gracefully
- Catch and display errors clearly
- Allow user to retry or cancel

## Commands for Development

### Using UV (Recommended)
```bash
# Initialize project (if not done)
uv init

# Add dependencies (if any)
uv add <package>

# Run the application
uv run python src/main.py
```

### Using Standard Python
```bash
# Run directly
python src/main.py

# Or with module syntax
python -m src.main
```

## Feature Implementation Checklist

When implementing a feature, ensure:
- [ ] Read the feature spec thoroughly
- [ ] Understand acceptance criteria
- [ ] Implement all functional requirements
- [ ] Follow validation rules
- [ ] Handle all edge cases specified
- [ ] Match UI examples in spec
- [ ] Update timestamps correctly
- [ ] Provide clear user feedback
- [ ] Test all scenarios listed in spec

## Hackathon Rules Reminder

**IMPORTANT**:
- ✅ Writing specifications
- ✅ Asking Claude Code to generate implementation
- ✅ Refining specs and regenerating code
- ❌ Manually writing Python code
- ❌ Direct code edits without spec updates

## Common Commands

### Generate Initial Implementation
```
Claude, generate the complete Python implementation based on all specs in /specs
```

### Implement Specific Feature
```
Claude, implement @specs/features/add-task.md
```

### Fix Issues by Refining Spec
```
1. Update the spec: @specs/features/add-task.md
2. Claude, regenerate add-task implementation from updated spec
```

### Test Application
```
Claude, create a test script to verify all features work according to specs
```

## Success Criteria

The implementation is complete when:
1. All 5 basic features work as specified
2. All validation rules are enforced
3. All edge cases are handled
4. UI matches spec examples
5. Code follows Python best practices
6. User can accomplish all user stories
7. No crashes or unhandled errors

## Next Steps

After Phase I completion:
- **Phase II**: Refactor into web app (Next.js + FastAPI)
- **Phase III**: Add AI chatbot (OpenAI ChatKit + MCP)
- **Phase IV**: Deploy on Kubernetes (Minikube)
- **Phase V**: Cloud deployment (DigitalOcean + Kafka + Dapr)

## Questions or Issues?

If you encounter issues:
1. Check the relevant spec for clarity
2. Verify code matches spec requirements
3. Refine spec if requirements were unclear
4. Regenerate code from refined spec
5. Document any spec improvements made

---

Remember: **Specifications drive development, not code!**
