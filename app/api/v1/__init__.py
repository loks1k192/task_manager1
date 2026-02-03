"""API v1 routes."""

from fastapi import APIRouter

from app.api.v1 import auth, tasks

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
