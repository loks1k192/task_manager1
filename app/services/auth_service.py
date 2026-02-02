"""Authentication service."""

from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import UnauthorizedError, UserNotFoundError, ValidationError
from app.core.security import create_access_token, get_password_hash, verify_password
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class AuthService:
    """Service for authentication operations."""

    def __init__(self, session: AsyncSession):
        """Initialize service with database session."""
        self.user_repo = UserRepository(session)

    async def register_user(self, user_data: UserCreate) -> dict:
        """Register a new user."""
        # Check if user already exists
        existing_user = await self.user_repo.get_by_email(user_data.email)
        if existing_user:
            raise ValidationError("User with this email already exists")

        existing_username = await self.user_repo.get_by_username(user_data.username)
        if existing_username:
            raise ValidationError("User with this username already exists")

        # Create user
        user_dict = user_data.model_dump()
        user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))
        user = await self.user_repo.create(user_dict)

        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email, "user_id": user.id}, expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer", "user_id": user.id}

    async def authenticate_user(self, email: str, password: str) -> dict:
        """Authenticate user and return access token."""
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise UserNotFoundError("User not found")

        if not verify_password(password, user.hashed_password):
            raise UnauthorizedError("Incorrect password")

        if not user.is_active:
            raise UnauthorizedError("User is inactive")

        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email, "user_id": user.id}, expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer", "user_id": user.id}
