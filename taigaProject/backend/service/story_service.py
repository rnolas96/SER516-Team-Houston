
from taigaApi.userStory.getUserStory import get_user_story

def get_total_storypoints_by_project_id(project_id,auth_token):
    response=[]
    
    user_stories = get_user_story(project_id, auth_token)
    total_story_points = 0

    user_stories_map = {}
    for user_story in user_stories: 
        if(user_story['milestone_name']):
            sprint = user_story['milestone_name'].split()
            sprint_key ="sprint" + sprint[1]
            if(sprint_key in user_stories_map):
                user_stories_map[sprint_key] += user_story['total_points']
            else:
                user_stories_map[sprint_key] = user_story['total_points']
    
        total_story_points += user_story['total_points']

    sprint_story_points_map ={}

    sprint_story_points_map['total_points']=total_story_points
    for key,val in user_stories_map.items():
        sprint_story_points_map[key] = total_story_points-val

        total_story_points -= val

    response.append(sprint_story_points_map)
    return response


