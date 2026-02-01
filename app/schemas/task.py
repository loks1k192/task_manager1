"""Task schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    """Base task schema."""

    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None


class TaskCreate(TaskBase):
    """Task creation schema."""

    pass


class TaskUpdate(BaseModel):
    """Task update schema."""

    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    is_completed: Optional[bool] = None


class TaskResponse(TaskBase):
    """Task response schema."""

    id: int
    is_completed: bool
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        """Pydantic config."""

        from_attributes = True
