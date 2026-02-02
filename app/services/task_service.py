"""Task service."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import TaskNotFoundError, UnauthorizedError
from app.repositories.task_repository import TaskRepository
from app.repositories.user_repository import UserRepository
from app.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    """Service for task operations."""

    def __init__(self, session: AsyncSession):
        """Initialize service with database session."""
        self.task_repo = TaskRepository(session)
        self.user_repo = UserRepository(session)

    async def create_task(self, user_id: int, task_data: TaskCreate) -> dict:
        """Create a new task for a user."""
        # Verify user exists
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise UnauthorizedError("User not found")

        task_dict = task_data.model_dump()
        task_dict["user_id"] = user_id
        task = await self.task_repo.create(task_dict)
        return task

    async def get_task(self, task_id: int, user_id: int) -> dict:
        """Get a task by ID."""
        task = await self.task_repo.get_by_id(task_id)
        if not task:
            raise TaskNotFoundError("Task not found")

        if task.user_id != user_id:
            raise UnauthorizedError("You don't have permission to access this task")

        return task

    async def list_tasks(self, user_id: int, skip: int = 0, limit: int = 100) -> list[dict]:
        """List tasks for a user."""
        tasks = await self.task_repo.get_by_user_id(user_id, skip=skip, limit=limit)
        return tasks

    async def update_task(self, task_id: int, user_id: int, task_data: TaskUpdate) -> dict:
        """Update a task."""
        task = await self.task_repo.get_by_id(task_id)
        if not task:
            raise TaskNotFoundError("Task not found")

        if task.user_id != user_id:
            raise UnauthorizedError("You don't have permission to update this task")

        update_dict = task_data.model_dump(exclude_unset=True)
        updated_task = await self.task_repo.update(task, update_dict)
        return updated_task

    async def delete_task(self, task_id: int, user_id: int) -> None:
        """Delete a task."""
        task = await self.task_repo.get_by_id(task_id)
        if not task:
            raise TaskNotFoundError("Task not found")

        if task.user_id != user_id:
            raise UnauthorizedError("You don't have permission to delete this task")

        await self.task_repo.delete(task)
