from itertools import groupby
from taigaApi.task.getTasks import get_closed_tasks_for_sprint, get_closed_tasks, get_all_tasks
from taigaApi.task.getTaskHistory import get_task_history


def get_sprintwise_task_count(sprint_id, project_id, auth_token):
    sprintwise_task_count = {}

    tasks = get_all_tasks(project_id, auth_token)

    for task in tasks:
        sprint_id = task.get("milestone")

        if sprint_id is not None:
            sprint_task_count = sprintwise_task_count.get(sprint_id)
            
            if sprint_task_count is not None:
                sprintwise_task_count[sprint_id] = sprint_task_count + 1
            else:
                sprintwise_task_count[sprint_id] = 1

    for task in tasks:
        sprint_id = task.get("milestone")

        closed_task = get_closed_tasks_for_sprint(sprint_id)

        sprintwise_task_count[sprint_id] = sprintwise_task_count[sprint_id] - len(closed_task)

    return sprintwise_task_count

#Function to calculate average cycle time for tasks which belong to a specific sprint
def get_cycle_time_by_sprint_id(sprint_id, project_id, auth_token):

    closed_sprint_tasks = get_closed_tasks_for_sprint(sprint_id, project_id, auth_token)
    cycle_time, closed_task = get_task_history(closed_sprint_tasks, auth_token)
    avg_cycle_time = round((cycle_time / closed_task), 2)

    return avg_cycle_time

# Function to calculate and display sprintwise average cycle time
def get_sprintwise_cycle_time(project_id, auth_token):
    tasks = get_closed_tasks(project_id, auth_token)

    # Sort the tasks milestone wise
    tasks.sort(key=lambda x: x["milestone_slug"])
    for key, group in groupby(tasks, key=lambda x: x["milestone_slug"]):
        result ={ }
        cycle_time, closed_task = get_task_history(list(group), auth_token)
        avg_cycle_time = round((cycle_time / closed_task), 2)

        milestone_slug_split = str(key).split('-')
        result["sprint" + milestone_slug_split[1]] = avg_cycle_time

    return result
        

