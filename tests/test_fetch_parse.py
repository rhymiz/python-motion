import os
import json
from motion import Motion, MotionResponse
from pydantic import ValidationError


def fetch_and_parse_tasks():
    # Initialize the Motion client with the API token
    motion = Motion(os.getenv("MOTION_API_TOKEN"))
    
    # Fetch tasks
    response = motion.tasks.list()
    
    # The response content is in bytes; decode it to string
    response_json = response.json()
    
    
    try:
        # Parse the dictionary into the MotionResponse Pydantic model
        motion_response = MotionResponse(**response_json)
        
        # Now you can interact with the data using Pydantic models
        print(f"Next Cursor: {motion_response.meta.nextCursor}")
        print(f"Page Size: {motion_response.meta.pageSize}")
        
        for task in motion_response.tasks:
            print(f"Task ID: {task.id}")
            print(f"Name: {task.name}")
            print(f"Due Date: {task.dueDate}")
            print(f"Assignees: {[assignee.name for assignee in task.assignees]}")
            print("-" * 40)
    
    except ValidationError as e:
        print("Error parsing Motion API response:")
        print(e.json())

if __name__ == "__main__":
    fetch_and_parse_tasks()



