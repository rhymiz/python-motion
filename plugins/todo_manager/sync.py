# python-motion/plugins/todo_manager/sync.py

import os
import re
import json
import logging
from typing import List, Dict, Any, Tuple
from motion import Motion
from pydantic import BaseModel
from motion.models import MotionResponse, Task
from pathlib import Path
from datetime import datetime

# Configure a logger for this module
logger = logging.getLogger(__name__)

# Regex pattern to match TODOs in files
TODO_PATTERN = re.compile(r'%\s*TODO\s*(.*)')

def extract_todos_from_content(file_path: str, content: str) -> List[Dict[str, Any]]:
    """
    Extracts todos from the given content of a file.

    Args:
        file_path (str): Path to the file.
        content (str): Content of the file.

    Returns:
        List[Dict[str, Any]]: List of extracted todos with category.
    """
    todos = []
    for line_num, line in enumerate(content.splitlines(), 1):
        match = TODO_PATTERN.search(line)
        if match:
            full_text = match.group(1).strip()
            if ':' in full_text:
                category, text = full_text.split(':', 1)
                category = category.strip().upper()
                text = text.strip()
            else:
                category = 'UNCATEGORIZED'
                text = full_text
            todo_id = f"{file_path}:{line_num}"
            todos.append({
                'id': todo_id,
                'category': category,
                'text': text,
                'file': file_path,
                'line': line_num,
                'status': 'active',  # New field to track status
                'created_at': datetime.utcnow().isoformat(),
                'completed_at': None  # To be filled when completed
            })
            logger.debug(f"Extracted TODO: {todos[-1]}")
    return todos

def get_all_todos(directory: str, file_types: List[str]) -> List[Dict[str, Any]]:
    """
    Walks through the directory and extracts all todos from files of specific types.

    Args:
        directory (str): Path to the directory containing files.
        file_types (List[str]): List of file extensions to scan for TODOs.

    Returns:
        List[Dict[str, Any]]: Aggregated list of all todos.
    """
    todos = []
    logger.debug(f"Scanning directory for files: {directory}")
    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in file_types):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    file_todos = extract_todos_from_content(file_path, content)
                    todos.extend(file_todos)
                    logger.debug(f"Processed file: {file_path}, found {len(file_todos)} TODO(s).")
                except (IOError, OSError) as e:
                    logger.error(f"Failed to read file {file_path}: {e}")
                    continue  # Skip files that can't be read
    logger.info(f"Total TODOs extracted from files: {len(todos)}")
    return todos

def determine_diffs(
    local_todos: List[Dict[str, Any]],
    api_todos: List[Task]
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Task]]:
    """
    Determines which todos need to be added, updated, or deleted.

    Args:
        local_todos (List[Dict[str, Any]]): Todos extracted from files.
        api_todos (List[Task]): Todos fetched from the API.

    Returns:
        Tuple containing lists of todos to add, update, and delete.
    """
    local_todo_map = {todo['id']: todo for todo in local_todos}
    api_todo_map = {task.id: task for task in api_todos}

    todos_to_add = [todo for id_, todo in local_todo_map.items() if id_ not in api_todo_map]
    todos_to_update = [
        todo for id_, todo in local_todo_map.items()
        if id_ in api_todo_map and (todo['text'] != api_todo_map[id_].name or todo['category'] != api_todo_map[id_].status.name)
    ]
    todos_to_delete = [task for task in api_todos if task.id not in local_todo_map]

    logger.debug(f"Todos to add: {len(todos_to_add)}")
    logger.debug(f"Todos to update: {len(todos_to_update)}")
    logger.debug(f"Todos to delete: {len(todos_to_delete)}")

    return todos_to_add, todos_to_update, todos_to_delete

