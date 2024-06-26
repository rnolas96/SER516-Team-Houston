import re
import json
import redis
import logging
from datetime import datetime, date, timedelta
import threading
from fastapi import HTTPException
from datetime import datetime, timedelta
from taigaApi.task.getTasks import get_tasks_by_milestone
from taigaApi.milestone.getMilestoneByProjectId import get_milestone_by_project_id
from taigaApi.milestone.getMilestoneById import get_milestone_by_id, MilestoneFetchingError
from taigaApi.userStory.getUserStory import get_custom_attribute_from_userstory, get_custom_attribute_type_id, get_user_story, UserStoryFetchingError, get_userstories_by_sprint, get_closed_tasks_per_user_story, get_userstory_total_points, get_task_per_user_story

r_userstory = redis.StrictRedis(host='redis-container-burndown', port=6379, db=0)

print("redis cache connected", r_userstory)

# funtion to get sprintwise burndown chart details for a project. 
def get_userstory_burndown_by_project_id(project_id,auth_token):
    response=[]
    
    user_stories = get_user_story(project_id, auth_token)
    total_story_points = 0

    user_stories_map = {}
    for user_story in user_stories: 
        if(user_story['milestone_name']):
            sprint = user_story['milestone_name']
            if(user_story['total_points']):
                user_stories_map[str(sprint)] = user_story['total_points']
                total_story_points += user_story['total_points']
            else:
                user_stories_map[str(sprint)] = 0

    sprint_story_points_map ={}

    sprint_story_points_map['total_points']=total_story_points
    for key,val in user_stories_map.items():
        sprint_story_points_map[key] = total_story_points-val

        total_story_points -= val

    response.append(sprint_story_points_map)
    return response

def get_storypoint_burndown_for_sprint(sprint_id, auth_token):
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
    # r_userstory.flushdb()

    response = {}
    try:
        print("stored redis key",  r_userstory.get(f'userstory_full_storypoint_data:{sprint_id}'))    

        serialized_cached_data = r_userstory.get(f'userstory_full_storypoint_data:{sprint_id}')
        if serialized_cached_data:

            background_thread = threading.Thread(target=storypoint_burndown_for_sprint_process, args=(sprint_id, auth_token))
            background_thread.start()
                    
            response = json.loads(serialized_cached_data)

            return response
        
        response = storypoint_burndown_for_sprint_process(sprint_id, auth_token)
        return response
    except UserStoryFetchingError as e:
        print(f"Error fetching UserStories: {e}")
        return None
         
    except MilestoneFetchingError as e:
        print(f"Error fetching Milestones: {e}")
        return None
    except Exception as e :
        print(f"Unexpected error :{e}")
        return None

def storypoint_burndown_for_sprint_process(sprint_id, auth_token):
    #get sprint info 
    sprint_data = get_milestone_by_id(sprint_id, auth_token)
    user_stories = sprint_data['user_stories']
    total_story_points = sprint_data['total_points'] 

    start_date = datetime.strptime(sprint_data['estimated_start'],"%Y-%m-%d")
    end_date =  datetime.strptime(sprint_data['estimated_finish'],"%Y-%m-%d")
    result={}
    date_storypoint_map={}

    for user_story in user_stories:
        if user_story['is_closed']:
                
            if user_story['finish_date']  :
                    
                finish_date = datetime.strptime(user_story['finish_date'],"%Y-%m-%dT%H:%M:%S.%fZ")
                finish_date = finish_date.strftime("%Y-%m-%d")

                if(finish_date in date_storypoint_map):
                    date_storypoint_map[finish_date] += user_story['total_points']
                else:
                    date_storypoint_map[finish_date] = user_story['total_points']

    for date in range((end_date - start_date).days+1):
       
        current_date = start_date+timedelta(days = date)
        if current_date.strftime('%Y-%m-%d') in date_storypoint_map:
            total_story_points -= date_storypoint_map[current_date.strftime('%Y-%m-%d')]
        result[current_date.strftime("%Y-%m-%d")] = total_story_points

    serialized_response = json.dumps(result)
    serialized_cached_data = r_userstory.get(f'userstory_full_storypoint_data:{sprint_id}')


    if serialized_cached_data != serialized_response:
            r_userstory.set(f'userstory_full_storypoint_data:{sprint_id}', serialized_response) 
            print("stored redis key",  r_userstory.get(f'userstory_full_storypoint_data:{sprint_id}'))    

    return result


