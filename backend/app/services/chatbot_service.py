from groq import Groq
from sqlmodel import Session
from typing import List, Dict, Any, Optional
import json
import uuid
from ..config import settings
from ..models.user import User
from ..models.task import TaskCreate, TaskUpdate
from .task_service import TaskService


class ChatbotService:
    """Service for handling AI chatbot interactions using Groq."""

    @staticmethod
    def _get_groq_client() -> Groq:
        """Initialize and return Groq client."""
        return Groq(api_key=settings.GROQ_API_KEY)

    @staticmethod
    def _get_system_prompt() -> str:
        """Get the system prompt for the AI assistant."""
        return """You are a helpful task management assistant. Help users manage their todo list by creating, viewing, updating, and deleting tasks.

When users ask to perform task operations, use the provided functions. Be concise, friendly, and helpful.

Guidelines:
- For creating tasks, extract the task title from user's message
- When listing tasks, present them in a clear, numbered format
- Confirm actions after they're completed
- Be conversational and supportive"""

    @staticmethod
    def _get_function_definitions() -> List[Dict[str, Any]]:
        """Get function definitions for Groq function calling."""
        return [
            {
                "name": "create_task",
                "description": "Create a new task in the user's todo list",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "The title/name of the task to create"
                        },
                        "description": {
                            "type": "string",
                            "description": "Optional detailed description of the task"
                        }
                    },
                    "required": ["title"]
                }
            },
            {
                "name": "list_tasks",
                "description": "Get all tasks from the user's todo list",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filter": {
                            "type": "string",
                            "enum": ["all", "pending", "completed"],
                            "description": "Filter tasks by status (default: all)"
                        }
                    }
                }
            },
            {
                "name": "update_task",
                "description": "Update an existing task's title or description",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "integer",
                            "description": "The ID of the task to update"
                        },
                        "title": {
                            "type": "string",
                            "description": "New title for the task"
                        },
                        "description": {
                            "type": "string",
                            "description": "New description for the task"
                        }
                    },
                    "required": ["task_id"]
                }
            },
            {
                "name": "toggle_task_complete",
                "description": "Mark a task as complete or incomplete",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "integer",
                            "description": "The ID of the task to toggle"
                        }
                    },
                    "required": ["task_id"]
                }
            },
            {
                "name": "delete_task",
                "description": "Delete a task from the todo list",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "integer",
                            "description": "The ID of the task to delete"
                        }
                    },
                    "required": ["task_id"]
                }
            }
        ]

    @staticmethod
    def _execute_function(
        session: Session,
        function_name: str,
        arguments: Dict[str, Any],
        user_id: uuid.UUID
    ) -> Dict[str, Any]:
        """Execute a function call from the AI."""
        try:
            if function_name == "create_task":
                task_data = TaskCreate(
                    title=arguments["title"],
                    description=arguments.get("description"),
                    completed=False
                )
                task = TaskService.create_task(session, task_data, user_id)
                return {
                    "success": True,
                    "task": {
                        "id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "completed": task.completed
                    },
                    "message": f"Created task: '{task.title}'"
                }

            elif function_name == "list_tasks":
                filter_type = arguments.get("filter", "all")
                tasks = TaskService.get_all_tasks(session, user_id)

                # Apply filter
                if filter_type == "pending":
                    tasks = [t for t in tasks if not t.completed]
                elif filter_type == "completed":
                    tasks = [t for t in tasks if t.completed]

                task_list = [
                    {
                        "id": t.id,
                        "title": t.title,
                        "completed": t.completed
                    }
                    for t in tasks
                ]

                return {
                    "success": True,
                    "tasks": task_list,
                    "count": len(task_list),
                    "message": f"Found {len(task_list)} task(s)"
                }

            elif function_name == "update_task":
                task_id = arguments["task_id"]
                task_update = TaskUpdate(
                    title=arguments.get("title"),
                    description=arguments.get("description")
                )
                task = TaskService.update_task(session, task_id, task_update, user_id)

                if not task:
                    return {
                        "success": False,
                        "message": f"Task {task_id} not found"
                    }

                return {
                    "success": True,
                    "task": {
                        "id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "completed": task.completed
                    },
                    "message": f"Updated task: '{task.title}'"
                }

            elif function_name == "toggle_task_complete":
                task_id = arguments["task_id"]
                task = TaskService.toggle_complete(session, task_id, user_id)

                if not task:
                    return {
                        "success": False,
                        "message": f"Task {task_id} not found"
                    }

                status = "completed" if task.completed else "pending"
                return {
                    "success": True,
                    "task": {
                        "id": task.id,
                        "title": task.title,
                        "completed": task.completed
                    },
                    "message": f"Marked '{task.title}' as {status}"
                }

            elif function_name == "delete_task":
                task_id = arguments["task_id"]
                success = TaskService.delete_task(session, task_id, user_id)

                if not success:
                    return {
                        "success": False,
                        "message": f"Task {task_id} not found"
                    }

                return {
                    "success": True,
                    "message": f"Deleted task {task_id}"
                }

            else:
                return {
                    "success": False,
                    "message": f"Unknown function: {function_name}"
                }

        except Exception as e:
            return {
                "success": False,
                "message": f"Error executing {function_name}: {str(e)}"
            }

    @staticmethod
    def process_message(
        session: Session,
        message: str,
        user_id: uuid.UUID,
        current_user: User
    ) -> Dict[str, Any]:
        """
        Process a chat message and return AI response.

        Args:
            session: Database session
            message: User's message text
            user_id: User's UUID
            current_user: Authenticated user object

        Returns:
            Dictionary with 'message' and optional 'actions_performed'
        """
        try:
            client = ChatbotService._get_groq_client()

            # Build messages for the conversation
            messages = [
                {
                    "role": "system",
                    "content": ChatbotService._get_system_prompt()
                },
                {
                    "role": "user",
                    "content": message
                }
            ]

            # Call Groq API with function calling
            response = client.chat.completions.create(
                model=settings.GROQ_MODEL,
                messages=messages,
                tools=[
                    {
                        "type": "function",
                        "function": func
                    }
                    for func in ChatbotService._get_function_definitions()
                ],
                tool_choice="auto",
                max_tokens=settings.GROQ_MAX_TOKENS,
                temperature=settings.GROQ_TEMPERATURE
            )

            response_message = response.choices[0].message
            actions_performed = []

            # Check if the model wants to call functions
            if response_message.tool_calls:
                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    # Execute the function
                    result = ChatbotService._execute_function(
                        session,
                        function_name,
                        function_args,
                        user_id
                    )

                    if result.get("success"):
                        actions_performed.append(result["message"])

                    # Add function result to messages for follow-up
                    messages.append({
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [tool_call.model_dump()]
                    })
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result)
                    })

                # Get final response after function calls
                final_response = client.chat.completions.create(
                    model=settings.GROQ_MODEL,
                    messages=messages,
                    max_tokens=settings.GROQ_MAX_TOKENS,
                    temperature=settings.GROQ_TEMPERATURE
                )

                final_message = final_response.choices[0].message.content
            else:
                # No function calls, just return the response
                final_message = response_message.content

            return {
                "message": final_message or "I'm ready to help with your tasks!",
                "actions_performed": actions_performed if actions_performed else None
            }

        except Exception as e:
            print(f"Chatbot error: {e}")
            return {
                "message": "Sorry, I encountered an error. Please try again.",
                "actions_performed": None
            }
