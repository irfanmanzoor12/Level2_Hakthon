from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import Annotated
from ..database import get_session
from ..models.user import User, UserCreate, UserResponse
from ..services.auth_service import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserCreate,
    session: Annotated[Session, Depends(get_session)]
):
    """Register a new user."""
    # Check if email already exists
    statement = select(User).where(User.email == user_data.email)
    existing_user = session.exec(statement).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Validate password length
    if len(user_data.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters"
        )

    # Create user
    user = User(
        email=user_data.email,
        name=user_data.name,
        password_hash=hash_password(user_data.password)
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    # Generate token
    token = create_access_token(user.id, user.email)

    return {
        "user": UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            created_at=user.created_at
        ),
        "token": token
    }


@router.post("/login", response_model=dict)
def login(
    user_data: UserCreate,
    session: Annotated[Session, Depends(get_session)]
):
    """Login user and return JWT token."""
    # Find user by email
    statement = select(User).where(User.email == user_data.email)
    user = session.exec(statement).first()

    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Generate token
    token = create_access_token(user.id, user.email)

    return {
        "user": UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            created_at=user.created_at
        ),
        "token": token
    }
