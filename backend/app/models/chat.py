from pydantic import BaseModel, Field
from typing import Optional, List


class ChatMessage(BaseModel):
    """Chat message request model."""
    text: str = Field(..., min_length=1, max_length=1000, description="User message text")


class ChatResponse(BaseModel):
    """Chat message response model."""
    message: str = Field(..., description="AI assistant response")
    actions_performed: Optional[List[str]] = Field(
        default=None,
        description="List of actions performed (e.g., 'Created task: Buy groceries')"
    )
