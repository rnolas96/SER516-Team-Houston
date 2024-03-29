from datetime import datetime, timedelta
from itertools import groupby
import logging
import re
from taigaApi.task.getTasks import TaskFetchingError, get_closed_tasks,  get_custom_attribute_values_from_task, get_milestone_name, get_task_custom_attribute_type_id, get_tasks_by_milestone, get_tasks
from taigaApi.task.getTaskHistory import get_cycle_time, get_lead_time
from taigaApi.milestone.getMilestoneById import MilestoneFetchingError, get_milestone_by_id
from taigaApi.issue.getIssuesByProjectId import get_issues_by_project_id
from taigaApi.issue.getCustomAttributeValueByIssueId import get_custom_attribute_value_by_issue_id, get_custom_attribute_type_id_for_issue
from taigaApi.userStory.getUserStory import get_userstories_by_sprint, get_custom_attribute_from_userstory, get_custom_attribute_type_id
from taigaApi.issue.getIssuesByProjectId import get_issues_by_project_id
from taigaApi.issue.getCustomAttributeValueByIssueId import get_custom_attribute_value_by_issue_id, get_custom_attribute_type_id_for_issue
from taigaApi.userStory.getUserStory import get_userstories_by_sprint, get_custom_attribute_from_userstory, get_custom_attribute_type_id
import threading
import redis
import json

r_task = redis.StrictRedis(host='redis-container-prod', port=6379, db=1)

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
    

def get_cost_of_delay_for_sprint(project_id, sprint_id, business_value_cost_factor, auth_token):
     
    issue_list = get_issues_by_project_id(project_id, auth_token)

    sprint_issue_list = []

    for issue in issue_list :
        if issue['milestone'] == sprint_id :
            sprint_issue_list.append(issue)

    response_userstory = {}
    response_business_value = {}
    response_cost_of_delay = {}

    sprint_data = get_milestone_by_id(sprint_id, auth_token)

    response_userstory["0"] = 0
    response_business_value["0"] = 0
    response_cost_of_delay["0"] = 0

    start_date = sprint_data['estimated_start']
    end_date = sprint_data['estimated_finish']

    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    for date in range((end_date - start_date).days+1):
        current_date = start_date+timedelta(days = date)
        response_userstory[current_date.strftime("%Y-%m-%d")] = 0
        response_business_value[current_date.strftime("%Y-%m-%d")] = 0
        response_cost_of_delay[current_date.strftime("%Y-%m-%d")] = 0

    custom_attribute_type_id = get_custom_attribute_type_id_for_issue(project_id, auth_token, "blocked")

    dependencies = {}
    issue_data = {}

    issue_date_map = {}

    for issue in sprint_issue_list :
        issue_id = issue['id']
        issue_date_map[issue_id] = {}
        issue_date_map[issue_id]['created_date'] = issue['created_date']
        issue_date_map[issue_id]['finished_date'] = issue['finished_date']

        custom_attribute_value_for_issue = get_custom_attribute_value_by_issue_id(issue_id, custom_attribute_type_id, auth_token)
        issue_data[issue_id] = issue
        issue_dependency_story_list = [x.strip() for x in custom_attribute_value_for_issue.split(',')] 
        dependencies[issue_id] = issue_dependency_story_list

    userstory_ref_map={}

    user_stories = get_userstories_by_sprint(sprint_id, auth_token)
    if user_stories and len(user_stories)>0 :
        for userstory in user_stories :
            userstory_ref = '#' + str(userstory['ref'])
            userstory_ref_map[userstory_ref] = userstory

    userstory_blocker_map = {}

    for dependency_key, dependency_value in dependencies.items() :
        for userstory_label in dependency_value :
            if userstory_label in userstory_ref_map:
                userstory = userstory_ref_map[userstory_label]
                userstory_id = userstory['id']
                
                if userstory_id in userstory_blocker_map :
                    userstory_blocker_map[userstory_label]['blocked_start_date'] = min(userstory_blocker_map[userstory_label]['blocked_start_date'], issue_date_map[dependency_key]['created_date'])
                    if issue_date_map[dependency_key]['finished_date'] != None :
                        userstory_blocker_map[userstory_label]['blocked_end_date'] = max(userstory_blocker_map[userstory_label]['blocked_end_date'], issue_date_map[dependency_key]['finished_date'])
                    else :
                        userstory_blocker_map[userstory_label]['blocked_end_date'] = None
                else :
                    userstory_blocker_map[userstory_label] = {}
                    userstory_blocker_map[userstory_label]['blocked_start_date'] = issue_date_map[dependency_key]['created_date']
                    userstory_blocker_map[userstory_label]['blocked_end_date'] = issue_date_map[dependency_key]['finished_date']

    for userstory_key, userstory_value in userstory_blocker_map.items() :
        userstory = userstory_ref_map[userstory_key]
        userstory_id = userstory['id']
        
        if userstory_value['blocked_start_date'] > sprint_data['estimated_start'] :
            custom_attribute_data = get_custom_attribute_from_userstory(userstory_id, auth_token)
            custom_attribute_type_id = get_custom_attribute_type_id(project_id, auth_token, "Business Value")

            issue_start_date = userstory_value['blocked_start_date']
            issue_end_date = userstory_value['blocked_end_date']
            issue_start_date = datetime.strptime(issue_start_date,"%Y-%m-%dT%H:%M:%S.%fZ")
            if issue_end_date != None :
                issue_end_date = datetime.strptime(issue_end_date,"%Y-%m-%dT%H:%M:%S.%fZ")

            if 'total_points' in userstory and userstory['total_points'] != None:
                response_userstory[issue_start_date.strftime("%Y-%m-%d")] += int(userstory['total_points'])
                if issue_end_date != None :
                    response_userstory[issue_end_date.strftime("%Y-%m-%d")] -= int(userstory['total_points'])
            if custom_attribute_type_id in custom_attribute_data and custom_attribute_data[custom_attribute_type_id] != None:
                response_business_value[issue_start_date.strftime("%Y-%m-%d")] += int(custom_attribute_data[custom_attribute_type_id])
                if issue_end_date != None :
                    response_business_value[issue_end_date.strftime("%Y-%m-%d")] -= int(custom_attribute_data[custom_attribute_type_id])

    response_prev = "0"
    for response_userstory_key, response_userstory_value in response_userstory.items():
        if response_userstory_key != "0":
            response_userstory[response_userstory_key] += response_userstory[response_prev]
            response_business_value[response_userstory_key] += response_business_value[response_prev]
            response_cost_of_delay[response_userstory_key] += ((business_value_cost_factor * response_business_value[response_userstory_key]) + response_cost_of_delay[response_prev])
            response_prev = response_userstory_key

    response = {}

    response['userstory'] = response_userstory
    response['business_value'] = response_business_value
    response['cost_of_delay'] = response_cost_of_delay

    return response


