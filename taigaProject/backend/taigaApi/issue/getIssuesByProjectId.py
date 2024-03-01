import os
import requests
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class IssueFetchingError(Exception):
    def __init__(self, status_code, reason):
        self.status_code = status_code
        self.reason = reason


# Function to retrieve issues based on project id
def get_issues_by_project_id(project_id, auth_token):
    # Get Taiga API URL from environment variables
    taiga_url = os.getenv('TAIGA_URL')

    # Construct the URL for collecting the issues for project.
    issue_api_url = f"{taiga_url}/issues?project={project_id}"

    # Define headers including the authorization token and content type
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
    }

    try:
        # Make a GET request to Taiga API
        response = requests.get(issue_api_url, headers=headers)
        response.raise_for_status()

        if response.status_code == 401:
            raise IssueFetchingError(401, "Client Error: Unauthorized")

        # Extract and return the issue response list from the response
        issue_info = response.json()
        return issue_info

    except requests.exceptions.HTTPError as e:
        print(f"HTTP error fetching Issues: {e}")
        raise IssueFetchingError(e.response.status_code, e.response.reason)

    except requests.exceptions.ConnectionError as e:
        print(f"Connection error fetching Issues: {e}")
        raise IssueFetchingError("CONNECTION_ERROR", str(e))

    except Exception as e:
        print(f"Unexpected error fetching Issues:{e}")
        raise 
