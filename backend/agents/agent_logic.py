from openai import OpenAI
from dotenv import load_dotenv
import os
from typing import Dict, Any, List
from mcp_server.server import mcp_server
from utils.context_helper import get_conversation_context
from utils.error_handler import create_error_response
from utils.birthday_parser import extract_birthdays_from_text, find_birthdays_on_specific_date

# Load environment variables
load_dotenv()

# Initialize OpenAI client
openai_api_key = os.getenv("OPENAI_API_KEY")

# If OpenAI API key is not available, fall back to mock implementation
if not openai_api_key or openai_api_key == "your-chatkit-domain-key":
    # Import and use the mock implementation
    from .agent_logic_mock import run_agent
else:
    # Use the real OpenAI implementation
    client = OpenAI(api_key=openai_api_key)

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
            import re  # Import re at the beginning of the function

            # Get conversation context (last 10 messages)
            context_messages = await get_conversation_context(conversation_id, limit=10)

            # Check for queries that require context from existing tasks
            user_message_lower = user_message.lower()
            context_required = any(
                word in user_message_lower
                for word in ["who", "when", "what", "whose", "which", "bday", "birthday", "birthdays"]
            )

            # Get all tasks to look for relevant information if context is required
            all_tasks = []
            if context_required:
                try:
                    all_tasks = await mcp_server.tools["list_tasks"](user_id=user_id, status="all")
                except Exception as e:
                    # If there's an error fetching tasks, continue anyway
                    all_tasks = []

            # Check for birthday-related queries
            birthday_patterns = [
                r"whose birthday is on (\w+ \d+)",  # "whose birthday is on August 14"
                r"who has a birthday on (\w+ \d+)",  # "who has a birthday on August 14"
                r"whose birthday is (\w+ \d+)",     # "whose birthday is August 14"
                r"when is (\w+)'s birthday",       # "when is John's birthday"
                r"(\w+)'s birthday",               # "John's birthday"
                r"(\d+)(?:st|nd|rd|th)?\s*(?:april|march|may|january|february|june|july|august|september|october|november|december).*kiska.*bday",  # "5th April ko kiska bday hai?"
            ]

            birthday_query = None
            person_name = None

            for pattern in birthday_patterns:
                match = re.search(pattern, user_message_lower, re.IGNORECASE)
                if match:
                    if "whose birthday is on" in user_message_lower or "who has a birthday on" in user_message_lower or "whose birthday is" in user_message_lower:
                        # This is a query about who has a birthday on a specific date
                        birthday_query = match.group(1)
                    elif "when is" in user_message_lower:
                        # This is a query about when someone's birthday is
                        person_name = match.group(1)
                    elif "'s birthday" in user_message_lower:
                        # This might be asking about a specific person's birthday
                        person_name = match.group(1)
                    elif "kiska.*bday" in user_message_lower:
                        # Handle Hindi-style queries like "5th April ko kiska bday hai?"
                        # Extract the date part from the match
                        date_part = match.group(0)
                        # Extract the day and month
                        day_match = re.search(r'(\d+)(?:st|nd|rd|th)?', date_part)
                        month_match = re.search(r'(april|march|may|january|february|june|july|august|september|october|november|december)', date_part, re.IGNORECASE)

                        if day_match and month_match:
                            day = day_match.group(1)
                            month = month_match.group(1).capitalize()
                            birthday_query = f"{month} {day}"
                    break

            # If it's a birthday query, handle it specially
            if birthday_query:
                # Extract all task titles and descriptions to search for birthday info
                task_content = ""
                for task in all_tasks:
                    task_content += f"{task.get('title', '')} {task.get('description', '')} "

                # Find people with birthdays on the specified date
                matching_names = find_birthdays_on_specific_date(task_content, birthday_query)

                if matching_names:
                    if len(matching_names) == 1:
                        agent_response = f"{birthday_query} ko {matching_names[0]} ka birthday hai!"
                    else:
                        agent_response = f"{birthday_query} ko {', '.join(matching_names)} logon ka birthday hai!"
                else:
                    agent_response = f"Mujhe {birthday_query} ko kisi ka birthday nahi mila."

                # Format the response with markdown for confirmation
                formatted_response = f"âœ… **Response:** {agent_response}"

                return {
                    "response": formatted_response,
                    "conversation_id": conversation_id,
                    "action_performed": False,  # No task-related action was performed
                    "timestamp": os.times()[4]  # Using system time
                }
            elif person_name:
                # Extract all task titles and descriptions to search for birthday info
                task_content = ""
                for task in all_tasks:
                    task_content += f"{task.get('title', '')} {task.get('description', '')} "

                # Find the birthday for the specified person
                birthdays = extract_birthdays_from_text(task_content)
                person_birthday = None

                for name, date in birthdays:
                    if person_name.lower() in name.lower():
                        person_birthday = date
                        break

                if person_birthday:
                    agent_response = f"{person_name} ka birthday {person_birthday} ko hai."
                else:
                    agent_response = f"Mujhe {person_name} ka birthday nahi mila."

                # Format the response with markdown for confirmation
                formatted_response = f"âœ… **Response:** {agent_response}"

                return {
                    "response": formatted_response,
                    "conversation_id": conversation_id,
                    "action_performed": False,  # No task-related action was performed
                    "timestamp": os.times()[4]  # Using system time
                }

            # Prepare the messages for the agent
            messages = [
                {"role": "system", "content": "You are a helpful AI assistant that manages tasks using specialized tools. You can add, list, update, complete, and delete tasks. Always respond in a friendly, helpful manner and confirm actions with the user. When a user provides a description for a task, always include it in the task. When updating tasks, always use the update_task tool specifically for edits. Also, you can help users find birthday information in their tasks."}
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

            # Call the OpenAI API with tools
            response = client.chat.completions.create(
                model="gpt-4o",  # Using gpt-4o as it's the latest model
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )

            # Get the response
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            # Track if any action was performed that affects tasks
            action_performed = False

            # If the agent wants to call tools
            if tool_calls:
                # Execute the tool calls
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = eval(tool_call.function.arguments)

                    # Call the appropriate MCP tool
                    if function_name == "add_task":
                        result = await mcp_server.tools[function_name](**function_args)
                        action_performed = True  # Mark that a task-related action was performed
                    elif function_name == "list_tasks":
                        result = await mcp_server.tools[function_name](**function_args)
                    elif function_name == "complete_task":
                        result = await mcp_server.tools[function_name](**function_args)
                        action_performed = True  # Mark that a task-related action was performed
                    elif function_name == "delete_task":
                        result = await mcp_server.tools[function_name](**function_args)
                        action_performed = True  # Mark that a task-related action was performed
                    elif function_name == "update_task":
                        result = await mcp_server.tools[function_name](**function_args)
                        action_performed = True  # Mark that a task-related action was performed
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
                    model="gpt-4o",
                    messages=messages
                )

                agent_response = final_response.choices[0].message.content
            else:
                # If no tools were called, just return the agent's response
                agent_response = response_message.content
                action_performed = False  # No action was performed

            # Format the response with markdown for confirmation
            formatted_response = f"âœ… **Response:** {agent_response}"

            return {
                "response": formatted_response,
                "conversation_id": conversation_id,
                "action_performed": action_performed,  # Indicate if a task-related action was performed
                "timestamp": os.times()[4]  # Using system time
            }

        except Exception as e:
            # Handle any errors gracefully
            error_msg = f"An error occurred: {str(e)}"
            return create_error_response(error_msg, "AGENT_ERROR")