def export_todos_to_json(todos_data: Dict[str, Any], output_path: str) -> None:
    """
    Exports the todos data to a JSON file.

    Args:
        todos_data (Dict[str, Any]): Dictionary containing all todos and their statuses.
        output_path (str): Path to the output JSON file.
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(todos_data, f, indent=4)
        logger.info(f"Exported {len(todos_data.get('todos', []))} TODO(s) to JSON file: {output_path}")
    except Exception as e:
        logger.error(f"Failed to export TODOs to JSON: {e}")
        raise

def export_todos_to_markdown(todos_data: Dict[str, Any], output_path: str, completed_todos: List[Dict[str, Any]] = None) -> None:
    """
    Exports the list of todos as categorized Markdown tables to a file, and lists completed todos.

    Args:
        todos_data (Dict[str, Any]): Dictionary containing all todos and their statuses.
        output_path (str): Path to the output Markdown file.
        completed_todos (List[Dict[str, Any]]): List of completed todos.
    """
    try:
        todos = [todo for todo in todos_data.get('todos', []) if todo['status'] == 'active']
        # Group todos by category
        categorized_todos: Dict[str, List[Dict[str, Any]]] = {}
        for todo in todos:
            category = todo.get('category', 'UNCATEGORIZED')
            categorized_todos.setdefault(category, []).append(todo)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for category in sorted(categorized_todos.keys()):
                f.write(f"### {category}\n\n")
                f.write("| ID | Text | File | Line |\n")
                f.write("|----|------|------|------|\n")
                for todo in categorized_todos[category]:
                    # Escape pipe characters in text to prevent Markdown table issues
                    text = todo['text'].replace('|', '\\|')
                    file_path = todo['file'].replace('|', '\\|')
                    f.write(f"| {todo['id']} | {text} | {file_path} | {todo['line']} |\n")
                f.write("\n")  # Add an empty line after each table

            # List the completed todos at the end of the markdown
            if completed_todos:
                f.write("### Completed TODOs\n\n")
                f.write("| ID | Text | File | Line | Completed At |\n")
                f.write("|----|------|------|------|--------------|\n")
                for todo in completed_todos:
                    text = todo['text'].replace('|', '\\|')
                    file_path = todo['file'].replace('|', '\\|')
                    completed_at = todo.get('completed_at', 'Unknown')
                    f.write(f"| {todo['id']} | {text} | {file_path} | {todo['line']} | {completed_at} |\n")

        logger.info(f"Exported TODOs to Markdown file: {output_path}")
    except Exception as e:
        logger.error(f"Failed to export TODOs to Markdown: {e}")
        raise

def load_todos_json(json_path: str) -> Dict[str, Any]:
    """
    Loads the todos.json file. If it doesn't exist, initializes a new structure.

    Args:
        json_path (str): Path to the todos.json file.

    Returns:
        Dict[str, Any]: The loaded or initialized todos data.
    """
    if not Path(json_path).exists():
        logger.info(f"todos.json not found at {json_path}. Creating a new one.")
        return {'todos': []}
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.debug(f"Loaded todos.json with {len(data.get('todos', []))} todos.")
        return data
    except Exception as e:
        logger.error(f"Failed to load todos.json: {e}")
        raise

def save_todos_json(todos_data: Dict[str, Any], json_path: str) -> None:
    """
    Saves the todos data to the todos.json file.

    Args:
        todos_data (Dict[str, Any]): The todos data to save.
        json_path (str): Path to the todos.json file.
    """
    try:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(todos_data, f, indent=4)
        logger.debug(f"Saved todos.json with {len(todos_data.get('todos', []))} todos.")
    except Exception as e:
        logger.error(f"Failed to save todos.json: {e}")
        raise

def sync_todos(
    directory: str,
    file_types: List[str],
    api_key: str,
    dry_run: bool = False,
    json_path: str = "todos.json"
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Task]]:
    """
    Synchronizes todos from specified files with the Motion API and exports them.

    Args:
        directory (str): Path to the directory containing files.
        file_types (List[str]): List of file extensions to scan for TODOs.
        api_key (str): API key for authentication.
        dry_run (bool): If True, only simulate the synchronization and show the changes.
        json_path (str): Path to the todos.json file.

    Returns:
        Tuple of lists for todos to add, update, and delete.
    """
    logger.info("Initializing Motion client.")
    motion = Motion(api_key)

    logger.debug("Fetching existing tasks from Motion API.")
    api_todos_response = motion.tasks.list().json()
    motion_response = MotionResponse.parse_obj(api_todos_response)
    api_tasks = motion_response.tasks
    logger.debug(f"Fetched {len(api_tasks)} tasks from Motion API.")

    # Load existing todos.json
    todos_data = load_todos_json(json_path)
    existing_todos = {todo['id']: todo for todo in todos_data.get('todos', [])}

    # Extract local TODOs from the files
    logger.debug("Extracting local TODOs from files.")
    local_todos = get_all_todos(directory, file_types)
    local_todo_map = {todo['id']: todo for todo in local_todos}

    # Determine diffs between local TODOs and API tasks
    todos_to_add, todos_to_update, todos_to_delete = determine_diffs(local_todos, api_tasks)

    if dry_run:
        # In dry run mode, we just log the changes without making API calls
        logger.info(f"Dry run: {len(todos_to_add)} new TODOs would be added.")
        logger.info(f"Dry run: {len(todos_to_delete)} completed TODOs would be removed from the API.")
        return todos_to_add, todos_to_update, todos_to_delete

    # Proceed with real syncing if not dry run
    # Add new todos to the Motion API
    for todo in todos_to_add:
        try:
            response = motion.tasks.create({
                'name': todo['text'],
                'description': f"File: {todo['file']}, Line: {todo['line']}"
            }).json()
            # Assuming the API returns the created task with an ID
            created_task = Task.parse_obj(response)
            logger.info(f"Added TODO to Motion API: {todo['text']} with ID {created_task.id}")
            # Update todo with API ID
            todo['api_id'] = created_task.id
            todo['status'] = 'active'
            todo['created_at'] = created_task.created_at.isoformat() if created_task.created_at else todo['created_at']
        except Exception as e:
            logger.error(f"Failed to add TODO '{todo['text']}': {e}")

    # Update todos in the Motion API
    for todo in todos_to_update:
        try:
            task = api_todo_map.get(todo['id'])
            if task:
                motion.tasks.update(task.id, {
                    'name': todo['text'],
                    'description': f"File: {todo['file']}, Line: {todo['line']}"
                })
                logger.info(f"Updated TODO in Motion API: {todo['text']}")
        except Exception as e:
            logger.error(f"Failed to update TODO '{todo['text']}': {e}")

    # Delete todos from the Motion API and mark them as completed in todos.json
    for task in todos_to_delete:
        try:
            motion.tasks.delete(task.id)
            logger.info(f"Deleted TODO ID: {task.id} from the Motion API")
            # Mark as completed in todos.json
            for todo in todos_data['todos']:
                if todo.get('api_id') == task.id:
                    todo['status'] = 'completed'
                    todo['completed_at'] = datetime.utcnow().isoformat()
        except Exception as e:
            logger.error(f"Failed to delete TODO ID '{task.id}': {e}")

    # Update todos.json with current active todos
    active_todos = [todo for todo in todos_data.get('todos', []) if todo['status'] == 'active']
    active_todos.extend(local_todos)  # Add current active todos
    todos_data['todos'] = active_todos

    # Save the updated todos.json
    save_todos_json(todos_data, json_path)

    logger.info("Sync complete.")
    return todos_to_add, todos_to_update, todos_to_delete
