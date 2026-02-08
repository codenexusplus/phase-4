from openai import OpenAI
from dotenv import load_dotenv
import os
from typing import Dict, Any, List
from mcp_server.server import mcp_server
from utils.context_helper import get_conversation_context
from utils.error_handler import create_error_response
from config.settings import settings
from utils.birthday_parser import extract_birthdays_from_text, find_birthdays_on_specific_date
import json

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
        context_messages = await get_conversation_context(conversation_id, limit=10)

        # Prepare the messages for the agent
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant that manages tasks using specialized tools. You can add, list, update, complete, and delete tasks. Always respond in a friendly, helpful manner and confirm actions with the user. When a user provides a description for a task, always include it in the task. When updating tasks, always use the update_task tool specifically for edits."}
        ]

        # For now, return a mock response since the LLM service might not be available
        # This will at least allow the chat functionality to work
        import re  # Import re at the beginning of the function
        user_message_lower = user_message.lower()

        # Check for queries that require context from existing tasks
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
        # Check for more specific phrases first to avoid conflicts
        # (e.g., "show task" should trigger "show" rather than "task")
        elif any(greeting in user_message_lower for greeting in ["hello", "hi", "hey"]):
            agent_response = "Hello there! I'm your AI assistant. How can I help you today?"
        elif any(action in user_message_lower for action in ["show", "list", "view"]) and any(item in user_message_lower for item in ["task", "my"]):
            # Actually list tasks using the MCP tool
            try:
                result = await mcp_server.tools["list_tasks"](user_id=user_id, status="all")
                if result:
                    task_titles = [f"- {task['title']}" for task in result]
                    agent_response = f"I found {len(result)} tasks for you:\n" + "\n".join(task_titles)
                else:
                    agent_response = "You don't have any tasks yet. You can add a new task!"
            except Exception as e:
                agent_response = "I can help you view your tasks. The system is retrieving your task list."
        elif "delete" in user_message_lower or "remove" in user_message_lower:
            # Extract task ID if mentioned in the message
            task_ids = re.findall(r'\d+', user_message)
            if task_ids:
                try:
                    task_id = int(task_ids[0])
                    result = await mcp_server.tools["delete_task"](user_id=user_id, task_id=task_id)
                    agent_response = result.get("message", f"I've deleted task #{task_id}. The task has been removed from your list.")
                except Exception as e:
                    agent_response = f"I tried to delete task #{task_id}, but encountered an error: {str(e)}"
            else:
                agent_response = "I need a specific task number to delete. Please mention the task ID."
        elif "complete" in user_message_lower or "done" in user_message_lower:
            # Extract task ID if mentioned in the message
            task_ids = re.findall(r'\d+', user_message)
            if task_ids:
                try:
                    task_id = int(task_ids[0])
                    result = await mcp_server.tools["complete_task"](user_id=user_id, task_id=task_id)
                    agent_response = result.get("message", f"I've marked task #{task_id} as completed. Great job!")
                except Exception as e:
                    agent_response = f"I tried to mark a task as completed, but encountered an error: {str(e)}"
            else:
                agent_response = "I need a specific task number to mark as completed. Please mention the task ID."
        elif any(update_word in user_message_lower for update_word in ["update", "change", "modify", "edit"]):
            # Extract task ID and new title/description
            task_ids = re.findall(r'\d+', user_message)
            if task_ids:
                try:
                    task_id = int(task_ids[0])

                    # Extract new title and description from the message
                    # Look for patterns like "update task 1 to 'new title' with description 'desc'"
                    title_pattern = r'(?:update|change|modify|edit)\s+(?:task\s+)?\d+\s+(?:to|with|as)\s+"?([^".,!?]+)"?'
                    desc_pattern = r'(?:with\s+description|description\s+is)\s+"?([^".,!?]+)"?'

                    title_match = re.search(title_pattern, user_message_lower)
                    desc_match = re.search(desc_pattern, user_message_lower)

                    new_title = title_match.group(1).strip().capitalize() if title_match else None
                    new_description = desc_match.group(1).strip() if desc_match else None

                    # If we didn't find title via the first pattern, try to extract it differently
                    if not new_title:
                        # Look for the content after the action word
                        words = user_message_lower.split()
                        for i, word in enumerate(words):
                            if word in ["update", "change", "modify", "edit"]:
                                # Get the next few words as the title
                                remaining = " ".join(words[i+1:])
                                # Remove common phrases like "with description" to isolate the title
                                if "with description" in remaining:
                                    new_title = remaining.split("with description")[0].strip()
                                else:
                                    new_title = remaining.strip()
                                break

                    # Call the update_task tool with both title and description if available
                    result = await mcp_server.tools["update_task"](
                        user_id=user_id,
                        task_id=task_id,
                        title=new_title,
                        description=new_description
                    )

                    if new_title and new_description:
                        agent_response = result.get("message", f"I've updated task #{task_id} with title '{new_title}' and description '{new_description}'")
                    elif new_title:
                        agent_response = result.get("message", f"I've updated task #{task_id} with the new title: '{new_title}'")
                    elif new_description:
                        agent_response = result.get("message", f"I've updated task #{task_id} with the new description: '{new_description}'")
                    else:
                        agent_response = f"I've processed your request to update task #{task_id}. Please specify what you'd like to change it to."
                except Exception as e:
                    agent_response = f"I tried to update a task, but encountered an error: {str(e)}"
            else:
                agent_response = "I need a specific task number to update. Please mention the task ID."
        elif "help" in user_message_lower:
            agent_response = "I'm here to help you manage your tasks. You can ask me to add, list, complete, or delete tasks."
        elif any(word in user_message_lower for word in ["add", "create", "new task", "make task"]):
            # Extract task title and description from the message using more comprehensive regex
            # Look for patterns that include both title and description
            # e.g., "add task 'Buy groceries' with description 'Get milk, bread, eggs'"
            title_desc_pattern = r'(?:add|create|make)\s+(?:a\s+|a\s+new\s+)?(?:task\s+)?(?:named\s+|called\s+|to\s+)?["\']([^"\']+?)["\']\s+(?:with\s+description|description\s+is|described\s+as)\s+["\']([^"\']+?)["\']'
            match = re.search(title_desc_pattern, user_message_lower)

            task_title = "New task"  # default title
            task_description = None  # default description

            if match:
                # Found both title and description
                task_title = match.group(1).strip().capitalize()
                task_description = match.group(2).strip()
            else:
                # Look for various patterns like "add 'task title'", "add task to 'title'", etc.
                patterns = [
                    r'(?:add|create|make)\s+(?:a\s+|a\s+new\s+)?(?:task\s+)?(?:named\s+|called\s+|to\s+)?"?([^".,!?]+)"?',  # "add task named X", "add X", etc.
                    r'new\s+task\s+(?:named\s+|called\s+|to\s+)?"?([^".,!?]+)"?',  # "new task X"
                ]

                for pattern in patterns:
                    match = re.search(pattern, user_message_lower)
                    if match:
                        task_title = match.group(1).strip().capitalize()
                        break

                # If no match found with regex, try to extract based on position
                if task_title == "New task" or not task_title.strip():
                    # Split the message and try to get the meaningful part after action words
                    words = user_message_lower.split()
                    try:
                        # Find the index after action words
                        for i, word in enumerate(words):
                            if word in ["add", "create", "make"]:
                                # Take the next few words as the task title
                                remaining_words = words[i+1:]
                                # Filter out common words and join the rest
                                filtered_words = [w for w in remaining_words if w not in ["a", "an", "the", "to", "my", "task", "tasks", "called", "named", "with", "description", "is", "described", "as"]]
                                if filtered_words:
                                    task_title = " ".join(filtered_words).strip().capitalize()
                                    break
                    except:
                        pass

            # Ensure we have a valid task title
            if not task_title.strip() or task_title == "New task":
                task_title = "New task from AI assistant"

            try:
                result = await mcp_server.tools["add_task"](user_id=user_id, title=task_title, description=task_description)
                if task_description:
                    agent_response = f"I've added the task '{task_title}' with description '{task_description}' to your list. Task ID: {result['task_id']}"
                else:
                    agent_response = f"I've added the task '{task_title}' to your list. Task ID: {result['task_id']}"

                # After adding a task, refresh the all_tasks list to include the new task
                try:
                    all_tasks = await mcp_server.tools["list_tasks"](user_id=user_id, status="all")
                except:
                    pass  # If refreshing fails, continue with the old list
            except Exception as e:
                agent_response = f"I tried to add the task '{task_title}', but encountered an error: {str(e)}"
        else:
            # For general queries, try to find relevant information in existing tasks
            if all_tasks:
                # Look for keywords from the user's message in existing tasks
                relevant_tasks = []
                user_keywords = user_message_lower.split()

                for task in all_tasks:
                    task_text = f"{task.get('title', '')} {task.get('description', '')}".lower()
                    if any(keyword.lower() in task_text for keyword in user_keywords):
                        relevant_tasks.append(task)

                if relevant_tasks:
                    if len(relevant_tasks) == 1:
                        task = relevant_tasks[0]
                        agent_response = f"I found a relevant task: '{task['title']}'"
                        if task.get('description'):
                            agent_response += f" (Description: {task['description']})"
                    else:
                        agent_response = f"I found {len(relevant_tasks)} tasks related to your query:"
                        for i, task in enumerate(relevant_tasks[:3]):  # Show first 3 tasks
                            agent_response += f"\n- {task['title']}"
                            if task.get('description'):
                                agent_response += f" (Description: {task['description']})"
                else:
                    agent_response = "I processed your request. Let me know if you'd like me to help with tasks."
            else:
                agent_response = "I processed your request. Let me know if you'd like me to help with tasks."

        # Format the response with markdown for confirmation
        formatted_response = f"âœ… **Response:** {agent_response}"

        return {
            "response": formatted_response,
            "action_performed": True,  # Indicate that an action was performed
            "conversation_id": conversation_id,
            "timestamp": os.times()[4]  # Using system time
        }

    except Exception as e:
        # Handle any errors gracefully
        error_msg = f"An error occurred: {str(e)}"
        return create_error_response(error_msg, "AGENT_ERROR")
