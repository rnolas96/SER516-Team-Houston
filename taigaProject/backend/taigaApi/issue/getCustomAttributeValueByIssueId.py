import os
import requests
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()


class CustomeAttributeFetchingError(Exception):
    def __init__(self, status_code, reason):
        self.status_code = status_code
        self.reason = reason

#Function to get custom attribute data from issue_id
def get_custom_attribute_value_by_issue_id(issue_id, attribute_id, auth_token):
    # Get Taiga API URL from environment variables
    taiga_url = os.getenv('TAIGA_URL')

    # Construct the URL for collecting the issues for project.
    custom_attribute_data_api_url = f"{taiga_url}/issues/custom-attributes-values/{issue_id}"

    # Define headers including the authorization token and content type
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
    }

    try:
        # Make a GET request to Taiga API
        response = requests.get(custom_attribute_data_api_url, headers=headers)
        response.raise_for_status()

        if response.status_code == 401:
            raise CustomeAttributeFetchingError(401,"Client Error: Unauthorized")

        # Extract and return the issue response list from the response
        custom_attribute_info = response.json()
        return custom_attribute_info['attributes_values'][attribute_id]

    except requests.exceptions.HTTPError as e:
        print(f"HTTP error fetching Custom Attributes of Issues By projectId: {e}")
        raise CustomeAttributeFetchingError(e.response.status_code, e.response.reason)

    except requests.exceptions.ConnectionError as e:
        print(f"Connection error fetching Custom Attributes of Issues By projectId : {e}")
        raise CustomeAttributeFetchingError("CONNECTION_ERROR", str(e))

    except Exception as e:
        print(f"Unexpected error fetching Custom Attributes of Issues By projectId:{e}")
        raise 

    
def get_custom_attribute_type_id_for_issue(project_id, auth_token, attribute_name):

    taiga_url = os.getenv('TAIGA_URL')

    custom_attribute_api_url = f"{taiga_url}/issue-custom-attributes?project={project_id}"

    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
    }

    try:

        response = requests.get(custom_attribute_api_url, headers=headers)
        response.raise_for_status() 

        if response.status_code == 401:
            raise CustomeAttributeFetchingError(401,"Client Error: Unauthorized")


        for res in response.json():
            if res["name"] == attribute_name:
                return str(res["id"])

    except requests.exceptions.HTTPError as e:
        print(f"HTTP error fetching Custom Attributes of Issues By projectId: {e}")
        raise CustomeAttributeFetchingError(e.response.status_code, e.response.reason)

    except requests.exceptions.ConnectionError as e:
        print(f"Connection error fetching Custom Attributes of Issues By projectId : {e}")
        raise CustomeAttributeFetchingError("CONNECTION_ERROR", str(e))

    except Exception as e:
        print(f"Unexpected error fetching Custom Attributes of Issues By projectId:{e}")
        raise 
