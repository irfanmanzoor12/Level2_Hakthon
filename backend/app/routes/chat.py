from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlmodel import Session
from typing import Annotated
import uuid
from ..database import get_session
from ..models.user import User
from ..models.chat import ChatMessage, ChatResponse
from ..middleware.auth import get_current_user
from ..services.chatbot_service import ChatbotService


router = APIRouter(prefix="/api/{user_id}/chat", tags=["Chat"])


def verify_user_access(user_id: uuid.UUID, current_user: User):
    """Verify that the user_id in the URL matches the authenticated user."""
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own chat"
        )


@router.post("/message", response_model=ChatResponse, status_code=status.HTTP_200_OK)
def send_chat_message(
    user_id: Annotated[uuid.UUID, Path()],
    message: ChatMessage,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)]
):
    """
    Send a message to the AI chatbot and get a response.

    The chatbot can help manage tasks through natural language:
    - Create tasks: "Add a task to buy groceries"
    - List tasks: "Show me all my tasks"
    - Update tasks: "Change task 3 to 'Buy milk'"
    - Complete tasks: "Mark task 5 as done"
    - Delete tasks: "Delete task 2"
    """
    verify_user_access(user_id, current_user)

    try:
        response = ChatbotService.process_message(
            session=session,
            message=message.text,
            user_id=user_id,
            current_user=current_user
        )

        return ChatResponse(
            message=response["message"],
            actions_performed=response.get("actions_performed")
        )

    except Exception as e:
        print(f"Chat endpoint error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process chat message"
        )
