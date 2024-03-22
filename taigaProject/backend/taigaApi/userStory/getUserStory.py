import os
import requests
from datetime import datetime
from datetime import datetime
from dotenv import load_dotenv
from taigaApi.task.getTasks import get_closed_tasks, get_all_tasks

# Load environment variables from .env file
load_dotenv()

class UserStoryFetchingError(Exception):
    def __init__(self, status_code, reason):
        self.status_code = status_code
        self.reason = reason

# Function to retrieve user stories for a specific project from the Taiga API
def get_user_story(project_id, auth_token):

    # Get Taiga API URL from environment variables
    taiga_url = os.getenv('TAIGA_URL')

    # Construct the URL for the user stories API endpoint for the specified project
    user_story_api_url = f"{taiga_url}/userstories?project={project_id}"

    # Define headers including the authorization token and content type
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
    }

    try:

        # Make a GET request to Taiga API to retrieve user stories
        response = requests.get(user_story_api_url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

        if response.status_code == 401:
            raise UserStoryFetchingError(401, "Client Error: Unauthorized")

        # Extract and return the user stories information from the response
        project_info = response.json()
        return project_info

    except requests.exceptions.HTTPError as e:
        print(f"HTTP error fetching UserStory: {e}")
        raise UserStoryFetchingError(e.response.status_code, e.response.reason)

    except requests.exceptions.ConnectionError as e:
        print(f"Connection error fetching UserStory: {e}")
        raise UserStoryFetchingError("CONNECTION_ERROR", str(e))

    except Exception as e:
        print("Unexpected error fetching UserStory:")
        raise 

def get_custom_attribute_from_userstory(user_story_id, auth_token):

    taiga_url = os.getenv('TAIGA_URL')

    custom_attribute_api_url = f"{taiga_url}/userstories/custom-attributes-values/{user_story_id}"

    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
    }

    try:

        response = requests.get(custom_attribute_api_url, headers=headers)
        response.raise_for_status() 
        
        if response.status_code == 401:
            raise UserStoryFetchingError(401, "Client Error: Unauthorized")

        custom_attribute = response.json()
        custom_attribute_data = custom_attribute['attributes_values']

        return custom_attribute_data

    except requests.exceptions.HTTPError as e:
        print(f"HTTP error fetching UserStory: {e}")
        raise UserStoryFetchingError(e.response.status_code, e.response.reason)

    except requests.exceptions.ConnectionError as e:
        print(f"Connection error fetching UserStory: {e}")
        raise UserStoryFetchingError("CONNECTION_ERROR", str(e))

    except Exception as e:
        print("Unexpected error fetching UserStory:")
        raise 
    
def get_userstories_by_sprint(sprint_id, auth_token):
    taiga_url = os.getenv('TAIGA_URL')

    userstory_api_url = f"{taiga_url}/userstories?milestone={sprint_id}"

    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
    }
    try:

        # Make a GET request to Taiga API to retrieve user stories
        response = requests.get(userstory_api_url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

        # Extract and return the user stories information from the response
        project_info = response.json()
        return project_info

    except requests.exceptions.HTTPError as e:
        print(f"HTTP error fetching UserStory: {e}")
        raise UserStoryFetchingError(e.response.status_code, e.response.reason)

    except requests.exceptions.ConnectionError as e:
        print(f"Connection error fetching UserStory: {e}")
        raise UserStoryFetchingError("CONNECTION_ERROR", str(e))

    except Exception as e:
        print("Unexpected error fetching UserStory:")
        raise 
    
def get_custom_attribute_type_id(project_id, auth_token, attribute_name):

    taiga_url = os.getenv('TAIGA_URL')

    custom_attribute_api_url = f"{taiga_url}/userstory-custom-attributes?project={project_id}"

    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
    }

    try:

        response = requests.get(custom_attribute_api_url, headers=headers)
        response.raise_for_status() 

        if response.status_code == 401:
            raise UserStoryFetchingError(401, "Client Error: Unauthorized")

        for res in response.json():
            if res["name"] == attribute_name:
                return str(res["id"])

    except requests.exceptions.HTTPError as e:
        print(f"HTTP error fetching UserStory: {e}")
        raise UserStoryFetchingError(e.response.status_code, e.response.reason)

    except requests.exceptions.ConnectionError as e:
        print(f"Connection error fetching UserStory: {e}")
        raise UserStoryFetchingError("CONNECTION_ERROR", str(e))

    except Exception as e:
        print("Unexpected error fetching UserStory:")
        raise 

    # return "40205"

