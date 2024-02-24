from fastapi import APIRouter, Header, Request, HTTPException
from service.userstory_service import get_storypoint_burndown_for_sprint, get_userstory_custom_attribute_burndown_for_sprint, get_partial_storypoint_burndown_for_sprint, get_sb_coupling

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
def get_partial_userstories_burndown(request:Request,sprint_id: int):
    access_token = request.headers.get('Authorization')
    if(access_token):
        return get_sb_coupling(sprint_id, access_token)
    else:
        raise HTTPException(status_code=401, detail="Missing or invalid access token")