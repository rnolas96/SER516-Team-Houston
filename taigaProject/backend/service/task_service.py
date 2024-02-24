from datetime import datetime, timedelta
from itertools import groupby
from taigaApi.task.getTasks import TaskFetchingError, get_closed_tasks, get_milestone_name, get_tasks_by_milestone
from taigaApi.task.getTaskHistory import get_cycle_time, get_lead_time
from taigaApi.milestone.getMilestoneById import MilestoneFetchingError, get_milestone_by_id



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

# Function to calculate  lead time for tasks which belong to a specific sprint
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

def get_cost_of_delay_for_tasks(sprint_id, auth_token):
    user_stories = []
    story_point_map = {}
    user_story_task_count_map = {}
    result = {'ideal_points':[], 'actual_points':[], 'cumulative_difference':[],'date':[]}

    try:
        #fetch sprint data
        sprint_data = get_milestone_by_id(sprint_id, auth_token)

        if sprint_data and len(sprint_data) > 1 :

            # filter user stories
            user_stories = sprint_data.get('user_stories', [])
            total_points_for_sprint = sprint_data.get('total_points',0)
            start_date = datetime.strptime(sprint_data['estimated_start'],"%Y-%m-%d")
            end_date =  datetime.strptime(sprint_data['estimated_finish'],"%Y-%m-%d")

            # map userstory with storypoints
            if user_stories and len(user_stories) > 1:
                for userstory in user_stories:
                    story_point_map[userstory['id']] = userstory['total_points']

        # fetch tasks
        tasks = get_tasks_by_milestone(sprint_data['project'],sprint_id, auth_token)

        if tasks and len(tasks)>1:
                for task in tasks:
                    if(task['user_story']):
                        userstory_id = task['user_story'] 

                        # map user story and count of tasks for that userstory
                        if userstory_id in user_story_task_count_map:
                            user_story_task_count_map[userstory_id]+=1

                        else:
                            user_story_task_count_map[userstory_id] = 1

        sprint_duration = (end_date - start_date).days + 1
        ideal_story_points_per_day = total_points_for_sprint/sprint_duration
        ideal_points_for_the_day = 0
        total_running_sum=0

        for date in range((end_date - start_date).days+1):
            ideal_points_for_the_day += ideal_story_points_per_day
            current_date = start_date+timedelta(days = date)
            total_points_for_the_day = 0

            if tasks and len(tasks)>1:
                for task in tasks:

                    if task['user_story'] :
                        userstory_id = task['user_story'] 

                        if task['is_closed'] and  datetime.fromisoformat(task["finished_date"].split("T")[0])==current_date:

                            total_userstory_points = story_point_map[userstory_id]
                            total_task_count = user_story_task_count_map[userstory_id]
                            task_points = (total_userstory_points / total_task_count)
                            total_points_for_the_day += task_points
           
            total_running_sum += total_points_for_the_day
            cumulative_difference= ideal_points_for_the_day - total_running_sum 
                            


            result['actual_points'].append(total_points_for_the_day)
            result['ideal_points'].append(ideal_points_for_the_day)
            result['cumulative_difference'].append(cumulative_difference)
            result['date'].append(current_date)

        return result

    except TaskFetchingError as e:
        print("Error fetching tasks: {e}")
        return None

    except MilestoneFetchingError as e:
        print(f"Error fetching milestones: {e}")
        return None  

    except Exception as e:
        print("Unexpected error calculating cost:")
        return None