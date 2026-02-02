"""Task repository."""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task


class TaskRepository:
    """Repository for Task operations."""

    def __init__(self, session: AsyncSession):
        """Initialize repository with database session."""
        self.session = session

    async def create(self, task_data: dict) -> Task:
        """Create a new task."""
        task = Task(**task_data)
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def get_by_id(self, task_id: int) -> Optional[Task]:
        """Get task by ID."""
        result = await self.session.execute(select(Task).where(Task.id == task_id))
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: int, skip: int = 0, limit: int = 100) -> list[Task]:
        """Get tasks by user ID with pagination."""
        result = await self.session.execute(
            select(Task).where(Task.user_id == user_id).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def update(self, task: Task, task_data: dict) -> Task:
        """Update task."""
        for key, value in task_data.items():
            setattr(task, key, value)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def delete(self, task: Task) -> None:
        """Delete task."""
        await self.session.delete(task)
        await self.session.commit()

    async def list_all(self, skip: int = 0, limit: int = 100) -> list[Task]:
        """List all tasks with pagination."""
        result = await self.session.execute(select(Task).offset(skip).limit(limit))
        return list(result.scalars().all())