def get_userstory_custom_attribute_burndown_for_sprint(project_id, sprint_id, auth_token, custom_attribute_name):
    """
    Description
    -----------
    Gets the user_story based on the project_id, filters it based on the sprint_id
    and uses the custom_attribute to get back the custom_attribute_values

    Arguments
    ---------
    project_id, print_id, auth_token, custom_attribute_name

    Returns
    -------
    A map of date and business value completed.
    """
    try:
        response = {}
        
        serialized_cached_data = r_userstory.get(f'userstory_business_value_data:{sprint_id}')
        if serialized_cached_data:

            background_thread = threading.Thread(target=userstory_custom_attribute_burndown_for_sprint_process, args=(project_id, sprint_id, auth_token, custom_attribute_name))
            background_thread.start()
                    
            response = json.loads(serialized_cached_data)

            return response
        
        response = userstory_custom_attribute_burndown_for_sprint_process(project_id, sprint_id, auth_token, custom_attribute_name)
        return response
    except:
        raise HTTPException(status_code=401, detail="Missing custom attribute")
    
def userstory_custom_attribute_burndown_for_sprint_process(project_id, sprint_id, auth_token, custom_attribute_name):

    response = {}

    sprint_data = get_milestone_by_id(sprint_id, auth_token)
    user_stories = sprint_data['user_stories']

    if not user_stories:
        return {}

    response["0"] = 0
    total_custom_attribute_value = 0

    start_date = sprint_data['estimated_start']
    end_date = sprint_data['estimated_finish']

    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    for date in range((end_date - start_date).days+1):
        current_date = start_date+timedelta(days = date)
        response[current_date.strftime("%Y-%m-%d")] = 0

    for user_story in user_stories:

        user_story_id = user_story['id']
        custom_attribute_data = get_custom_attribute_from_userstory(user_story_id, auth_token)
        custom_attribute_type_id = get_custom_attribute_type_id(project_id, auth_token, custom_attribute_name)
        total_custom_attribute_value += int(custom_attribute_data[custom_attribute_type_id])

        if user_story['is_closed'] and user_story['finish_date']:
            current_date = datetime.strptime(user_story['finish_date'],"%Y-%m-%dT%H:%M:%S.%fZ") 
            
            prepared_current_date = current_date.strftime("%Y-%m-%d")
            
            if prepared_current_date in response:
                response[prepared_current_date] += int(custom_attribute_data[custom_attribute_type_id])
            else:
                response[prepared_current_date] = int(custom_attribute_data[custom_attribute_type_id])

    response["0"] = total_custom_attribute_value

    response = dict(sorted(response.items()))

    temp = ""

    for res_key, res_val in response.items():
        if res_key != "0":
            temp=res_key
            response[res_key] = total_custom_attribute_value - response[res_key]
            total_custom_attribute_value = response[res_key]

    serialized_response = json.dumps(response)
    serialized_cached_data = r_userstory.get(f'userstory_business_value_data:{sprint_id}')


    if serialized_cached_data != serialized_response:
            r_userstory.set(f'userstory_business_value_data:{sprint_id}', serialized_response)
            print("stored redis key",  r_userstory.get(f'userstory_business_value_data:{sprint_id}'))    


    return response

def get_partial_storypoint_burndown_for_sprint(sprint_id, auth_token):
    """
    Description
    -----------
    Gets the partial story point burndown for a sprint
    Arguments
    ---------
    sprint_id auth_token
    Returns
    -------
    A map of date and partial storypoints value completed.
    """
    response = {}
    
    serialized_cached_data = r_userstory.get(f'userstory_partial_storypoint_data:{sprint_id}')
    if serialized_cached_data:

        background_thread = threading.Thread(target=partial_storypoint_burndown_for_sprint_process, args=(sprint_id, auth_token))
        background_thread.start()
                
        response = json.loads(serialized_cached_data)

        return response
    
    response = partial_storypoint_burndown_for_sprint_process(sprint_id, auth_token)
    return response

