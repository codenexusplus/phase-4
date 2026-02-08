from mcp.server.fastmcp import FastMCP
from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from models.task import Task
from database.connection import async_engine
from utils.error_handler import BusinessError


# Initialize MCP Server
mcp_server = FastMCP("todo-mcp-server")


@mcp_server.tool("add_task")
async def add_task(user_id: str, title: str, description: Optional[str] = None) -> dict:
    """
    Creates a new entry in the Tasks table.

    Args:
        user_id: Identifier for the user
        title: Title of the task
        description: Description of the task (optional)

    Returns:
        Dictionary containing the created task ID
    """
    async with AsyncSession(async_engine) as session:
        # Create a new task object
        new_task = Task(
            title=title,
            description=description,
            user_id=user_id,
            completed=False
        )

        # Add the new task to the session
        session.add(new_task)
        await session.commit()
        await session.refresh(new_task)

    return {
        "task_id": new_task.id,
        "message": f"Task '{title}' added successfully"
    }


@mcp_server.tool("list_tasks")
async def list_tasks(user_id: str, status: str = "all") -> List[dict]:
    """
    Filters tasks by 'all', 'pending', or 'completed'.

    Args:
        user_id: Identifier for the user
        status: Filter status ('all', 'pending', 'completed')

    Returns:
        Array of task objects matching the criteria
    """
    async with AsyncSession(async_engine) as session:
        # Build the query based on status filter
        query = select(Task).where(Task.user_id == user_id)

        if status == "pending":
            query = query.where(Task.completed == False)
        elif status == "completed":
            query = query.where(Task.completed == True)
        elif status != "all":
            raise BusinessError(f"Invalid status filter: {status}. Must be 'all', 'pending', or 'completed'")

        # Execute the query
        result = await session.execute(query)
        tasks = result.scalars().all()

    # Convert tasks to dictionaries
    return [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        }
        for task in tasks
    ]


@mcp_server.tool("complete_task")
async def complete_task(user_id: str, task_id: int) -> dict:
    """
    Marks a specific task as done.

    Args:
        user_id: Identifier for the user
        task_id: ID of the task to complete

    Returns:
        Dictionary indicating success or failure
    """
    async with AsyncSession(async_engine) as session:
        # Find the task by ID and user
        query = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        result = await session.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            raise BusinessError(f"Task with ID {task_id} not found for user {user_id}")

        # Update the task to completed
        stmt = (
            update(Task)
            .where(Task.id == task_id)
            .values(completed=True, updated_at=datetime.utcnow())
        )

        await session.execute(stmt)
        await session.commit()
        await session.refresh(task)

    return {
        "success": True,
        "message": f"Task '{task.title}' marked as completed"
    }


@mcp_server.tool("delete_task")
async def delete_task(user_id: str, task_id: int) -> dict:
    """
    Permanently removes a task.

    Args:
        user_id: Identifier for the user
        task_id: ID of the task to delete

    Returns:
        Dictionary indicating success or failure
    """
    async with AsyncSession(async_engine) as session:
        # Find the task by ID and user
        query = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        result = await session.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            raise BusinessError(f"Task with ID {task_id} not found for user {user_id}")

        # Delete the task
        stmt = delete(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        await session.execute(stmt)
        await session.commit()

    return {
        "success": True,
        "message": f"Task '{task.title}' deleted successfully"
    }


@mcp_server.tool("update_task")
async def update_task(user_id: str, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> dict:
    """
    Modifies existing task details.

    Args:
        user_id: Identifier for the user
        task_id: ID of the task to update
        title: New title for the task (optional)
        description: New description for the task (optional)

    Returns:
        Dictionary indicating success or failure
    """
    async with AsyncSession(async_engine) as session:
        # Find the task by ID and user
        query = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        result = await session.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            raise BusinessError(f"Task with ID {task_id} not found for user {user_id}")

        # Prepare update values
        update_values = {}
        if title is not None:
            update_values["title"] = title
        if description is not None:
            update_values["description"] = description
        update_values["updated_at"] = datetime.utcnow()

        # Update the task
        stmt = update(Task).where(Task.id == task_id).where(Task.user_id == user_id).values(**update_values)
        await session.execute(stmt)
        await session.commit()
        await session.refresh(task)

    return {
        "success": True,
        "message": f"Task updated successfully",
        "task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        }
    }
