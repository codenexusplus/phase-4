from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import uuid

from database.session import get_session
from models.task import Task, TaskBase, TaskCreate, TaskUpdate
from models.user import User
from utils.auth import get_current_user
from utils.error_handler import handle_error
from services.task_service import TaskService

router = APIRouter()


@router.get("/{user_id}/tasks")
async def get_tasks(
    user_id: str,
    status: str = "all",  # Query parameter to filter by status
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Retrieve all tasks for a specific user.

    Args:
        user_id: The ID of the user whose tasks to retrieve
        status: Filter by status - 'all', 'pending', or 'completed'
        current_user: The authenticated user (from token)
        session: Database session

    Returns:
        List of tasks for the user
    """
    # Verify that the requested user_id matches the authenticated user
    if current_user.id != user_id:
        handle_error("Access denied: Cannot access another user's tasks", 403)

    # Use the unified service layer
    tasks = await TaskService.list_tasks(session, user_id, status)

    # Convert tasks to dictionaries to ensure proper serialization
    tasks_dict = []
    for task in tasks:
        task_dict = {
            "id": task["id"],
            "title": task["title"],
            "description": task["description"],
            "user_id": task["user_id"],
            "completed": task["completed"],
            "created_at": task["created_at"],
            "updated_at": task["updated_at"]
        }
        tasks_dict.append(task_dict)

    return tasks_dict


@router.post("/{user_id}/tasks")
async def create_task(
    user_id: str,
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Create a new task for a specific user.

    Args:
        user_id: The ID of the user creating the task
        task_data: Task details (title, description)
        current_user: The authenticated user (from token)
        session: Database session

    Returns:
        Created task
    """
    # Verify that the requested user_id matches the authenticated user
    if current_user.id != user_id:
        handle_error("Access denied: Cannot create tasks for another user", 403)

    # Use the unified service layer
    result = await TaskService.add_task(
        session,
        current_user.id,
        task_data.title,
        task_data.description
    )

    return {
        "id": result["id"],
        "title": result["title"],
        "description": result["description"],
        "user_id": result["user_id"],
        "completed": result["completed"],
        "created_at": result["created_at"],
        "updated_at": result["updated_at"]
    }


@router.put("/{user_id}/tasks/{task_id}")
async def update_task(
    user_id: str,
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Update an existing task for a specific user.

    Args:
        user_id: The ID of the user
        task_id: The ID of the task to update
        task_data: Updated task details
        current_user: The authenticated user (from token)
        session: Database session

    Returns:
        Updated task
    """
    # Verify that the requested user_id matches the authenticated user
    if current_user.id != user_id:
        handle_error("Access denied: Cannot update another user's tasks", 403)

    # Use the unified service layer
    result = await TaskService.update_task(
        session,
        user_id,
        task_id,
        task_data.title,
        task_data.description
    )

    return {
        "id": result["task"]["id"],
        "title": result["task"]["title"],
        "description": result["task"]["description"],
        "user_id": result["task"]["user_id"],
        "completed": result["task"]["completed"],
        "created_at": result["task"]["created_at"],
        "updated_at": result["task"]["updated_at"]
    }


@router.patch("/{user_id}/tasks/{task_id}/complete")
async def update_task_completion(
    user_id: str,
    task_id: int,
    completed_status: dict,  # Expecting a dict with "completed" boolean
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Update the completion status of a task.

    Args:
        user_id: The ID of the user
        task_id: The ID of the task to update
        completed_status: Dict containing the new completion status
        current_user: The authenticated user (from token)
        session: Database session

    Returns:
        Updated task
    """
    # Verify that the requested user_id matches the authenticated user
    if current_user.id != user_id:
        handle_error("Access denied: Cannot update another user's tasks", 403)

    # Validate the input
    if "completed" not in completed_status:
        handle_error("Request must include 'completed' field", 400)

    # Use the unified service layer
    result = await TaskService.update_task(
        session,
        user_id,
        task_id,
        title=None,  # Don't update title
        description=None  # Don't update description
    )

    # Update the completion status specifically
    result = await TaskService.complete_task(session, user_id, task_id)

    return {
        "id": result["task"]["id"],
        "title": result["task"]["title"],
        "description": result["task"]["description"],
        "user_id": result["task"]["user_id"],
        "completed": result["task"]["completed"],
        "created_at": result["task"]["created_at"],
        "updated_at": result["task"]["updated_at"]
    }


@router.delete("/{user_id}/tasks/{task_id}")
async def delete_task(
    user_id: str,
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Delete a specific task for a user.

    Args:
        user_id: The ID of the user
        task_id: The ID of the task to delete
        current_user: The authenticated user (from token)
        session: Database session

    Returns:
        Confirmation message
    """
    # Verify that the requested user_id matches the authenticated user
    if current_user.id != user_id:
        handle_error("Access denied: Cannot delete another user's tasks", 403)

    # Use the unified service layer
    result = await TaskService.delete_task(session, user_id, task_id)

    return {"message": result["message"]}
