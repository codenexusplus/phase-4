"""
Unified Task Service Layer
Provides shared functionality for both REST API and MCP tools
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from datetime import datetime
from models.task import Task
from utils.error_handler import BusinessError


class TaskService:
    """Unified service layer for task operations"""
    
    @staticmethod
    async def add_task(session: AsyncSession, user_id: str, title: str, description: Optional[str] = None) -> Dict[str, Any]:
        """
        Creates a new task in the database.

        Args:
            session: Database session
            user_id: Identifier for the user
            title: Title of the task
            description: Description of the task (optional)

        Returns:
            Dictionary containing the created task ID and success message
        """
        new_task = Task(
            title=title,
            description=description,
            user_id=user_id,
            completed=False
        )

        session.add(new_task)
        await session.commit()
        await session.refresh(new_task)

        return {
            "id": new_task.id,
            "title": new_task.title,
            "description": new_task.description,
            "completed": new_task.completed,
            "user_id": new_task.user_id,
            "created_at": new_task.created_at.isoformat(),
            "updated_at": new_task.updated_at.isoformat(),
            "message": f"Task '{title}' added successfully"
        }

    @staticmethod
    async def list_tasks(session: AsyncSession, user_id: str, status: str = "all") -> List[Dict[str, Any]]:
        """
        Filters tasks by 'all', 'pending', or 'completed'.

        Args:
            session: Database session
            user_id: Identifier for the user
            status: Filter status ('all', 'pending', 'completed')

        Returns:
            Array of task objects matching the criteria
        """
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
                "user_id": task.user_id,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }
            for task in tasks
        ]

    @staticmethod
    async def complete_task(session: AsyncSession, user_id: str, task_id: int) -> Dict[str, Any]:
        """
        Marks a specific task as completed.

        Args:
            session: Database session
            user_id: Identifier for the user
            task_id: ID of the task to complete

        Returns:
            Dictionary indicating success or failure
        """
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
            "message": f"Task '{task.title}' marked as completed",
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "user_id": task.user_id,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }
        }

    @staticmethod
    async def delete_task(session: AsyncSession, user_id: str, task_id: int) -> Dict[str, Any]:
        """
        Permanently removes a task.

        Args:
            session: Database session
            user_id: Identifier for the user
            task_id: ID of the task to delete

        Returns:
            Dictionary indicating success or failure
        """
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

    @staticmethod
    async def update_task(
        session: AsyncSession, 
        user_id: str, 
        task_id: int, 
        title: Optional[str] = None, 
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Updates existing task details.

        Args:
            session: Database session
            user_id: Identifier for the user
            task_id: ID of the task to update
            title: New title for the task (optional)
            description: New description for the task (optional)

        Returns:
            Dictionary indicating success or failure
        """
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
        if update_values:  # Only update if there are values to update
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
                "user_id": task.user_id,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }
        }
