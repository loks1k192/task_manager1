"""Pytest configuration and fixtures."""

import os

import pytest
from dotenv import load_dotenv

# Загружаем .env из корня проекта (независимо от cwd при запуске pytest)
_load_env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(_load_env_path)


from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base, get_db
from app.main import app

# Берём URL тестовой БД из окружения (пароль и хост могут отличаться)
DEFAULT_TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/task_manager_test"


def _get_test_database_url() -> str:
    """Test DB URL: TEST_DATABASE_URL, или DATABASE_URL с базой task_manager_test, или default."""
    url = os.environ.get("TEST_DATABASE_URL")
    if url:
        return url
    main_url = os.environ.get("DATABASE_URL")
    if main_url:
        # Подменить имя базы на task_manager_test (после последнего /)
        if "/" in main_url:
            base = main_url.rsplit("/", 1)[0]
            return f"{base}/task_manager_test"
    return DEFAULT_TEST_DATABASE_URL


@pytest.fixture(scope="session")
def test_database_url():
    """Test database URL (env TEST_DATABASE_URL or derived from DATABASE_URL or default)."""
    return _get_test_database_url()


@pytest.fixture
async def test_engine(test_database_url):
    """Create test database engine (function scope to avoid event loop mismatch)."""
    engine = create_async_engine(test_database_url, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def db_session(test_engine):
    """Create database session for testing."""
    async_session = sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
        await session.rollback()


@pytest.fixture
async def client(db_session: AsyncSession):
    """Create test client."""
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
