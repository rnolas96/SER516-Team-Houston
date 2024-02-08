from fastapi import APIRouter, Header, Request, HTTPException
from service.story_service import get_total_storypoints_by_project_id

router = APIRouter()

@router.get("/userstory")
def get_userstories(request:Request,project_id: int):
    access_token = request.headers.get('Authorization')
    if(access_token):
        return get_total_storypoints_by_project_id(project_id, access_token)
    else:
        raise HTTPException(status_code=401, detail="Missing or invalid access token")