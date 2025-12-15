import google.generativeai as genai
from sqlmodel import Session
from typing import Dict, Any
import json
import uuid
from datetime import datetime, date
from ..config import settings
from ..models.user import User
from ..models.task import TaskCreate, TaskUpdate
from .task_service import TaskService


class ChatbotService:
    """Service for handling AI chatbot interactions using Google Gemini (headless interpreter mode)."""

    @staticmethod
    def _get_headless_prompt() -> str:
        """Get the headless command interpreter system prompt."""
        current_date = datetime.now().date()
        current_year = current_date.year

        return f"""Role:
You are a headless command interpreter for a Todo application.
Current date: {current_date.isoformat()} (format: YYYY-MM-DD, example: 2025-12-13)
Current year: {current_year}

Rules:
- Interpret input literally; do NOT infer, correct, or enrich.
- Create exactly ONE task per request; ignore additional tasks.
- Preserve text exactly as written (URLs, numbers, typos, casing).
- Extract due_date if a specific calendar date is given:
    * Formats accepted (in precedence order):
      1. YYYY-MM-DD (2025-12-20)
      2. Month DD YYYY (Dec 20 2025, December 20 2025 - case-insensitive)
      3. DD/MM/YYYY (20/12/2025)
      4. MM/DD/YYYY (12/20/2025)
    * If year is missing, assume current year ({current_year})
    * Normalize to YYYY-MM-DD in output
    * Ambiguous dates (01/02/2025) are interpreted as DD/MM/YYYY
    * Reject relative dates: today, tomorrow, next week, Monday, etc.
- Extract tags ONLY if prefixed with # followed by alphanumeric characters.
    * Tags must be space-separated: "#tag1 #tag2" (valid)
    * Ignore "#" alone or "#tag1#tag2" (no space)
    * Case-sensitive: #Invoice and #invoice are different tags
    * Remove # in output
- If text is empty after processing, return {{"error":"invalid_request"}}.
- If no valid date found, set due_date to null.
- If no valid tags found, set tags to [].
- Return ONLY a JSON object; no prose, no markdown, no explanations.

Supported Actions:
1. create_task - Create a new task
   Input examples: "add task to buy milk", "create task: finish report #work 2025-12-20"

2. list_tasks - Show all tasks or filter tasks
   Input examples: "show my tasks", "list all tasks", "what do I have to do", "show incomplete tasks"

3. update_task - Update task fields
   Input examples: "update task 5 title to 'New Title'", "change description of task 3 to 'Updated'"

4. toggle_complete - Mark task complete or incomplete
   Input examples: "mark task 5 as done", "complete task 3", "mark task 2 as incomplete"

5. delete_task - Delete a task
   Input examples: "delete task 5", "remove task 3"

Output Schemas:

1. CREATE_TASK:
{{
  "action": "create_task",
  "data": {{
    "text": "string",
    "due_date": "YYYY-MM-DD or null",
    "tags": ["array of strings"]
  }}
}}

2. LIST_TASKS:
{{
  "action": "list_tasks",
  "data": {{
    "filter": "all" or "completed" or "incomplete"
  }}
}}

3. UPDATE_TASK:
{{
  "action": "update_task",
  "data": {{
    "task_id": number,
    "updates": {{
      "title": "string (optional)",
      "description": "string (optional)",
      "due_date": "YYYY-MM-DD or null (optional)",
      "tags": ["array of strings (optional)"]
    }}
  }}
}}

4. TOGGLE_COMPLETE:
{{
  "action": "toggle_complete",
  "data": {{
    "task_id": number
  }}
}}

5. DELETE_TASK:
{{
  "action": "delete_task",
  "data": {{
    "task_id": number
  }}
}}

Error Response:
{{
  "error": "invalid_request"
}}"""

    @staticmethod
    def _get_gemini_model():
        """Initialize and return Gemini model for headless mode."""
        genai.configure(api_key=settings.GEMINI_API_KEY)

        generation_config = {
            "temperature": 0.1,  # Low temperature for consistent parsing
            "max_output_tokens": 500,
        }

        model = genai.GenerativeModel(
            model_name=settings.GEMINI_MODEL,
            generation_config=generation_config,
            system_instruction=ChatbotService._get_headless_prompt()
        )

        return model

    @staticmethod
    def _parse_json_response(response_text: str) -> Dict[str, Any]:
        """Parse JSON from Gemini response, handling potential markdown wrapping."""
        try:
            # Remove markdown code blocks if present
            text = response_text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]

            text = text.strip()
            return json.loads(text)
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}, Response: {response_text}")
            return {"error": "invalid_request"}

    @staticmethod
    def _execute_create_task(
        session: Session,
        data: Dict[str, Any],
        user_id: uuid.UUID
    ) -> Dict[str, Any]:
        """Execute create_task action."""
        try:
            # Parse due_date from string to date object
            due_date = None
            if data.get("due_date"):
                try:
                    due_date = datetime.strptime(data["due_date"], "%Y-%m-%d").date()
                except ValueError:
                    due_date = None

            # Create task
            task_data = TaskCreate(
                title=data["text"],
                description=None,
                due_date=due_date,
                tags=data.get("tags", [])
            )

            task = TaskService.create_task(session, task_data, user_id)

            return {
                "success": True,
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "due_date": task.due_date.isoformat() if task.due_date else None,
                    "tags": task.tags,
                    "completed": task.completed
                },
                "message": f"✓ Created task ID {task.id}"
            }

        except Exception as e:
            print(f"Error creating task: {e}")
            return {
                "success": False,
                "message": f"Error: {str(e)}"
            }

    @staticmethod
    def _execute_list_tasks(
        session: Session,
        data: Dict[str, Any],
        user_id: uuid.UUID
    ) -> Dict[str, Any]:
        """Execute list_tasks action."""
        try:
            # Get all tasks
            all_tasks = TaskService.get_all_tasks(session, user_id)

            # Apply filter
            filter_type = data.get("filter", "all")
            if filter_type == "completed":
                tasks = [t for t in all_tasks if t.completed]
            elif filter_type == "incomplete":
                tasks = [t for t in all_tasks if not t.completed]
            else:
                tasks = all_tasks

            # Format tasks for response
            if not tasks:
                message = "You have no tasks."
                if filter_type == "completed":
                    message = "You have no completed tasks."
                elif filter_type == "incomplete":
                    message = "You have no incomplete tasks."
                return {
                    "success": True,
                    "message": message,
                    "tasks": []
                }

            # Build formatted message
            lines = []
            for task in tasks:
                status = "✓" if task.completed else "○"
                due_str = f" (due: {task.due_date.isoformat()})" if task.due_date else ""
                tags_str = f" {' '.join(['#' + tag for tag in task.tags])}" if task.tags else ""
                lines.append(f"{status} [{task.id}] {task.title}{due_str}{tags_str}")

            message = f"Found {len(tasks)} task(s):\n" + "\n".join(lines)

            return {
                "success": True,
                "message": message,
                "tasks": [{"id": t.id, "title": t.title, "completed": t.completed} for t in tasks]
            }

        except Exception as e:
            print(f"Error listing tasks: {e}")
            return {
                "success": False,
                "message": f"Error: {str(e)}"
            }

    @staticmethod
    def _execute_update_task(
        session: Session,
        data: Dict[str, Any],
        user_id: uuid.UUID
    ) -> Dict[str, Any]:
        """Execute update_task action."""
        try:
            task_id = data.get("task_id")
            updates = data.get("updates", {})

            if not task_id:
                return {
                    "success": False,
                    "message": "Task ID is required"
                }

            # Parse due_date if present
            if "due_date" in updates and updates["due_date"]:
                try:
                    updates["due_date"] = datetime.strptime(updates["due_date"], "%Y-%m-%d").date()
                except ValueError:
                    updates["due_date"] = None

            # Create TaskUpdate object
            task_update = TaskUpdate(**updates)

            # Update task
            task = TaskService.update_task(session, task_id, task_update, user_id)

            if not task:
                return {
                    "success": False,
                    "message": f"Task {task_id} not found"
                }

            return {
                "success": True,
                "message": f"✓ Updated task {task_id}",
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "completed": task.completed
                }
            }

        except Exception as e:
            print(f"Error updating task: {e}")
            return {
                "success": False,
                "message": f"Error: {str(e)}"
            }

    @staticmethod
    def _execute_toggle_complete(
        session: Session,
        data: Dict[str, Any],
        user_id: uuid.UUID
    ) -> Dict[str, Any]:
        """Execute toggle_complete action."""
        try:
            task_id = data.get("task_id")

            if not task_id:
                return {
                    "success": False,
                    "message": "Task ID is required"
                }

            # Toggle completion
            task = TaskService.toggle_complete(session, task_id, user_id)

            if not task:
                return {
                    "success": False,
                    "message": f"Task {task_id} not found"
                }

            status = "completed" if task.completed else "incomplete"
            return {
                "success": True,
                "message": f"✓ Marked task {task_id} as {status}",
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "completed": task.completed
                }
            }

        except Exception as e:
            print(f"Error toggling task: {e}")
            return {
                "success": False,
                "message": f"Error: {str(e)}"
            }

    @staticmethod
    def _execute_delete_task(
        session: Session,
        data: Dict[str, Any],
        user_id: uuid.UUID
    ) -> Dict[str, Any]:
        """Execute delete_task action."""
        try:
            task_id = data.get("task_id")

            if not task_id:
                return {
                    "success": False,
                    "message": "Task ID is required"
                }

            # Delete task
            success = TaskService.delete_task(session, task_id, user_id)

            if not success:
                return {
                    "success": False,
                    "message": f"Task {task_id} not found"
                }

            return {
                "success": True,
                "message": f"✓ Deleted task {task_id}"
            }

        except Exception as e:
            print(f"Error deleting task: {e}")
            return {
                "success": False,
                "message": f"Error: {str(e)}"
            }

    @staticmethod
    def process_message(
        session: Session,
        message: str,
        user_id: uuid.UUID,
        current_user: User
    ) -> Dict[str, Any]:
        """
        Process a chat message using headless interpreter mode.

        Args:
            session: Database session
            message: User's message text
            user_id: User's UUID
            current_user: Authenticated user object

        Returns:
            Dictionary with 'message' and optional 'actions_performed'
        """
        try:
            model = ChatbotService._get_gemini_model()

            # Send message to Gemini
            response = model.generate_content(message)

            # Parse JSON response
            parsed = ChatbotService._parse_json_response(response.text)

            # Check for error
            if "error" in parsed:
                return {
                    "message": "Invalid request. Please provide a task to create.",
                    "actions_performed": None
                }

            # Execute action
            action = parsed.get("action")
            data = parsed.get("data", {})

            # Route to appropriate action handler
            if action == "create_task":
                result = ChatbotService._execute_create_task(session, data, user_id)
            elif action == "list_tasks":
                result = ChatbotService._execute_list_tasks(session, data, user_id)
            elif action == "update_task":
                result = ChatbotService._execute_update_task(session, data, user_id)
            elif action == "toggle_complete":
                result = ChatbotService._execute_toggle_complete(session, data, user_id)
            elif action == "delete_task":
                result = ChatbotService._execute_delete_task(session, data, user_id)
            else:
                return {
                    "message": f"Unknown action '{action}'.",
                    "actions_performed": None
                }

            # Return result
            if result.get("success"):
                return {
                    "message": result["message"],
                    "actions_performed": [result["message"]]
                }
            else:
                return {
                    "message": result["message"],
                    "actions_performed": None
                }

        except Exception as e:
            print(f"Chatbot error: {e}")
            return {
                "message": "Sorry, I encountered an error. Please try again.",
                "actions_performed": None
            }
