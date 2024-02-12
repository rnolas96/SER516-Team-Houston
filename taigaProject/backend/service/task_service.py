from datetime import datetime, timedelta
from itertools import groupby
from taigaApi.task.getTasks import get_closed_tasks_for_sprint, get_closed_tasks, get_tasks, get_all_tasks
from taigaApi.task.getTaskHistory import get_task_history

# Function to get the number of open task for each sprint
def get_sprintwise_task_count(project_id, auth_token):
    sprintwise_task_count = {}
    sprintwise_closed_tasks_count = {}
    sprintwise_open_task_count = {}

    tasks = get_all_tasks(project_id, auth_token)

    for task in tasks:
        sprint_id = task.get("milestone")
        sprint_name = task.get("milestone_slug")

        if sprint_id is not None:
            if sprintwise_task_count.get(sprint_name) is None:
                sprintwise_task_count[sprint_name] = 1
            else:
                sprintwise_task_count[sprint_name] += 1

            closed_tasks = get_closed_tasks_for_sprint(sprint_id, project_id, auth_token)
            sprintwise_closed_tasks_count[sprint_name] = len(closed_tasks)

    for task_count in sprintwise_task_count.keys():
        sprintwise_open_task_count[task_count] = sprintwise_task_count[task_count] - sprintwise_closed_tasks_count[task_count]
        
    return sprintwise_open_task_count

#F unction to calculate average cycle time for tasks which belong to a specific sprint
def get_cycle_time_by_sprint_id(sprint_id, project_id, auth_token):

    closed_sprint_tasks = get_closed_tasks_for_sprint(sprint_id, project_id, auth_token)
    cycle_time, closed_task = get_task_history(closed_sprint_tasks, auth_token)
    avg_cycle_time = round((cycle_time / closed_task), 2)

    return avg_cycle_time

# Function to calculate and display sprintwise average cycle time
def get_sprintwise_cycle_time(project_id, auth_token):
    result={}
    tasks = get_closed_tasks(project_id, auth_token)

    # Sort the tasks milestone wise
    tasks.sort(key=lambda x: x["milestone_slug"])
    # group by milestone_slug
    for key, group in groupby(tasks, key=lambda x: x["milestone_slug"]):
        cycle_time, closed_task = get_task_history(list(group), auth_token)

        if closed_task > 0:
            avg_cycle_time = round((cycle_time / closed_task), 2)
        else:
            avg_cycle_time = None  
            
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
        
        if closed_tasks > 0:
            avg_lead_time = round((lead_time / closed_tasks), 2)
        else:
            avg_lead_time = None  
        result[milestone] = avg_lead_time
    return result
