from fastapi import APIRouter, Header, Request, HTTPException
from service.userstory_service import get_userstory_burndown_by_project_id

userstory_router = APIRouter()

@userstory_router.get("/userstory_burndown")
def get_userstories(request:Request,project_id: int):
    access_token = request.headers.get('Authorization')
    if(access_token):
        return get_userstory_burndown_by_project_id(project_id, access_token)
    else:
        raise HTTPException(status_code=401, detail="Missing or invalid access token")
    
