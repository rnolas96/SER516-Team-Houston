from datetime import datetime, timedelta
from itertools import groupby
from taigaApi.task.getTasks import get_closed_tasks_for_sprint, get_closed_tasks
from taigaApi.task.getTaskHistory import get_task_history

#function to calculate average cycle time for tasks which belong to a specific sprint
def get_cycle_time_by_sprint_id(sprint_id, project_id, auth_token):

    closed_sprint_tasks = get_closed_tasks_for_sprint(sprint_id, project_id, auth_token)
    cycle_time, closed_task = get_task_history(closed_sprint_tasks, auth_token)
    avg_cycle_time = round((cycle_time / closed_task), 2)

    return avg_cycle_time


# Function to calculate and display  sprintwise average cycle time
def get_sprintwise_cycle_time(project_id, auth_token):
    result={}
    tasks = get_closed_tasks(project_id, auth_token)

    # sort the tasks milestone wise
    tasks.sort(key=lambda x: x["milestone_slug"])
    for key, group in groupby(tasks, key=lambda x: x["milestone_slug"]):
        cycle_time, closed_task = get_task_history(list(group), auth_token)
        avg_cycle_time = round((cycle_time / closed_task), 2)
        result[str(key)] = avg_cycle_time

    return result

#function to get lead time for each sprint.        
def get_sprintwise_lead_time(project_id, auth_token):
    result={}
    tasks = get_closed_tasks(project_id, auth_token)
    # sort the tasks milestone wise
    tasks.sort(key=lambda x: x["milestone_slug"])
    
    for key, group in groupby(tasks, key=lambda x: x["milestone_slug"]):
        milestone=""
        lead_time = 0
        closed_tasks = 0
        for task in list(group):
            created_date = datetime.fromisoformat(task["created_date"])
            finished_date = datetime.fromisoformat(task['finished_date'])
        
            lead_time += (finished_date - created_date).days
            closed_tasks += 1
            milestone = str(task["milestone_slug"])

        avg_lead_time = round((lead_time / closed_tasks), 2)
        result[milestone] = avg_lead_time
    return result