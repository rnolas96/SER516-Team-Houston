import datetime
import json
import threading
import redis

from taigaApi.milestone.get_milestone_name import MilestoneFetchingError, get_milestone_name
from taigaApi.task.getTaskHistory import get_cycle_time
from taigaApi.task.getTasks import TaskFetchingError, get_closed_tasks


#r_task = redis.StrictRedis(host='redis-container-prod', port=6379, db=1)
r_task = None

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
                task_response.append({
                    "task_id": closed_task.get("id"),
                    "cycle_time": get_cycle_time(closed_task, auth_token)
                })

                closed_tasks_response[sprint_name] = task_response 
            else:
                closed_tasks_response[sprint_name] = [{
                    "task_id": closed_task.get("id"),
                    "cycle_time": get_cycle_time(closed_task, auth_token)
                }]

        return closed_tasks_response

    return {}

def get_cycle_time_for_date_range(project_id, start_date, end_date, auth_token):
    """
    Description
    -----------
    Gets the user_story storypoint burndown based on the sprint_id.

    Arguments
    ---------
    sprint_id, auth_token

    Returns
    -------
    A map of date and remaining story points value for every day until end of the sprint.
    """

    response = {}
    try:
        cycle_time_redis_id = str(project_id) + '_' + start_date + '_' + end_date
        serialized_cached_data = r_task.get(f'cycle_time_data_for_date_range:{cycle_time_redis_id}')
        if serialized_cached_data:

            background_thread = threading.Thread(target=get_task_cycle_time_time_range, args=(project_id, start_date, end_date, auth_token))
            background_thread.start()
                    
            response = json.loads(serialized_cached_data)

            return response
        
        response = get_task_cycle_time_time_range(project_id, start_date, end_date, auth_token)
        return response
    
    except TaskFetchingError as e:
        print(f"Error fetching Tasks: {e}")
        return None
         
    except MilestoneFetchingError as e:
        print(f"Error fetching Milestones: {e}")
        return None
    
    except Exception as e :
        print(f"Unexpected error :{e}")
        return None

def get_task_cycle_time_time_range(project_id, start_date, end_date, auth_token):
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

                if closed_tasks_response.get("range_cycle_time") is not None:
                    task_response = closed_tasks_response.get("range_cycle_time")

                    task_response.append({
                        "task_id": closed_task.get("id"),
                        "cycle_time": get_cycle_time(closed_task, auth_token)
                    })

                    closed_tasks_response["range_cycle_time"] = task_response 
                else:
                    closed_tasks_response["range_cycle_time"] = [{
                        "task_id": closed_task.get("id"),
                        "cycle_time": get_cycle_time(closed_task, auth_token)
                    }]

        serialized_response = json.dumps(closed_tasks_response)
        serialized_cached_data = r_task.get(f'cycle_time_data_for_date_range:{project_id}:{start_date}:{end_date}')

        if serialized_cached_data != serialized_response:
            cycle_time_redis_id = str(project_id) + '_' + start_date + '_' + end_date
            r_task.set(f'cycle_time_data_for_date_range:{cycle_time_redis_id}', serialized_response)

        return closed_tasks_response

    return {}

