import os
import requests
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class TaskStatusFetchError(Exception):
    def __init__(self, status_code, reason):
        self.status_code = status_code
        self.reason = reason

# Function to retrieve project task statuses for a specific project from the Taiga API
def get_project_task_status_name(project_id, auth_token):
    # Get Taiga API URL from environment variables
    taiga_url = os.getenv('TAIGA_URL')

    # Construct the URL for the project task statuses API endpoint for the specified project
    project_task_api_url = f"{taiga_url}/task-statuses?project={project_id}"

    # Define headers including the authorization token and content type
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
    }

    try:
        # Make a GET request to Taiga API to retrieve project task statuses
        response = requests.get(project_task_api_url, headers=headers)
        response.raise_for_status()

        if response.status_code == 401:
            raise TaskStatusFetchError(401, "Client Error: Unauthorized")

        # Extract and return the project task statuses information from the response
        project_info = response.json()
        return project_info
    
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error fetching Task Status: {e}")
        raise TaskStatusFetchError(e.response.status_code, e.response.reason)

    except requests.exceptions.ConnectionError as e:
        print(f"Connection error fetching Task Status: {e}")
        raise TaskStatusFetchError("CONNECTION_ERROR", str(e))

    except Exception as e:
        print(f"Unexpected error fetching Task Status:{e}")
        raise 