from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Dict
from models.message import Message
from database.connection import async_engine


async def get_conversation_context(conversation_id: int, limit: int = 10) -> List[Dict[str, str]]:
    """
    Fetches the last N messages from the DB to maintain stateless memory.

    Args:
        conversation_id: The ID of the conversation
        limit: The number of messages to fetch (default: 10)

    Returns:
        List of message dictionaries with role and content
    """
    async with AsyncSession(async_engine) as session:
        # Query to get the most recent messages for the conversation
        query = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        )

        result = await session.execute(query)
        messages = result.scalars().all()

        # Convert to list of dictionaries in reverse order (oldest first)
        context = []
        for msg in reversed(messages):
            context.append({
                "role": msg.role,
                "content": msg.content
            })

        return context
