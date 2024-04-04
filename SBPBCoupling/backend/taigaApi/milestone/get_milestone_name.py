import requests
import os

def get_milestone_name(project_id, auth_token):

    # Get Taiga API URL from environment variables
    taiga_url = os.getenv('TAIGA_URL')

    # Construct the URL for the tasks API endpoint for the specified project
    milestones_api_url = f"{taiga_url}/milestones?project={project_id}"

    # Define headers including the authorization token and content type
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
    }

    try:

        # Make a GET request to Taiga API to retrieve tasks
        response = requests.get(milestones_api_url, headers = headers)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

        milestones = response.json()
        milestones_info = {}

        for milestone in milestones:
            if milestones_info.get(milestone['id']) is None:
                milestones_info[milestone['id']] = milestone['name']

        return milestones_info

    except requests.exceptions.RequestException as e:

        # Handle errors during the API request and print an error message
        print(f"Error fetching tasks: {e}")
        return None