from datetime import datetime, timedelta
from itertools import groupby
from taigaApi.task.getTasks import get_closed_tasks, get_all_tasks
from taigaApi.task.getTaskHistory import get_lead_time

def get_sprintwise_task_lead_time(project_id, auth_token):
    closed_tasks = get_closed_tasks(project_id, auth_token)
    closed_tasks_response = {}

    if closed_tasks is not None:
        for closed_task in closed_tasks:
            sprint_id = closed_task.get("milestone_id")

            if closed_tasks_response.get(sprint_id) is not None:
                task_response = closed_tasks_response.get(sprint_id)
                task_response.append(
                    {
                        "task_id": closed_task.get("id"),
                        "lead_time": get_lead_time(closed_task, auth_token)
                        }
                )

                closed_tasks_response[sprint_id] = task_response 
            else:
                closed_tasks_response[sprint_id] = [{
                    "task_id": closed_task.get("id"),
                     "lead_time": get_lead_time(closed_task, auth_token)
                }]

        return closed_tasks_response

    return {}