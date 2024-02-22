from datetime import datetime, timedelta
from itertools import groupby
from taigaApi.task.getTasks import TaskFetchingError, get_closed_tasks_for_sprint, get_closed_tasks, get_tasks, get_all_tasks, get_tasks_by_milestone
from taigaApi.task.getTaskHistory import get_task_history
from taigaProject.backend.taigaApi.milestone.getMilestoneById import MilestoneFetchingError, get_milestone_by_id

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
        cumulative_difference = ideal_story_points_per_day

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
                            cumulative_difference -= task_points


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