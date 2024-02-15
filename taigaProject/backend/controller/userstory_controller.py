from fastapi import APIRouter, Header, Request, HTTPException
from service.userstory_service import get_storypoint_burndown_for_sprint

userstory_router = APIRouter()

@userstory_router.get("/userstory_burndown")
def get_userstories(request:Request,sprint_id: int):
    access_token = request.headers.get('Authorization')
    if(access_token):
        return get_storypoint_burndown_for_sprint(sprint_id, access_token)
    else:
        raise HTTPException(status_code=401, detail="Missing or invalid access token")
    
