# Feature: Delete Task

## User Story
As a user, I want to delete tasks that are no longer needed so I can keep my task list clean and relevant.

## Priority
**Medium** - Important for task management and list hygiene

## Acceptance Criteria

### Functional Requirements
1. User can select a task by ID to delete
2. System validates the task ID exists
3. System shows task details before deletion
4. System asks for confirmation before deleting
5. System permanently removes task from storage
6. System confirms deletion with success message
7. Deleted task no longer appears in task list
8. User can cancel deletion before confirming

### Validation Rules
- **Task ID**:
  - Must be a valid integer
  - Must exist in the task list
- **Confirmation**:
  - User must explicitly confirm deletion
  - Typing "yes" or "y" confirms
  - Any other input cancels

### Safety Features
- **Confirmation Required**: Prevent accidental deletions
- **Show Before Delete**: Display task details before confirming
- **Cancel Option**: Easy to back out of deletion
- **Clear Feedback**: Confirm when task is deleted

## User Interface

### Happy Path
```
=== DELETE TASK ===

Enter task ID to delete: 1

Task to be deleted:
[1] ○ Buy groceries
    Milk and eggs

⚠ Are you sure you want to delete this task? This cannot be undone.
Type 'yes' or 'y' to confirm, or anything else to cancel: yes

✓ Task deleted successfully!
  ID: 1
  Title: Buy groceries

Press Enter to return to main menu...
```

### Cancelled Deletion
```
Enter task ID to delete: 2

Task to be deleted:
[2] ✓ Call mom
    Wish happy birthday

⚠ Are you sure you want to delete this task? This cannot be undone.
Type 'yes' or 'y' to confirm, or anything else to cancel: no

Deletion cancelled. Task was not deleted.

Press Enter to return to main menu...
```

## Behavior Specification

### Happy Path
1. System displays "Delete Task" interface
2. System prompts for task ID
3. User enters valid task ID
4. System retrieves task from storage
5. System displays task details
6. System displays warning message
7. System prompts for confirmation (yes/y to confirm)
8. User types "yes" or "y"
9. System removes task from storage
10. System displays confirmation with deleted task details
11. System waits for Enter key
12. System returns to main menu

### Cancelled Deletion
1-7. Same as happy path
8. User types anything other than "yes" or "y"
9. System displays cancellation message
10. Task remains in storage (not deleted)
11. System waits for Enter key
12. System returns to main menu

### Edge Cases

#### Invalid Task ID
```
Enter task ID to delete: 999
❌ Error: Task with ID 999 not found.
Press Enter to return to main menu...
```

#### Non-Integer Task ID
```
Enter task ID to delete: abc
❌ Error: Please enter a valid task ID (number).
Press Enter to return to main menu...
```

#### Case-Insensitive Confirmation
```
Type 'yes' or 'y' to confirm: YES
✓ Task deleted successfully!
```

```
Type 'yes' or 'y' to confirm: Y
✓ Task deleted successfully!
```

#### Empty Task List
```
Enter task ID to delete: 1
❌ Error: No tasks available to delete.
Press Enter to return to main menu...
```

## Data Structure

### Before Deletion
```python
tasks = [
    {"id": 1, "title": "Buy groceries", "completed": False, ...},
    {"id": 2, "title": "Call mom", "completed": True, ...},
    {"id": 3, "title": "Review PR", "completed": False, ...}
]
```

### After Deleting Task 2
```python
tasks = [
    {"id": 1, "title": "Buy groceries", "completed": False, ...},
    {"id": 3, "title": "Review PR", "completed": False, ...}
]
# Task 2 is permanently removed
# Note: ID 2 is never reused for new tasks
```

## Technical Requirements

### Task Lookup
- Search for task by ID in storage
- Return error if task not found
- Display full task details before deletion

### Deletion Logic
- Remove task from in-memory storage (list/dict)
- Ensure task is completely removed (not just marked deleted)
- Do NOT reuse deleted task IDs for new tasks

### Confirmation Logic
- Accept "yes", "y", "YES", "Y", "Yes" as confirmation
- Treat any other input as cancellation
- Case-insensitive comparison

### Error Handling
- Validate task ID exists before showing confirmation
- Handle invalid input gracefully
- Provide clear error messages
- Allow user to return to menu safely

## Testing Scenarios

1. **Delete task successfully**
   - Input: ID=1, confirm="yes"
   - Expected: Task removed, confirmation shown

2. **Cancel deletion**
   - Input: ID=1, confirm="no"
   - Expected: Task NOT removed, cancellation message shown

3. **Delete with case-insensitive confirmation**
   - Input: ID=1, confirm="YES"
   - Expected: Task removed (case doesn't matter)

4. **Invalid task ID**
   - Input: ID=999 (doesn't exist)
   - Expected: Error message, return to menu

5. **Non-integer task ID**
   - Input: ID="abc"
   - Expected: Error message, return to menu

6. **Delete completed task**
   - Input: ID of completed task, confirm="yes"
   - Expected: Task removed (completion status doesn't matter)

7. **Delete from empty list**
   - Input: ID=1 when no tasks exist
   - Expected: Error message about empty list

8. **Multiple deletions**
   - Input: Delete task 1, then task 3
   - Expected: Both tasks removed successfully

## User Experience Goals
- **Safety**: Confirmation prevents accidental deletions
- **Clarity**: Show what will be deleted before confirming
- **Transparency**: Clear feedback about what happened
- **Forgiveness**: Easy to cancel deletion
- **Speed**: Quick deletion for intentional actions

## Important Notes

### ID Management
- Deleted task IDs are NEVER reused
- If task 2 is deleted, the next new task gets ID 4 (not 2)
- This prevents confusion and maintains data integrity

### Irreversible Action
- Deletion is permanent (in Phase I)
- No "undo" feature in console version
- This is why confirmation is required

## Success Metrics
- Task is successfully removed from storage
- Deleted task does NOT appear in "View All Tasks"
- User receives clear confirmation
- Accidental deletions are prevented by confirmation
- Validation prevents invalid deletions
