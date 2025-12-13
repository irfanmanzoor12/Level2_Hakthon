import google.generativeai as genai
from sqlmodel import Session
from typing import List, Dict, Any, Optional
import json
import uuid
from ..config import settings
from ..models.user import User
from ..models.task import TaskCreate, TaskUpdate
from .task_service import TaskService


class ChatbotService:
    """Service for handling AI chatbot interactions using Google Gemini."""

    @staticmethod
    def _get_gemini_model():
        """Initialize and return Gemini model."""
        genai.configure(api_key=settings.GEMINI_API_KEY)

        # Define function declarations for Gemini
        tools = [
            {
                "function_declarations": [
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
            }
        ]

        generation_config = {
            "temperature": settings.GEMINI_TEMPERATURE,
            "max_output_tokens": settings.GEMINI_MAX_TOKENS,
        }

        model = genai.GenerativeModel(
            model_name=settings.GEMINI_MODEL,
            tools=tools,
            generation_config=generation_config,
            system_instruction="""You are a helpful task management assistant. Help users manage their todo list by creating, viewing, updating, and deleting tasks.

When users ask to perform task operations, use the provided functions. Be concise, friendly, and helpful.

Guidelines:
- For creating tasks, extract the task title from user's message
- When listing tasks, ALWAYS show the actual task ID (not numbered 1, 2, 3). Format: "Task ID X: title"
- Users must use the actual task ID (not position number) to update/delete/complete tasks
- Confirm actions after they're completed
- Be conversational and supportive"""
        )

        return model

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
            model = ChatbotService._get_gemini_model()
            chat = model.start_chat(history=[])

            # Send message to Gemini
            response = chat.send_message(message)

            actions_performed = []

            # Check if the model wants to call functions
            if response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'function_call') and part.function_call:
                        function_call = part.function_call
                        function_name = function_call.name
                        function_args = dict(function_call.args)

                        # Execute the function
                        result = ChatbotService._execute_function(
                            session,
                            function_name,
                            function_args,
                            user_id
                        )

                        if result.get("success"):
                            actions_performed.append(result["message"])

                        # Send function result back to Gemini
                        function_response = {
                            "function_call": {
                                "name": function_name,
                            },
                            "function_response": {
                                "name": function_name,
                                "response": result
                            }
                        }

                        # Get final response after function execution
                        final_response = chat.send_message(
                            genai.protos.Content(
                                parts=[genai.protos.Part(
                                    function_response=genai.protos.FunctionResponse(
                                        name=function_name,
                                        response={"result": result}
                                    )
                                )]
                            )
                        )

                        final_message = final_response.text
                        break
                else:
                    # No function calls, just return the response
                    final_message = response.text
            else:
                final_message = response.text

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