def get_task_coupling(project_id, auth_token):
    result = {}
    task_ref_map={}

    tasks = []
    nodes = []
    edges = []

    try:
        custom_attribute_name = "DependsOn"
        
        tasks = get_tasks(project_id, auth_token)
        custom_attribute_type_id = get_task_custom_attribute_type_id(project_id, auth_token, custom_attribute_name)

        if tasks and len(tasks)>0:
            for task in tasks:
                task_ref_map[task['ref']] = task['id']

            for task in tasks:
                task_obj={}
                task_obj['id'] = task['id']
                task_obj['label'] = task['ref']
                task_obj['title'] = task['subject']
                nodes.append(task_obj)

                logging.info(f"task id :{task['id']}")         
                logging.info(f"task subject :{task['subject']}")               
      
                depends_on_values=[]
                custom_attribute_data = get_custom_attribute_values_from_task(task['id'], auth_token)

                logging.info(f"custom attribute data : {custom_attribute_data}")
                logging.info(f"custom attribute type id : {custom_attribute_type_id}")


                if(custom_attribute_type_id in custom_attribute_data):
                    depends_on_str = custom_attribute_data[custom_attribute_type_id]
                    depends_on_values = re.findall(r"#(\d+)", depends_on_str)

                for depends_on in depends_on_values:
                    edge = {}
                    edge['from'] = task['id']
                    edge['to'] = task_ref_map[int(depends_on)]
                    edges.append(edge)
                
        result['nodes'] = nodes
        result['edges'] = edges
        return result

    except TaskFetchingError as e:
            print("Error fetching tasks: {e}")
            return None

    except Exception as e:
        print("Unexpected error calculating cost:")
        return None


