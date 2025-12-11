# Feature: Mark Task Complete/Incomplete

## User Story
As a user, I want to mark tasks as complete or incomplete so I can track my progress and see what still needs to be done.

## Priority
**High** - Core feature for task management

## Acceptance Criteria

### Functional Requirements
1. User can toggle task completion status by ID
2. System validates the task ID exists
3. System shows current status before toggling
4. System changes `completed` field to opposite value
5. System updates the `updated_at` timestamp
6. System confirms status change with clear message
7. Status change is immediately reflected in task list
8. Can toggle completed → incomplete and vice versa

### Validation Rules
- **Task ID**:
  - Must be a valid integer
  - Must exist in the task list
- **Status Toggle**:
  - If current status is `False`, change to `True`
  - If current status is `True`, change to `False`

## User Interface

### Mark as Complete
```
=== MARK TASK COMPLETE/INCOMPLETE ===

Enter task ID: 1

Current task:
[1] ○ Buy groceries
    Milk and eggs
Status: Pending

✓ Task marked as complete!
  ID: 1
  Title: Buy groceries
  New Status: Completed

Press Enter to return to main menu...
```

### Mark as Incomplete (Undo Completion)
```
=== MARK TASK COMPLETE/INCOMPLETE ===

Enter task ID: 2

Current task:
[2] ✓ Call mom
    Wish happy birthday
Status: Completed

✓ Task marked as incomplete!
  ID: 2
  Title: Call mom
  New Status: Pending

Press Enter to return to main menu...
```

## Behavior Specification

### Happy Path (Mark as Complete)
1. System displays "Mark Task" interface
2. System prompts for task ID
3. User enters valid task ID
4. System retrieves task from storage
5. System displays current task details and status
6. System checks current `completed` value
7. Current value is `False` (pending)
8. System sets `completed` to `True`
9. System updates `updated_at` timestamp
10. System displays confirmation "Task marked as complete!"
11. System waits for Enter key
12. System returns to main menu

### Happy Path (Mark as Incomplete)
1-6. Same as above
7. Current value is `True` (completed)
8. System sets `completed` to `False`
9. System updates `updated_at` timestamp
10. System displays confirmation "Task marked as incomplete!"
11. System waits for Enter key
12. System returns to main menu

### Edge Cases

#### Invalid Task ID
```
Enter task ID: 999
❌ Error: Task with ID 999 not found.
Press Enter to return to main menu...
```

#### Non-Integer Task ID
```
Enter task ID: abc
❌ Error: Please enter a valid task ID (number).
Press Enter to return to main menu...
```

#### Empty Task List
```
Enter task ID: 1
❌ Error: No tasks available to update.
Press Enter to return to main menu...
```

## Data Structure

### Before Marking Complete (Task is Pending)
```python
{
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk and eggs",
    "completed": False,  # Current status
    "created_at": "2025-12-09T10:30:00",
    "updated_at": "2025-12-09T10:30:00"
}
```

### After Marking Complete
```python
{
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk and eggs",
    "completed": True,  # Status changed
    "created_at": "2025-12-09T10:30:00",  # Unchanged
    "updated_at": "2025-12-09T11:45:00"  # Updated
}
```

### After Marking Incomplete Again (Toggle Back)
```python
{
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk and eggs",
    "completed": False,  # Status toggled back
    "created_at": "2025-12-09T10:30:00",  # Unchanged
    "updated_at": "2025-12-09T12:15:00"  # Updated again
}
```

## Technical Requirements

### Task Lookup
- Search for task by ID in storage
- Return error if task not found
- Display current task details and status

### Toggle Logic
```python
# Simple toggle
task["completed"] = not task["completed"]

# Or explicit:
if task["completed"] == False:
    task["completed"] = True
else:
    task["completed"] = False
```

### Timestamp Update
- Update `updated_at` to current timestamp
- Do NOT modify `created_at`
- Do NOT modify task ID

### Status Display
- **Pending**: Display as "Pending" or "Incomplete"
- **Completed**: Display as "Completed" or "Done"
- Use consistent terminology throughout app

### Error Handling
- Validate task ID exists
- Handle invalid input gracefully
- Provide clear error messages
- Allow user to return to menu safely

## Testing Scenarios

1. **Mark pending task as complete**
   - Input: ID=1 (status=False)
   - Expected: Status becomes True, confirmation shown

2. **Mark completed task as incomplete**
   - Input: ID=2 (status=True)
   - Expected: Status becomes False, confirmation shown

3. **Toggle task multiple times**
   - Input: Mark complete, then incomplete, then complete again
   - Expected: Status toggles correctly each time

4. **Invalid task ID**
   - Input: ID=999 (doesn't exist)
   - Expected: Error message, return to menu

5. **Non-integer task ID**
   - Input: ID="abc"
   - Expected: Error message, return to menu

6. **Empty task list**
   - Input: ID=1 when no tasks exist
   - Expected: Error message about empty list

7. **Verify updated_at changes**
   - Input: Mark task complete
   - Expected: updated_at timestamp is current

## Visual Indicators

### In Task List (View Tasks)
- **Pending**: `○ Task title` (empty circle)
- **Completed**: `✓ Task title` (checkmark)

### In Status Messages
- **Pending**: "Status: Pending" or "Status: Incomplete"
- **Completed**: "Status: Completed" or "Status: Done"

## User Experience Goals
- **Quick Toggle**: Fast way to mark tasks done
- **Flexibility**: Can undo completion if needed
- **Clear Feedback**: Always know current and new status
- **Visual Consistency**: Status indicators match throughout app
- **Speed**: Mark complete in under 3 seconds

## Alternative UI Approaches

### Option 1: Automatic Toggle (Current Spec)
- User enters ID, system automatically toggles
- Simple, but less explicit

### Option 2: Explicit Choice (Alternative)
```
Current status: Pending
1. Mark as Complete
2. Mark as Incomplete
3. Cancel
Enter choice:
```
- More explicit, but slower
- Use automatic toggle for Phase I (simpler)

## Success Metrics
- Task completion status is correctly toggled
- `updated_at` timestamp is current
- Updated status appears in "View All Tasks"
- User receives clear confirmation
- Validation prevents invalid operations
- Can toggle status multiple times without issues
