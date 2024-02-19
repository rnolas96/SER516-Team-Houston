from datetime import datetime, timedelta
from itertools import groupby
from taigaApi.task.getTasks import get_closed_tasks, get_milestone_name
from taigaApi.task.getTaskHistory import get_cycle_time, get_lead_time



# Function to calculate  cycle time for tasks which belong to a specific sprint
def get_sprintwise_task_cycle_time(project_id, auth_token):
    closed_tasks = get_closed_tasks(project_id, auth_token)
    milestones_name = get_milestone_name(project_id, auth_token)

    closed_tasks_response = {}

    if closed_tasks is not None:
        for closed_task in closed_tasks:
            sprint_id = closed_task.get("milestone_id")
            sprint_name = milestones_name.get(sprint_id)

            if closed_tasks_response.get(sprint_name) is not None:
                task_response = closed_tasks_response.get(sprint_name)
                task_response.append(
                    {
                        "task_id": closed_task.get("id"),
                        "cycle_time": get_cycle_time(closed_task, auth_token)
                        }
                )

                closed_tasks_response[sprint_name] = task_response 
            else:
                closed_tasks_response[sprint_name] = [{
                    "task_id": closed_task.get("id"),
                     "cycle_time": get_cycle_time(closed_task, auth_token)
                }]

        return closed_tasks_response

    return {}
  
  def get_sprintwise_task_lead_time(project_id, auth_token):
    closed_tasks = get_closed_tasks(project_id, auth_token)
    closed_tasks_response = {}

    milestones_name = get_milestone_name(project_id, auth_token)

    if closed_tasks is not None:
        for closed_task in closed_tasks:
            sprint_id = closed_task.get("milestone_id")
            sprint_name = milestones_name[sprint_id]

            if closed_tasks_response.get(sprint_name) is not None:
                task_response = closed_tasks_response.get(sprint_name)
                task_response.append(
                    {
                        "task_id": closed_task.get("id"),
                        "lead_time": get_lead_time(closed_task, auth_token)
                        }
                )

                closed_tasks_response[sprint_name] = task_response 
            else:
                closed_tasks_response[sprint_name] = [{
                    "task_id": closed_task.get("id"),
                     "lead_time": get_lead_time(closed_task, auth_token)
                }]

        return closed_tasks_response

    return {}