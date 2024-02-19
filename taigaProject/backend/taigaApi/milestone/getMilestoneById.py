import requests
import os

def get_milestone_by_id(milestone_id, auth_token):


    taiga_url = os.getenv('TAIGA_URL')
    taiga_api_url = f"{taiga_url}/milestones/{milestone_id}"

    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type' : 'application/json'
    }

    try:
        response = requests.get(taiga_api_url, headers= headers)
        response.raise_for_status()

        milestone_info = response.json()

        return milestone_info
    
    except requests.exceptions.RequestException as e:
        print(f'Error fetching milestones:{e}')
        return None



