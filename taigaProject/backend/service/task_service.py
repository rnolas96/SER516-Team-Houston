from itertools import groupby
from taigaApi.task.getTasks import get_closed_tasks, get_all_tasks
from taigaApi.task.getTaskHistory import get_cycle_time

# Function to get the number of open task for each sprint
# def get_sprintwise_task_count(project_id, auth_token):
#     sprintwise_task_count = {}
#     sprintwise_closed_tasks_count = {}
#     sprintwise_open_task_count = {}

#     tasks = get_all_tasks(project_id, auth_token)

#     for task in tasks:
#         sprint_id = task.get("milestone")
#         sprint_name = task.get("milestone_slug")

#         if sprint_id is not None:
#             if sprintwise_task_count.get(sprint_name) is None:
#                 sprintwise_task_count[sprint_name] = 1
#             else:
#                 sprintwise_task_count[sprint_name] += 1

#             closed_tasks = get_closed_tasks_for_sprint(sprint_id, project_id, auth_token)
#             sprintwise_closed_tasks_count[sprint_name] = len(closed_tasks)

#     for task_count in sprintwise_task_count.keys():
#         sprintwise_open_task_count[task_count] = sprintwise_task_count[task_count] - sprintwise_closed_tasks_count[task_count]
        
#     return sprintwise_open_task_count

# Function to calculate  cycle time for tasks which belong to a specific sprint
def get_sprintwise_task_cycle_time(project_id, auth_token):
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
                        "cycle_time": get_cycle_time(closed_task, auth_token)
                        }
                )

                closed_tasks_response[sprint_id] = task_response 
            else:
                closed_tasks_response[sprint_id] = [{
                    "task_id": closed_task.get("id"),
                     "cycle_time": get_cycle_time(closed_task, auth_token)
                }]

        return closed_tasks_response

    return {}