def get_userstories_by_sprint(sprint_id, auth_token):
    taiga_url = os.getenv('TAIGA_URL')

    userstory_api_url = f"{taiga_url}/userstories?milestone={sprint_id}"

    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
    }
    try:

        # Make a GET request to Taiga API to retrieve user stories
        response = requests.get(userstory_api_url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

        if response.status_code == 401:
            raise UserStoryFetchingError(401, "Client Error: Unauthorized")

        # Extract and return the user stories information from the response
        project_info = response.json()
        return project_info

    except requests.exceptions.HTTPError as e:
        print(f"HTTP error fetching UserStory: {e}")
        raise UserStoryFetchingError(e.response.status_code, e.response.reason)

    except requests.exceptions.ConnectionError as e:
        print(f"Connection error fetching UserStory: {e}")
        raise UserStoryFetchingError("CONNECTION_ERROR", str(e))

    except Exception as e:
        print("Unexpected error fetching UserStory:")
        raise 

def get_userstory_total_points(project_id, auth_token):
    """
    Retrieves total story points for a User Story.

    Args:
        project_id (str): ID of the project.
        auth_token (str): User authorization token.

    Returns:
        dict: Userstory ID with total story point

    Raises:
        UserStoryFetchingError: If the user story data cannot be retrieved.
    """
    try:
        userstories_data = get_user_story(project_id, auth_token)

        userstory_total_points = [
            {
                "id": userstory_data["id"],
                "total_points": userstory_data.get("total_points", 0)
            }
            for userstory_data in userstories_data
        ]

        userstory_total_points = {story["id"]: story.get("total_points", 0) for story in userstories_data}

        return userstory_total_points
    except Exception as e:
        raise UserStoryFetchingError(401, f"CONNECTION_ERROR: {e}")

def get_closed_tasks_per_user_story(project_id, auth_token):
    """
    Retrieves the closed task for each User Story.

    Args:
        project_id (str): ID of the Taiga Project.
        auth_token (str): Authorization token of the user.

    Returns:
        dict: Number of closed task for each user story.

    Raises:
        UserStoryFetchingError: If the user story data cannot be retrieved.
    """
    try:
        closed_tasks = get_closed_tasks(project_id, auth_token)

        closed_tasks_details = {}

        for closed_task in closed_tasks:
            user_story = closed_task.get("user_story")
            task_id = closed_task.get("id")
            finished_date = closed_task.get("finished_date")
            datetime_obj = datetime.strptime(finished_date, "%Y-%m-%dT%H:%M:%S.%fZ")
            normal_date = datetime_obj.strftime("%Y-%m-%d")

            if user_story:
                closed_task_info = closed_tasks_details.get(user_story, [])
                closed_task_info.append({"task_id": task_id, "finished_date": normal_date})
                closed_tasks_details[user_story] = closed_task_info

        return closed_tasks_details

    except Exception as e:
        raise UserStoryFetchingError(401, f"CONNECTION_ERROR: {e}")
    
def get_task_per_user_story(project_id, auth_token):
    """
    Retrives all the task for a user story.
    
    Args:
        project_id (str): ID of the Taiga Project.
        auth_token (str): Bearer token for Taiga.
    
    Return:
        dict: Number of task for a user story
    `
    Raises:
        UserStoryFectchingError: If the User Story details cannot be retrieved.
    """
    try:
        tasks = get_all_tasks(project_id, auth_token)

        tasks_details = {}

        for task in tasks:
            user_story = task.get("user_story")

            if user_story:
                task_id = task.get("id")
                task_info = tasks_details.get(user_story, [])
                task_info.append({"task_id": task_id})
                tasks_details[user_story] = task_info

        return tasks_details

    except Exception as e:
        raise UserStoryFetchingError(401, f"CONNECTION_ERROR: {e}")
    