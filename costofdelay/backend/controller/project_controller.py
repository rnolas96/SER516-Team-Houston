from fastapi import APIRouter, Header, Request, HTTPException

from service.project_service import get_sprint_details_from_project_id

project_router = APIRouter()

@project_router.get("/milestone_data")
def get_project_details(request:Request, project_slug:str):
    access_token = request.headers.get('Authorization')
    if access_token:
        return get_sprint_details_from_project_id(project_slug, access_token)
    else:
        raise HTTPException(status_code=401, detail="Missing or invalid access token")



