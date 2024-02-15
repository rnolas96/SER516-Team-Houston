
import datetime
from datetime import timedelta
from taigaApi.milestone.getMilestoneById import get_milestone_by_id
from taigaApi.userStory.getUserStory import get_user_story


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

def get_storypoint_burndown_for_sprint(sprint_id,auth_token):
    response=[]
    
    #get sprint info 
    sprint_data = get_milestone_by_id(sprint_id, auth_token)
    user_stories = sprint_data['user_stories']

    start_date = sprint_data['estimated_start']
    end_date = sprint_data['estimated_finish']

    for date in range((end_date - start_date).days+1):
        result={}
        current_date = start_date+timedelta(days = date)
        print("date ==",date)
        
        for user_story in user_stories:
            if user_story['is_closed']:
                if user_story['finish_date'] and datetime.fromisoformat(user_story['finish_date'].split("T")[0])==current_date :
                    result[current_date]=user_story['total_points']
    print(result)
   ##user_stories = get_user_story(project_id, auth_token)
    total_story_points = 0

    return response