def partial_storypoint_burndown_for_sprint_process(sprint_id, auth_token):
    #get sprint info 
    sprint_data = get_milestone_by_id(sprint_id, auth_token)
    user_stories = sprint_data['user_stories']
    total_points_for_sprint = sprint_data['total_points'] 

    start_date = datetime.strptime(sprint_data['estimated_start'],"%Y-%m-%d")
    end_date =  datetime.strptime(sprint_data['estimated_finish'],"%Y-%m-%d")
    story_point_map ={}
    result={}
    tasks = get_tasks_by_milestone(sprint_data['project'],sprint_id, auth_token)

    user_story_task_count_map = {}

    # map userstory with storypoints
    for userstory in user_stories:
        story_point_map[userstory['id']]= userstory['total_points']

    # map userstoru with total task count 
    for task in tasks:
        if(task['user_story']):
            userstory_id = task['user_story'] 

            if userstory_id in user_story_task_count_map:
                user_story_task_count_map[userstory_id]+=1

            else:
               user_story_task_count_map[userstory_id] = 1


    #calculate burndown for every day from start to end of the sprint          
    for date in range((end_date - start_date).days+1):
        current_date = start_date+timedelta(days = date)

        partial_task_count_map={}

        # count the number of partial tasks for a user story
        for task in tasks:

            if(task['user_story']):
                userstory_id = task['user_story'] 

                if task['is_closed'] and  datetime.fromisoformat(task["finished_date"].split("T")[0])==current_date:

                    if userstory_id in partial_task_count_map:
                        partial_task_count_map[userstory_id]+=1

                    else:   
                        partial_task_count_map[userstory_id]=1

        # iterate through the partial task map and find the remaining points for the date           
        for key,partial_task_count in partial_task_count_map.items(): 

            total_task_count =  user_story_task_count_map[key]

            userstory_points = story_point_map[key]

            partial_story_points = (partial_task_count/total_task_count)*userstory_points

            total_points_for_sprint -= partial_story_points


        result[current_date.strftime("%Y-%m-%d")]= total_points_for_sprint

    serialized_response = json.dumps(result)
    serialized_cached_data = r_userstory.get(f'userstory_partial_storypoint_data:{sprint_id}')

    if serialized_cached_data != serialized_response:
            r_userstory.set(f'userstory_partial_storypoint_data:{sprint_id}', serialized_response)
            

    return result
    
def get_burndown_all_sprints(project_id, auth_token):
    """
    Description
    -----------
    Gets the full user story point burndown for multiple sprints
    ---------
    project_id auth_token
    Returns
    -------
    A map of date and  storypoints value completed.
    """   
    end_dates = []
    start_dates = []

    total_story_points = 0

    date_storypoint_map = {}
    result = {}
    milestones_response = get_milestone_by_project_id(project_id, auth_token)

    for milestone_item in milestones_response:

        end_date_obj = datetime.strptime(milestone_item['estimated_finish'], "%Y-%m-%d")
        start_date_obj = datetime.strptime(milestone_item['estimated_start'], "%Y-%m-%d")

        end_dates.append(end_date_obj)
        start_dates.append(start_date_obj)
        
        for userstory in milestone_item['user_stories']:
            total_story_points += userstory['total_points']

            if(userstory['is_closed']):
                if userstory['finish_date']  :
                    
                    finish_date = datetime.strptime(userstory['finish_date'],"%Y-%m-%dT%H:%M:%S.%fZ")
                    finish_date = finish_date.strftime("%Y-%m-%d")

                    if(finish_date in date_storypoint_map):
                        date_storypoint_map[finish_date] += userstory['total_points']
                    else:
                        date_storypoint_map[finish_date] = userstory['total_points']
                
        
    start_date = min(start_dates)

    end_date = max(end_dates)

    current_date = start_date

    while current_date < end_date:
        current_date += timedelta(days=1)    
        if current_date.strftime('%Y-%m-%d') in date_storypoint_map:
            total_story_points -= date_storypoint_map[current_date.strftime('%Y-%m-%d')]
        result[current_date.strftime("%Y-%m-%d")] = total_story_points
               

    return result

def get_business_value_burndown_for_all_sprints(project_id, custom_attribute_name, auth_token):
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
    # r_userstory.flushdb()

    response = {}
    try:
        serialized_cached_data = r_userstory.get(f'userstory_business_value_data_all_sprints:{project_id}')
        if serialized_cached_data:
            print("exists in cache")
            background_thread = threading.Thread(target=get_business_value_burndown_all_sprints, args=(project_id, custom_attribute_name, auth_token))
            background_thread.start()
                    
            response = json.loads(serialized_cached_data)

            return response
        print("does not exist in cache")
        response = get_business_value_burndown_all_sprints(project_id, custom_attribute_name, auth_token)
        return response
    except UserStoryFetchingError as e:
        print(f"Error fetching UserStories: {e}")
        return None
         
    except MilestoneFetchingError as e:
        print(f"Error fetching Milestones: {e}")
        return None
    except Exception as e :
        print(f"Unexpected error :{e}")
        return None

