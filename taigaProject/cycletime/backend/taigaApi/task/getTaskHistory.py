from datetime import datetime
import os
import requests
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

class TaskHistoryError(Exception):
    def __init__(self, status_code, reason):
        self.status_code = status_code
        self.reason = reason


def get_cycle_time(task, auth_token):
    cycle_time = 0
    taiga_url = os.getenv('TAIGA_URL')
    finished_date = task['finished_date']
    task_id = task.get('id')
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json'
    }

    task_history_url = f"{taiga_url}/history/task/{task_id}"

    try:
        response = requests.get(task_history_url, headers=headers)
        response.raise_for_status()
        history_data = response.json()

        # print("historydata----------------", history_data)

        in_progress_date = extract_new_to_in_progress_date(history_data)

        finished_date = datetime.fromisoformat(finished_date[:-1])

        if in_progress_date:
            in_progress_date = datetime.fromisoformat(str(in_progress_date)[:-6])

            cycle_time += (finished_date - in_progress_date).days
   
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error fetching Task History: {e}")
        raise TaskHistoryError(e.response.status_code, e.response.reason)

    except requests.exceptions.ConnectionError as e:
        print(f"Connection error fetching Task History: {e}")
        raise TaskHistoryError("CONNECTION_ERROR", str(e))

    except Exception as e:
        print(f"Unexpected error while Calculating Cycle Time:{e}")
        raise 

    return cycle_time

# Function to extract the date when a task transitioned from 'New' to 'In progress'
def extract_new_to_in_progress_date(history_data):
    for event in history_data:
        values_diff = event.get("values_diff", {})
        if "status" in values_diff and values_diff["status"] == ["New", "In progress"]:
            created_at = datetime.fromisoformat(event["created_at"])
            return created_at
    return None

