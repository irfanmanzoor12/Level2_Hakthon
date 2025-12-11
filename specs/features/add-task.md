# Feature: Add Task

## User Story
As a user, I want to add new tasks to my todo list so I can track what I need to do.

## Priority
**High** - Core feature required for basic functionality

## Acceptance Criteria

### Functional Requirements
1. User can enter a task title (required)
2. User can optionally enter a description
3. System assigns a unique ID to each task automatically
4. System records creation timestamp
5. Task is marked as incomplete by default
6. System confirms task creation with success message
7. Task is immediately available in the task list

### Validation Rules
- **Title**:
  - Required field (cannot be empty)
  - Minimum length: 1 character
  - Maximum length: 200 characters
  - Must contain at least one non-whitespace character
- **Description**:
  - Optional field
  - Maximum length: 1000 characters
  - Can be empty or omitted

### User Interface
```
=== ADD NEW TASK ===

Enter task title: [user input]
Enter task description (press Enter to skip): [user input]

✓ Task added successfully!
  ID: 1
  Title: Buy groceries
  Status: Pending
```

## Behavior Specification

### Happy Path
1. System displays "Add Task" interface
2. System prompts for task title
3. User enters valid title
4. System prompts for description (optional)
5. User enters description or presses Enter to skip
6. System creates task with:
   - Auto-incremented ID
   - User-provided title
   - User-provided description (or empty string)
   - Status: `completed = False`
   - Current timestamp for `created_at`
   - Current timestamp for `updated_at`
7. System adds task to in-memory storage
8. System displays confirmation with task details
9. System returns to main menu

### Edge Cases

#### Empty Title
```
Enter task title:
❌ Error: Title cannot be empty. Please try again.
Enter task title: [re-prompt]
```

#### Title Too Long (>200 characters)
```
Enter task title: [201+ characters]
❌ Error: Title is too long (max 200 characters). Please enter a shorter title.
Enter task title: [re-prompt]
```

#### Whitespace-Only Title
```
Enter task title: "   "
❌ Error: Title cannot be only whitespace. Please enter a valid title.
Enter task title: [re-prompt]
```

#### Description Too Long (>1000 characters)
```
Enter task description: [1001+ characters]
⚠ Warning: Description truncated to 1000 characters.
✓ Task added successfully! [continues normally]
```

## Data Structure

### Task Object
```python
{
    "id": 1,                          # Auto-increment integer
    "title": "Buy groceries",         # User input (validated)
    "description": "Milk, eggs...",   # User input (optional)
    "completed": False,                # Default: False
    "created_at": "2025-12-09T10:30:00",  # ISO timestamp
    "updated_at": "2025-12-09T10:30:00"   # ISO timestamp
}
```

## Technical Requirements

### ID Generation
- Use auto-incrementing integer IDs
- Start from 1
- Track highest ID used (even if tasks are deleted)
- Never reuse deleted task IDs

### Storage
- Add task to in-memory list/dict immediately after creation
- Ensure task persists for duration of program execution

### Error Handling
- Validate all inputs before creating task
- Provide clear error messages
- Allow user to retry on validation failure
- Handle unexpected errors gracefully

## Testing Scenarios

1. **Valid task with title and description**
   - Input: title="Buy groceries", description="Milk and eggs"
   - Expected: Task created with ID 1, confirmed to user

2. **Valid task with title only**
   - Input: title="Call mom", description=""
   - Expected: Task created with empty description

3. **Empty title**
   - Input: title=""
   - Expected: Error message, re-prompt for title

4. **Very long title (201 characters)**
   - Input: title=[201 chars]
   - Expected: Error message, re-prompt

5. **Very long description (1001 characters)**
   - Input: description=[1001 chars]
   - Expected: Warning, description truncated, task created

6. **Special characters in title**
   - Input: title="Review PR #123 & merge"
   - Expected: Task created successfully with special characters preserved

## User Experience Goals
- **Speed**: User can add a task in under 5 seconds
- **Clarity**: Clear prompts and confirmation messages
- **Forgiveness**: Easy to retry on validation errors
- **Feedback**: Immediate confirmation with task details

## Success Metrics
- Task is successfully added to storage
- Task appears in "View All Tasks" list
- User receives clear confirmation message
- Validation prevents invalid data