def get_business_value_burndown_all_sprints(project_id, custom_attribute_name, auth_token):
    """
    Description
    -----------
    Gets the full business value burndown for multiple sprints
    ---------
    project_id auth_token
    Returns
    -------
    A map of date and business value completed.
    """   
    end_dates = []
    start_dates = []

    total_custom_attribute_value = 0

    date_storypoint_map = {}
    result = {}
    milestones_response = get_milestone_by_project_id(project_id, auth_token)

    for milestone_item in milestones_response:

        end_date_obj = datetime.strptime(milestone_item['estimated_finish'], "%Y-%m-%d")
        start_date_obj = datetime.strptime(milestone_item['estimated_start'], "%Y-%m-%d")

        end_dates.append(end_date_obj)
        start_dates.append(start_date_obj)
        
        for userstory in milestone_item['user_stories']:

            user_story_id = userstory['id']
            custom_attribute_data = get_custom_attribute_from_userstory(user_story_id, auth_token)
            custom_attribute_type_id = get_custom_attribute_type_id(project_id, auth_token, custom_attribute_name)
            total_custom_attribute_value += int(custom_attribute_data[custom_attribute_type_id])

            if(userstory['is_closed']):
                if userstory['finish_date']  :
                    
                    finish_date = datetime.strptime(userstory['finish_date'],"%Y-%m-%dT%H:%M:%S.%fZ")
                    finish_date = finish_date.strftime("%Y-%m-%d")

                    if(finish_date in date_storypoint_map):
                        date_storypoint_map[finish_date] += int(custom_attribute_data[custom_attribute_type_id])
                    else:
                        date_storypoint_map[finish_date] = int(custom_attribute_data[custom_attribute_type_id])
                
        
    start_date = min(start_dates)

    end_date = max(end_dates)

    current_date = start_date

    while current_date < end_date:
        current_date += timedelta(days=1)    
        if current_date.strftime('%Y-%m-%d') in date_storypoint_map:
            total_custom_attribute_value -= date_storypoint_map[current_date.strftime('%Y-%m-%d')]
        result[current_date.strftime("%Y-%m-%d")] = total_custom_attribute_value
               
    serialized_response = json.dumps(result)
    serialized_cached_data = r_userstory.get(f'userstory_business_value_data_all_sprints:{project_id}')

    print("processing...")

    if serialized_cached_data != serialized_response:
            r_userstory.set(f'userstory_business_value_data_all_sprints:{project_id}', serialized_response)

    return result
    

def get_partial_sp(project_id, auth_token):
    """
    Get the partial story for a for each day

    Args:
        project_id (str): ID of the Taiga Project
        auth_token (str): Authorization Token of the Taiga User
    Return
        dict: Partial story points for each day
    """
    story_points = get_userstory_total_points(project_id, auth_token)
    closed_task_per_user_story = get_closed_tasks_per_user_story(project_id, auth_token)
    tasks_per_user_story = get_task_per_user_story(project_id, auth_token)
    milestones_response = get_milestone_by_project_id(project_id, auth_token)

    start_dates = []
    end_dates = []

    for milestone_item in milestones_response:
        end_date_obj = datetime.strptime(milestone_item['estimated_finish'], "%Y-%m-%d")
        start_date_obj = datetime.strptime(milestone_item['estimated_start'], "%Y-%m-%d")

        end_dates.append(end_date_obj)
        start_dates.append(start_date_obj)
    
    start_date = min(start_dates)
    end_date = max(end_dates)


    total_points = 0

    for user_story in story_points:
        total_points += story_points.get(user_story)

    points_per_task = {}

    for user_story in story_points:
        tasks = tasks_per_user_story.get(user_story)
        if tasks:
            points_per_task[user_story] = round(story_points[user_story] / len(tasks), 3)

    points_per_date = {}

    for user_story in closed_task_per_user_story:
        closed_tasks = closed_task_per_user_story.get(user_story)
        for closed_task in closed_tasks:
            finished_date = closed_task.get('finished_date')
            if points_per_task.get(user_story):
                points_per_date[finished_date] = points_per_date.get(finished_date, 0.0) + points_per_task.get(user_story)

    complete_dates = []

    while start_date <= end_date:
        complete_dates.append(str(start_date.date()))
        start_date += timedelta(days = 1)


    partial_story_points = {}
    partial_story_points["Total"] = total_points

    for date in complete_dates:
        points_on_date = points_per_date.get(date)
        points_on_previous_date = partial_story_points.get(list(partial_story_points.keys())[-1], total_points)

        if points_on_date:
            partial_story_points[date] = round(points_on_previous_date - points_on_date, 2)
        else:
            partial_story_points[date] = points_on_previous_date
    

    return partial_story_points
