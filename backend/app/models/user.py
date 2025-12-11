from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from pydantic import EmailStr
import uuid


class User(SQLModel, table=True):
    """User model for authentication."""
    __tablename__ = "users"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        nullable=False
    )
    email: str = Field(
        max_length=255,
        unique=True,
        nullable=False,
        index=True
    )
    name: Optional[str] = Field(
        max_length=255,
        default=None
    )
    password_hash: str = Field(
        max_length=255,
        nullable=False
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False
    )


class UserCreate(SQLModel):
    """Schema for user registration."""
    email: EmailStr
    name: Optional[str] = None
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "name": "John Doe",
                "password": "SecurePass123"
            }
        }


class UserResponse(SQLModel):
    """Schema for user response (no password)."""
    id: uuid.UUID
    email: str
    name: Optional[str]
    created_at: datetime
