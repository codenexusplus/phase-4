from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from typing import Dict, Any
import uuid

from database.session import get_session
from models.user import User, UserCreate, UserLogin, UserPublic
from utils.auth import get_password_hash, verify_password, create_access_token, authenticate_user
from utils.error_handler import handle_error
from utils.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=UserPublic)
async def register_user(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session)
):
    """Register a new user."""
    try:
        # Check if user already exists
        existing_user = await session.execute(
            select(User).filter((User.email == user_data.email) | (User.username == user_data.username))
        )
        if existing_user.scalar_one_or_none():
            handle_error("Email or username already registered", 400)

        # Hash the password
        hashed_password = get_password_hash(user_data.password)

        # Create new user
        db_user = User(
            id=str(uuid.uuid4()),
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password
        )

        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)

        return db_user
    except IntegrityError:
        handle_error("Username or email already exists", 400)
    except Exception as e:
        handle_error(f"Registration failed: {str(e)}", 500)

@router.post("/login")
async def login_user(
    user_data: UserLogin,
    session: AsyncSession = Depends(get_session)
) -> Dict[str, Any]:
    """Login a user and return an access token."""
    try:
        user = await authenticate_user(session, user_data.email, user_data.password)
        if not user:
            handle_error("Incorrect email or password", 401)

        if not user.is_active:
            handle_error("Account is deactivated", 401)

        # Create access token
        access_token = create_access_token(data={"sub": user.id})

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username
            }
        }
    except Exception as e:
        handle_error(f"Login failed: {str(e)}", 500)

@router.get("/me", response_model=UserPublic)
async def get_user_profile(
    current_user: User = Depends(get_current_user)
):
    """Get the current user's profile."""
    return current_user
