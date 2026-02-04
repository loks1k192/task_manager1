"""Tests for task endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_task(client: AsyncClient):
    """Test creating a task."""
    # Register and get token
    register_response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "taskuser@example.com",
            "username": "taskuser",
            "password": "taskpassword123",
        },
    )
    token = register_response.json()["access_token"]

    # Create task
    response = await client.post(
        "/api/v1/tasks",
        json={"title": "Test Task", "description": "Test Description"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["is_completed"] is False


@pytest.mark.asyncio
async def test_list_tasks(client: AsyncClient):
    """Test listing tasks."""
    # Register and get token
    register_response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "listuser@example.com",
            "username": "listuser",
            "password": "listpassword123",
        },
    )
    token = register_response.json()["access_token"]

    # Create multiple tasks
    for i in range(3):
        await client.post(
            "/api/v1/tasks",
            json={"title": f"Task {i}", "description": f"Description {i}"},
            headers={"Authorization": f"Bearer {token}"},
        )

    # List tasks
    response = await client.get(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


@pytest.mark.asyncio
async def test_get_task(client: AsyncClient):
    """Test getting a task by ID."""
    # Register and get token
    register_response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "getuser@example.com",
            "username": "getuser",
            "password": "getpassword123",
        },
    )
    token = register_response.json()["access_token"]

    # Create task
    create_response = await client.post(
        "/api/v1/tasks",
        json={"title": "Get Task", "description": "Get Description"},
        headers={"Authorization": f"Bearer {token}"},
    )
    task_id = create_response.json()["id"]

    # Get task
    response = await client.get(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Get Task"


@pytest.mark.asyncio
async def test_update_task(client: AsyncClient):
    """Test updating a task."""
    # Register and get token
    register_response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "updateuser@example.com",
            "username": "updateuser",
            "password": "updatepassword123",
        },
    )
    token = register_response.json()["access_token"]

    # Create task
    create_response = await client.post(
        "/api/v1/tasks",
        json={"title": "Update Task", "description": "Update Description"},
        headers={"Authorization": f"Bearer {token}"},
    )
    task_id = create_response.json()["id"]

    # Update task
    response = await client.put(
        f"/api/v1/tasks/{task_id}",
        json={"title": "Updated Task", "is_completed": True},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Task"
    assert data["is_completed"] is True


@pytest.mark.asyncio
async def test_delete_task(client: AsyncClient):
    """Test deleting a task."""
    # Register and get token
    register_response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "deleteuser@example.com",
            "username": "deleteuser",
            "password": "deletepassword123",
        },
    )
    token = register_response.json()["access_token"]

    # Create task
    create_response = await client.post(
        "/api/v1/tasks",
        json={"title": "Delete Task", "description": "Delete Description"},
        headers={"Authorization": f"Bearer {token}"},
    )
    task_id = create_response.json()["id"]

    # Delete task
    response = await client.delete(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 204

    # Verify task is deleted
    get_response = await client.get(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert get_response.status_code == 404
