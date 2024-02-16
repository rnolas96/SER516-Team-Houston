
import datetime
from datetime import datetime, timedelta
from taigaApi.milestone.getMilestoneById import get_milestone_by_id
from taigaApi.userStory.getUserStory import get_custom_attribute_from_userstory, get_custom_attribute_type_id, get_user_story
import redis
import json

r_userstory = redis.StrictRedis(host='localhost', port=6379, db=0)

# funtion to get sprintwise burndown chart details for a project. 
def get_userstory_burndown_by_project_id(project_id,auth_token):
    response=[]
    
    user_stories = get_user_story(project_id, auth_token)
    total_story_points = 0

    user_stories_map = {}
    for user_story in user_stories: 
        if(user_story['milestone_name']):
            print(user_story)
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

    #get sprint info 
    sprint_data = get_milestone_by_id(sprint_id, auth_token)
    user_stories = sprint_data['user_stories']
    total_story_points = sprint_data['total_points'] 

    start_date = datetime.strptime(sprint_data['estimated_start'],"%Y-%m-%d")
    end_date =  datetime.strptime(sprint_data['estimated_finish'],"%Y-%m-%d")
    result={}

    for date in range((end_date - start_date).days+1):
       
        current_date = start_date+timedelta(days = date)
        
        for user_story in user_stories:
            if user_story['is_closed']:
                if user_story['finish_date'] and datetime.fromisoformat(user_story['finish_date'].replace('Z', '+00:00')).date()==current_date.date() :
                    total_story_points -= user_story['total_points']
                    
            result[current_date] = total_story_points

    return result

def get_userstory_custom_attribute_burndown_for_sprint(project_id, sprint_id, auth_token, custom_attribute_name):
    """
    Description
    -----------
    Gets the user_story based on the project_id, filters it based on the sprint_id
    and uses the custom_attribute to get back the custom_attribute_values

    Arguments
    ---------
    project_id, sprint_id, auth_token, custom_attribute_name

    Returns
    -------
    A map of date and business value completed.
    """
    response = {}
    
    serialized_cached_data = r_userstory.get('userstory_business_value_data')
    if serialized_cached_data:
        response = json.loads(serialized_cached_data)
        return response

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
        response[str(current_date)] = 0

    for user_story in user_stories:

        user_story_id = user_story['id']
        custom_attribute_data = get_custom_attribute_from_userstory(user_story_id, auth_token)
        custom_attribute_type_id = get_custom_attribute_type_id(project_id, auth_token, custom_attribute_name)
        total_custom_attribute_value += int(custom_attribute_data[custom_attribute_type_id])

        if user_story['is_closed'] and user_story['finish_date']:
            current_date = datetime.fromisoformat(user_story['finish_date'].split("T")[0])
            if str(current_date) in response:
                response[str(current_date)] += int(custom_attribute_data[custom_attribute_type_id])
            else:
                response[str(current_date)] = int(custom_attribute_data[custom_attribute_type_id])

    response["0"] = total_custom_attribute_value

    response = dict(sorted(response.items()))

    for res_key, res_val in response.items():
        if res_key != "0":
            response[res_key] = total_custom_attribute_value - response[res_key]
            total_custom_attribute_value = response[res_key]


    serialized_response = json.dumps(response)

    r_userstory.set('userstory_business_value_data', serialized_response)

    return response
    
