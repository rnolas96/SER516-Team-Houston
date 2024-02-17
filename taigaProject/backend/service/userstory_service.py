
import datetime
from datetime import datetime, timedelta
from taigaApi.milestone.getMilestoneById import get_milestone_by_id
from taigaApi.userStory.getUserStory import get_custom_attribute_from_userstory, get_custom_attribute_type_id, get_user_story
from taigaApi.task.getTasks import get_tasks_by_milestone


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
    date_storypoint_map={}
<<<<<<< HEAD
=======

    for user_story in user_stories:
        if user_story['is_closed']:
                
            if user_story['finish_date']  :
                    
                finish_date = datetime.fromisoformat(user_story['finish_date'].replace('Z', '+00:00')).strftime('%Y-%m-%d')
                if(finish_date in date_storypoint_map):
                    date_storypoint_map[finish_date] += user_story['total_points']
                else:
                    date_storypoint_map[finish_date] = user_story['total_points']

    print("dictionary",date_storypoint_map)
>>>>>>> b947cc9 (changed burndown api)

    for user_story in user_stories:
        if user_story['is_closed']:
                
            if user_story['finish_date']  :
                    
                finish_date = datetime.fromisoformat(user_story['finish_date'].replace('Z', '+00:00')).strftime('%Y-%m-%d')
<<<<<<< HEAD
<<<<<<< HEAD
=======
                print("date=====",finish_date)
>>>>>>> b947cc9 (changed burndown api)
=======
>>>>>>> c0a16ab (removed unwanted prints)
                if(finish_date in date_storypoint_map):
                    date_storypoint_map[finish_date] += user_story['total_points']
                else:
                    date_storypoint_map[finish_date] = user_story['total_points']
<<<<<<< HEAD
=======

<<<<<<< HEAD
    print("dictionary",date_storypoint_map)
>>>>>>> b947cc9 (changed burndown api)

=======
>>>>>>> c0a16ab (removed unwanted prints)
    for date in range((end_date - start_date).days+1):
       
        current_date = start_date+timedelta(days = date)
        if current_date.strftime('%Y-%m-%d') in date_storypoint_map:
            total_story_points -= date_storypoint_map[current_date.strftime('%Y-%m-%d')]
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

    sprint_data = get_milestone_by_id(sprint_id, auth_token)
    user_stories = sprint_data['user_stories']

    if not user_stories:
        return {}

    response["0"] = 0
    total_custom_attribute_value = 0

    start_date = sprint_data['estimated_start']
    end_date = sprint_data['estimated_finish']

<<<<<<< HEAD
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    for date in range((end_date - start_date).days+1):
        current_date = start_date+timedelta(days = date)
        response[str(current_date)] = 0

    for user_story in user_stories:
        if user_story['is_closed'] and user_story['finish_date']:
            current_date = datetime.fromisoformat(user_story['finish_date'].split("T")[0])
            user_story_id = user_story['id']
            custom_attribute_data = get_custom_attribute_from_userstory(user_story_id, auth_token)
            custom_attribute_type_id = get_custom_attribute_type_id(project_id, auth_token, custom_attribute_name)
            if current_date in response:
                response[current_date] += int(custom_attribute_data[custom_attribute_type_id])
            else:
                response[current_date] = 0
                response[current_date] += int(custom_attribute_data[custom_attribute_type_id])

    total_custom_attribute_value = 0

    for res_key, res_val in response.items():
        total_custom_attribute_value += res_val

=======
>>>>>>> c0a16ab (removed unwanted prints)
    response = dict(sorted(response.items()))

    for res_key, res_val in response.items():
        if res_key != "0":
            response[res_key] = total_custom_attribute_value - response[res_key]
            total_custom_attribute_value = response[res_key]
            
    serialized_response = json.dumps(response)
    r_userstory.set('userstory_business_value_data', serialized_response)

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


        result[current_date.date()]= total_points_for_sprint
  
    return result