from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Dict, Any
import json

from database.session import get_session
from agents.agent_logic import run_agent
from models.message import Message, MessageBase
from models.conversation import Conversation
from utils.error_handler import handle_error
from config.settings import settings
from utils.auth import get_current_user
from models.user import User

router = APIRouter()


@router.post("/chat")
async def chat_endpoint(
    message_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> Dict[str, Any]:
    """
    Main chat endpoint that handles user messages and returns AI responses.

    Logic:
    1. Receive message
    2. Fetch history from MessageTable
    3. Run Agent with history + MCP tools
    4. Save user input and agent output back to MessageTable
    5. Return JSON response
    """
    try:
        # Extract message and conversation_id from the request
        user_message = message_data.get("message", "")
        conversation_id = message_data.get("conversation_id", None)
        user_id = current_user.id  # Use authenticated user's ID

        if not user_message:
            handle_error("Message content is required", 400)

        # If no conversation_id is provided, create a new conversation
        if conversation_id is None:
            new_conversation = Conversation(user_id=user_id)
            session.add(new_conversation)
            await session.commit()
            await session.refresh(new_conversation)
            conversation_id = new_conversation.id
        else:
            # Verify that the conversation belongs to the user
            conversation_query = select(Conversation).where(
                Conversation.id == conversation_id
            ).where(Conversation.user_id == user_id)

            result = await session.execute(conversation_query)
            conversation = result.scalar_one_or_none()

            if not conversation:
                handle_error("Conversation not found or does not belong to user", 404)

        # Create and save the user's message
        user_message_obj = Message(
            conversation_id=conversation_id,
            role="user",
            content=user_message
        )
        session.add(user_message_obj)
        await session.commit()
        await session.refresh(user_message_obj)

        # Run the agent with the conversation history
        agent_response = await run_agent(user_message, conversation_id, user_id)

        # Create and save the agent's response
        if "error" not in agent_response:
            agent_message_obj = Message(
                conversation_id=conversation_id,
                role="assistant",
                content=agent_response.get("response", "I processed your request.")
            )
            session.add(agent_message_obj)
            await session.commit()

        # Return the agent's response
        return agent_response

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Handle any unexpected errors
        handle_error(f"An unexpected error occurred: {str(e)}", 500)
