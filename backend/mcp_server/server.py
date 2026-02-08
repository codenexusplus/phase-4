from mcp.server.fastmcp import FastMCP
from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import async_engine
from utils.error_handler import BusinessError
from services.task_service import TaskService


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
        result = await TaskService.add_task(session, user_id, title, description)
        return {
            "task_id": result["id"],
            "message": result["message"]
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
        tasks = await TaskService.list_tasks(session, user_id, status)
        # Remove user_id from the response for consistency with previous format
        return [
            {
                "id": task["id"],
                "title": task["title"],
                "description": task["description"],
                "completed": task["completed"],
                "created_at": task["created_at"],
                "updated_at": task["updated_at"]
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
        result = await TaskService.complete_task(session, user_id, task_id)
        return {
            "success": result["success"],
            "message": result["message"]
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
        result = await TaskService.delete_task(session, user_id, task_id)
        return {
            "success": result["success"],
            "message": result["message"]
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
        result = await TaskService.update_task(session, user_id, task_id, title, description)
        return {
            "success": result["success"],
            "message": result["message"],
            "task": {
                "id": result["task"]["id"],
                "title": result["task"]["title"],
                "description": result["task"]["description"],
                "completed": result["task"]["completed"],
                "created_at": result["task"]["created_at"],
                "updated_at": result["task"]["updated_at"]
            }
        }


# Export tools for external access (after all functions are defined)
mcp_server.tools = {
    "add_task": add_task,
    "list_tasks": list_tasks,
    "complete_task": complete_task,
    "delete_task": delete_task,
    "update_task": update_task
}
