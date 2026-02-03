"""Task endpoints."""

from typing import List

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user_id
from app.db.base import get_db
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services.task_service import TaskService

router = APIRouter()


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> TaskResponse:
    """Create a new task."""
    task_service = TaskService(db)
    task = await task_service.create_task(user_id, task_data)
    return TaskResponse.model_validate(task)


@router.get("", response_model=List[TaskResponse])
async def list_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> List[TaskResponse]:
    """List all tasks for the current user."""
    task_service = TaskService(db)
    tasks = await task_service.list_tasks(user_id, skip=skip, limit=limit)
    return [TaskResponse.model_validate(task) for task in tasks]


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> TaskResponse:
    """Get a task by ID."""
    task_service = TaskService(db)
    task = await task_service.get_task(task_id, user_id)
    return TaskResponse.model_validate(task)


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> TaskResponse:
    """Update a task."""
    task_service = TaskService(db)
    task = await task_service.update_task(task_id, user_id, task_data)
    return TaskResponse.model_validate(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete a task."""
    task_service = TaskService(db)
    await task_service.delete_task(task_id, user_id)
