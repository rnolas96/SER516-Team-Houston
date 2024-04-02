# Function to calculate  lead time for tasks which belong to a specific sprint
from taigaApi.task.getTaskHistory import get_lead_time
from taigaApi.task.getTasks import get_closed_tasks, get_milestone_name

import datetime

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
                task_response.append({
                    "task_id": closed_task.get("id"),
                    "lead_time": get_lead_time(closed_task, auth_token)
                })

                closed_tasks_response[sprint_name] = task_response 
            else:
                closed_tasks_response[sprint_name] = [{
                    "task_id": closed_task.get("id"),
                     "lead_time": get_lead_time(closed_task, auth_token)
                }]

        return closed_tasks_response
    return {}

def get_task_lead_time_time_range(project_id, start_date, end_date, auth_token):
    closed_tasks = get_closed_tasks(project_id, auth_token)
    closed_tasks_response = {}

    if closed_tasks is not None:
        for closed_task in closed_tasks:
            print("start_date - ", start_date, "     end_date - ", end_date, "        finished date for task - ", closed_task['finished_date'])
            
            modified_start_date = datetime.strptime(start_date, "%Y-%m-%d")
            modified_end_date = datetime.strptime(end_date, "%Y-%m-%d")

            task_finished_date = datetime.strptime(closed_task['finished_date'], "%Y-%m-%dT%H:%M:%S.%fZ")

            print("dates to compare", modified_start_date, task_finished_date, modified_end_date)

            if task_finished_date >= modified_start_date and task_finished_date <= modified_end_date:
                
                print('finished_date for each closed task', task_finished_date)

                if closed_tasks_response.get("range_lead_time") is not None:
                    task_response = closed_tasks_response.get("range_lead_time")

                    task_response.append({
                        "task_id": closed_task.get("id"),
                        "lead_time": get_lead_time(closed_task, auth_token)
                    })

                    closed_tasks_response["range_lead_time"] = task_response 
                else:
                    closed_tasks_response["range_lead_time"] = [{
                        "task_id": closed_task.get("id"),
                        "lead_time": get_lead_time(closed_task, auth_token)
                    }]

        print("length of final list", len(closed_tasks_response["range_lead_time"]))
        return closed_tasks_response

    return {}
