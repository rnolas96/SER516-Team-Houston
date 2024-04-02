import os
import requests
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class TaskFetchingError(Exception):
    def __init__(self, status_code, reason):
        self.status_code = status_code
        self.reason = reason
    
def get_tasks(project_id, auth_token):

    # Get Taiga API URL from environment variables
    taiga_url = os.getenv('TAIGA_URL')

    # Construct the URL for the tasks API endpoint for the specified project
    task_api_url = f"{taiga_url}/tasks?project={project_id}"

    # Define headers including the authorization token and content type
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
        'x-disable-pagination': 'True'
    }

    try:

        # Make a GET request to Taiga API to retrieve tasks
        response = requests.get(task_api_url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        
        if response.status_code == 401:
            raise TaskFetchingError(401, "Client Error: Unauthorized")

        # Extract and return the tasks information from the response
        project_info = response.json()
        return project_info

    except requests.exceptions.HTTPError as e:
        print(f"HTTP error fetching Tasks: {e}")
        raise TaskFetchingError(e.response.status_code, e.response.reason)

    except requests.exceptions.ConnectionError as e:
        print(f"Connection error fetching Tasks: {e}")
        raise TaskFetchingError("CONNECTION_ERROR", str(e))

    except Exception as e:
        print(f"Unexpected error fetching Tasks:{e}")
        raise 

def get_tasks_by_milestone(project_id, sprint_id, auth_token):
    # Get Taiga API URL from environment variables
    taiga_url = os.getenv('TAIGA_URL')
    # Construct the URL for the tasks API endpoint for the specified project
    task_api_url = f"{taiga_url}/tasks?project={project_id}&milestone={sprint_id}"
    # Define headers including the authorization token and content type
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
    }
    try:
        # Make a GET request to Taiga API to retrieve tasks
        response = requests.get(task_api_url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        
        if response.status_code == 401:
            raise TaskFetchingError(401, "Client Error: Unauthorized")

        # Extract and return the tasks information from the response
        tasks = response.json()
        return tasks
   
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error fetching Tasks: {e}")
        raise TaskFetchingError(e.response.status_code, e.response.reason)

    except requests.exceptions.ConnectionError as e:
        print(f"Connection error fetching Tasks: {e}")
        raise TaskFetchingError("CONNECTION_ERROR", str(e))

    except Exception as e:
        print("Unexpected error fetching Tasks:")
        raise 

def get_closed_tasks(project_id, auth_token):

    try:
        # Call the get_tasks function to retrieve all tasks for the project
        tasks = get_tasks(project_id, auth_token)
        if tasks:
            # Filter tasks to include only closed tasks and format the result
            closed_tasks = [
                {
                    "id": task["id"],
                    "subject": task["subject"],
                    "created_date": task["created_date"],
                    "finished_date": task["finished_date"],
                    "milestone_id": task["milestone"],
                    "milestone_slug": task["milestone_slug"],
                    "assigned_to": task["assigned_to_extra_info"]['full_name_display'],
                    "user_story": task["user_story"]
                }
                for task in tasks if task.get("is_closed") and task['assigned_to_extra_info'] is not None
            ]

            return closed_tasks
        else:
            return None
    
    except TaskFetchingError as e:
        raise
    
    except Exception as e:
        print(f"Unexpected error fetching Tasks:{e}")
        raise 
    
    except requests.exceptions.HTTPError as e:
        raise
    
def get_all_tasks(project_id, auth_token):

    try:
        # Call the get_tasks function to retrieve all tasks for the project
        tasks = get_tasks(project_id, auth_token)

        if tasks:
            # Format all tasks and return the result
            all_tasks = [
                {
                    "id": task["id"],
                    "milestone": task["milestone"],
                    "milestone_slug": task["milestone_slug"],
                    "created_date": task["created_date"],
                    "finished_date": task["finished_date"],
                    "user_story": task["user_story"]
                }
                for task in tasks
            ]

            return all_tasks
        else:
            return None
    
    except TaskFetchingError as e:
        raise

    except Exception as e:
        # Handle unexpected exceptions in get_all_tasks
        print(f"Unexpected error in get_all_tasks: {e}")
        # Consider returning None or a specific error message here
        return None
    
