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

Supported Actions (Phase III default: create_task):
- create_task (implemented in Phase III)
- list_tasks (reserved for Phase IV)
- update_task (reserved for Phase IV)
- toggle_complete (reserved for Phase IV)
- delete_task (reserved for Phase IV)

Output Schema (Phase III):

{{
  "action": "create_task",
  "data": {{
    "text": "string",
    "due_date": "YYYY-MM-DD or null",
    "tags": ["array of strings"]
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

            if action == "create_task":
                result = ChatbotService._execute_create_task(session, data, user_id)

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
            else:
                return {
                    "message": f"Action '{action}' not yet implemented.",
                    "actions_performed": None
                }

        except Exception as e:
            print(f"Chatbot error: {e}")
            return {
                "message": "Sorry, I encountered an error. Please try again.",
                "actions_performed": None
            }
