"""FastAPI application entry point."""

from fastapi import FastAPI

from app.api.v1 import router as v1_router
from app.core.config import settings
from app.core.exceptions import setup_exception_handlers
from app.core.logging import setup_logging

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.1.0",
    description="REST API for Task Management",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Setup logging
setup_logging()

# Setup exception handlers
setup_exception_handlers(app)

# Include routers
app.include_router(v1_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Task Management API", "version": "0.1.0"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
