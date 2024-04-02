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


def get_lead_time(task, auth_token):
    finished_date = task['finished_date']
    creation_date = task['created_date']
    
    finished_date = datetime.fromisoformat(finished_date[: -1])
    creation_date = datetime.fromisoformat(creation_date[: -1])

    lead_time = (finished_date - creation_date).days

    return lead_time
# Function to extract the date when a task transitioned from 'New' to 'In progress'
def extract_new_to_in_progress_date(history_data):
    for event in history_data:
        values_diff = event.get("values_diff", {})
        if "status" in values_diff and values_diff["status"] == ["New", "In progress"]:
            created_at = datetime.fromisoformat(event["created_at"])
            return created_at
    return None

