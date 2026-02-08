from openai import OpenAI
from dotenv import load_dotenv
import os
from typing import Dict, Any, List
from mcp_server.server_absolute import mcp_server
from utils.context_helper_absolute import get_conversation_context
from utils.error_handler import create_error_response
from config.settings import settings

# Load environment variables
load_dotenv()

# Initialize Ollama client (using OpenAI-compatible API)
# Make sure to install ollama first and run: ollama serve
# Then pull a model: ollama pull llama3.2
client = OpenAI(
    base_url=settings.OLLAMA_BASE_URL,
    api_key=settings.OLLAMA_API_KEY
)

async def run_agent(user_message: str, conversation_id: int, user_id: str) -> Dict[str, Any]:
    """
    Runs the OpenAI agent with the conversation history and available tools.

    Args:
        user_message: The message from the user
        conversation_id: The ID of the conversation
        user_id: The ID of the user

    Returns:
        Dictionary with the agent's response
    """
    try:
        # Get conversation context (last 10 messages)
        context_messages = get_conversation_context(conversation_id, limit=10)

        # Prepare the messages for the agent
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant that manages tasks using specialized tools. You can add, list, update, complete, and delete tasks. Always respond in a friendly, helpful manner and confirm actions with the user."}
        ]

        # Add context messages
        messages.extend(context_messages)

        # Add the current user message
        messages.append({"role": "user", "content": user_message})

        # Define the available tools (MCP server tools)
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Adds a new task to the user's list",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user's ID"},
                            "title": {"type": "string", "description": "The task title"},
                            "description": {"type": "string", "description": "The task description"}
                        },
                        "required": ["user_id", "title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "Lists the user's tasks with optional status filter",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user's ID"},
                            "status": {"type": "string", "description": "Filter by status: 'all', 'pending', or 'completed'"}
                        },
                        "required": ["user_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Marks a task as completed",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user's ID"},
                            "task_id": {"type": "integer", "description": "The ID of the task to complete"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Deletes a task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user's ID"},
                            "task_id": {"type": "integer", "description": "The ID of the task to delete"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Updates a task's title or description",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user's ID"},
                            "task_id": {"type": "integer", "description": "The ID of the task to update"},
                            "title": {"type": "string", "description": "The new title for the task (optional)"},
                            "description": {"type": "string", "description": "The new description for the task (optional)"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            }
        ]

        # Call the Ollama API with tools
        response = client.chat.completions.create(
            model="llama3.2",  # Using llama3.2 as it's a good open-source model
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        # Get the response
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        # If the agent wants to call tools
        if tool_calls:
            # Execute the tool calls
            import json
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                # Call the appropriate MCP tool (these are async functions)
                if function_name == "add_task":
                    result = await mcp_server.tools[function_name](**function_args)
                elif function_name == "list_tasks":
                    result = await mcp_server.tools[function_name](**function_args)
                elif function_name == "complete_task":
                    result = await mcp_server.tools[function_name](**function_args)
                elif function_name == "delete_task":
                    result = await mcp_server.tools[function_name](**function_args)
                elif function_name == "update_task":
                    result = await mcp_server.tools[function_name](**function_args)
                else:
                    result = {"error": f"Unknown tool: {function_name}"}

                # Add the tool result to the messages
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": str(result)
                })

            # Get the final response from the agent after tool execution
            final_response = client.chat.completions.create(
                model="llama3.2",
                messages=messages
            )

            agent_response = final_response.choices[0].message.content
        else:
            # If no tools were called, just return the agent's response
            agent_response = response_message.content

        # Format the response with markdown for confirmation
        formatted_response = f"âœ… **Response:** {agent_response}"

        return {
            "response": formatted_response,
            "conversation_id": conversation_id,
            "timestamp": os.times()[4]  # Using system time
        }

    except Exception as e:
        # Handle any errors gracefully
        error_msg = f"An error occurred: {str(e)}"
        return create_error_response(error_msg, "AGENT_ERROR")
