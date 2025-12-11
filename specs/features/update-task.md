# Feature: Update Task

## User Story
As a user, I want to update the title or description of an existing task so I can correct mistakes or add more detail.

## Priority
**Medium** - Important for task management but not critical for MVP

## Acceptance Criteria

### Functional Requirements
1. User can select a task by ID to update
2. User can update the task title
3. User can update the task description
4. User can choose to update title only, description only, or both
5. System validates the task ID exists
6. System validates new title/description (same rules as Add Task)
7. System updates the `updated_at` timestamp
8. System confirms update with success message
9. Updated task is immediately reflected in task list

### Validation Rules
- **Task ID**:
  - Must be a valid integer
  - Must exist in the task list
- **Title** (if updating):
  - Cannot be empty
  - 1-200 characters
  - Must contain at least one non-whitespace character
- **Description** (if updating):
  - Optional (can be empty)
  - Maximum 1000 characters

## User Interface

### Happy Path
```
=== UPDATE TASK ===

Enter task ID to update: 1

Current task:
[1] ○ Buy groceries
    Milk and eggs

What would you like to update?
1. Title only
2. Description only
3. Both title and description
4. Cancel

Enter your choice (1-4): 1

Current title: Buy groceries
Enter new title: Buy groceries and fruits

✓ Task updated successfully!
  ID: 1
  New Title: Buy groceries and fruits
  Description: Milk and eggs
  Status: Pending
```

### Update Both Fields
```
Enter your choice (1-4): 3

Current title: Buy groceries
Enter new title (or press Enter to keep current): Buy groceries and snacks

Current description: Milk and eggs
Enter new description (or press Enter to keep current): Milk, eggs, chips, cookies

✓ Task updated successfully!
  ID: 1
  Title: Buy groceries and snacks
  Description: Milk, eggs, chips, cookies
```

## Behavior Specification

### Happy Path (Update Title)
1. System displays "Update Task" interface
2. System prompts for task ID
3. User enters valid task ID
4. System retrieves and displays current task details
5. System presents update options menu
6. User selects "Title only"
7. System displays current title
8. System prompts for new title
9. User enters valid new title
10. System validates new title
11. System updates task title
12. System updates `updated_at` timestamp
13. System displays confirmation
14. System returns to main menu

### Happy Path (Update Description)
1-6. Same as above
7. User selects "Description only"
8. System displays current description
9. System prompts for new description
10. User enters new description (or empty to clear)
11. System validates new description
12. System updates task description
13. System updates `updated_at` timestamp
14. System displays confirmation
15. System returns to main menu

### Happy Path (Update Both)
1-6. Same as above
7. User selects "Both"
8. System prompts for new title (with option to keep current)
9. User enters new title or presses Enter
10. System prompts for new description (with option to keep current)
11. User enters new description or presses Enter
12. System validates inputs
13. System updates task with new values
14. System updates `updated_at` timestamp
15. System displays confirmation
16. System returns to main menu

### Edge Cases

#### Invalid Task ID
```
Enter task ID to update: 999
❌ Error: Task with ID 999 not found.
Press Enter to return to main menu...
```

#### Non-Integer Task ID
```
Enter task ID to update: abc
❌ Error: Please enter a valid task ID (number).
Press Enter to return to main menu...
```

#### Empty New Title
```
Enter new title:
❌ Error: Title cannot be empty. Please try again.
Enter new title: [re-prompt]
```

#### Title Too Long
```
Enter new title: [201+ characters]
❌ Error: Title is too long (max 200 characters).
Enter new title: [re-prompt]
```

#### Keep Current Value (Press Enter)
```
Current title: Buy groceries
Enter new title (or press Enter to keep current): [Enter]
→ Title unchanged

Current description: Milk and eggs
Enter new description (or press Enter to keep current): [Enter]
→ Description unchanged
```

#### Cancel Operation
```
Enter your choice (1-4): 4
Operation cancelled. Returning to main menu.
```

## Data Structure

### Before Update
```python
{
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk and eggs",
    "completed": False,
    "created_at": "2025-12-09T10:30:00",
    "updated_at": "2025-12-09T10:30:00"
}
```

### After Update (Title)
```python
{
    "id": 1,
    "title": "Buy groceries and fruits",  # Changed
    "description": "Milk and eggs",
    "completed": False,
    "created_at": "2025-12-09T10:30:00",
    "updated_at": "2025-12-09T11:45:00"  # Updated timestamp
}
```

## Technical Requirements

### Task Lookup
- Search for task by ID in storage
- Return error if task not found
- Display current values before prompting for new ones

### Update Logic
- Only update fields that user chooses to modify
- If user presses Enter without input, keep current value
- Update `updated_at` timestamp on any modification
- Do NOT modify `created_at` timestamp
- Do NOT modify task ID

### Error Handling
- Validate task ID exists before showing update options
- Validate all new inputs with same rules as Add Task
- Handle unexpected input gracefully
- Allow user to cancel operation

## Testing Scenarios

1. **Update task title successfully**
   - Input: ID=1, new title="Buy groceries and fruits"
   - Expected: Title updated, timestamp updated, confirmation shown

2. **Update task description successfully**
   - Input: ID=1, new description="Updated description"
   - Expected: Description updated, timestamp updated

3. **Update both title and description**
   - Input: ID=1, both fields updated
   - Expected: Both fields updated, timestamp updated

4. **Keep current values (press Enter)**
   - Input: Press Enter for both fields
   - Expected: No changes, but timestamp still updated

5. **Invalid task ID**
   - Input: ID=999 (doesn't exist)
   - Expected: Error message, return to menu

6. **Cancel operation**
   - Input: Select cancel option
   - Expected: No changes, return to menu

7. **Empty new title**
   - Input: New title=""
   - Expected: Error, re-prompt

8. **Update task that's already completed**
   - Input: ID of completed task
   - Expected: Update allowed, completion status unchanged

## User Experience Goals
- **Flexibility**: Update only what needs changing
- **Safety**: Show current values before overwriting
- **Clarity**: Clear options and confirmation
- **Efficiency**: Quick updates without unnecessary steps
- **Forgiveness**: Easy to cancel or keep current values

## Success Metrics
- Task is successfully updated in storage
- Updated task appears correctly in "View All Tasks"
- `updated_at` timestamp is current
- User receives clear confirmation
- Validation prevents invalid data
