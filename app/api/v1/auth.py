"""Authentication endpoints."""

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user_id
from app.db.base import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> JSONResponse:
    """Register a new user."""
    auth_service = AuthService(db)
    result = await auth_service.register_user(user_data)
    return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    email: str,
    password: str,
    db: AsyncSession = Depends(get_db),
) -> JSONResponse:
    """Login user and get access token."""
    auth_service = AuthService(db)
    result = await auth_service.authenticate_user(email, password)
    return JSONResponse(content=result)


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    """Get current user information."""
    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(user_id)
    if not user:
        raise ValueError("User not found")
    return UserResponse.model_validate(user)
