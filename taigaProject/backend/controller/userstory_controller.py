from fastapi import APIRouter, Header, Request, HTTPException
from service.userstory_service import get_storypoint_burndown_for_sprint, get_userstory_custom_attribute_burndown_for_sprint, get_partial_storypoint_burndown_for_sprint, get_sb_coupling, get_pb_coupling, get_partial_sp, get_burndown_all_sprints, get_business_value_burndown_all_sprints

userstory_router = APIRouter()

@userstory_router.get("/userstory_burndown")
def get_userstories(request:Request,sprint_id: int):
    access_token = request.headers.get('Authorization')
    if(access_token):
        return get_storypoint_burndown_for_sprint(sprint_id, access_token)
    else:
        raise HTTPException(status_code=401, detail="Missing or invalid access token")
    
@userstory_router.get("/business_value_burndown")
def get_userstories_business_value_burndown(request:Request, project_id: int, sprint_id: int):
    access_token = request.headers.get('Authorization')
    if(access_token):
        try:
            return get_userstory_custom_attribute_burndown_for_sprint(project_id, sprint_id, access_token, "BV")
        except Exception as e:
            return e
    else:
        raise HTTPException(status_code=401, detail="Missing or invalid access token")
    
@userstory_router.get("/partial_userstory_burndown")
def get_partial_userstories_burndown(request:Request,sprint_id: int):
    access_token = request.headers.get('Authorization')
    if(access_token):
        return get_partial_storypoint_burndown_for_sprint(sprint_id, access_token)
    else:
        raise HTTPException(status_code=401, detail="Missing or invalid access token")
    

@userstory_router.get("/sb_coupling")
def get_sprint_backlog_coupling(request:Request, sprint_id: int):
    access_token = request.headers.get('Authorization')
    if(access_token):
        return get_sb_coupling(sprint_id, access_token)
    else:
        raise HTTPException(status_code=401, detail="Missing or invalid access token")
    

@userstory_router.get("/pb_coupling")
def get_product_backlog_coupling(request:Request, project_id: int):
    access_token = request.headers.get('Authorization')
    if(access_token):
        return get_pb_coupling(project_id, access_token)
    else:
        raise HTTPException(status_code=401, detail="Missing or invalid access token")
    
@userstory_router.get("/partial_story_points")
def get_partial_story_points(request: Request, project_id: int):
    access_token = request.headers.get('Authorization')
    if access_token:
        return get_partial_sp(project_id, access_token)
    else:
        raise HTTPException(status_code = 401, detail = "Missing or invalid access token")
    
@userstory_router.get("/userstory_burndown_for_all_sprints")
def get_userstories(request:Request,project_id: int):
    access_token = request.headers.get('Authorization')
    if(access_token):
        return get_burndown_all_sprints(project_id, access_token)
    else:
        raise HTTPException(status_code=401, detail="Missing or invalid access token")
    
@userstory_router.get("/business_value_burndown_for_all_sprints")
def get_business_values(request:Request,project_id: int):
    access_token = request.headers.get('Authorization')
    if(access_token):
        return get_business_value_burndown_all_sprints(project_id, "BV", access_token)
    else:
        raise HTTPException(status_code=401, detail="Missing or invalid access token")
