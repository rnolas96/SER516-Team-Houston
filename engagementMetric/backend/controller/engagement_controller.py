from fastapi import APIRouter, Header, Request, HTTPException
from service.engagement_service import get_taiga_member_stats

engagement_router = APIRouter()

@engagement_router.get("/taiga_member_engagement")
def get_taiga_member_engagement_stat(request: Request, project_id: int):
    """
    """
    access_token = request.headers.get("Authorization")

    if access_token:
        return get_taiga_member_stats(project_id, access_token)
    else:
        raise HTTPException(status_code = 401, details = "Missing or invalid token")
    