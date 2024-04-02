from http.client import HTTPException
from urllib.request import Request
from fastapi import APIRouter, Header, Request, HTTPException

from service.leadtime_service import get_sprintwise_task_lead_time, get_task_lead_time_time_range

leadtime_router = APIRouter()


@leadtime_router.get("/lead_time")
def get_task_lead_time(request: Request, project_id: int):
    auth_token = request.headers.get('Authorization')

    if (auth_token):
        return get_sprintwise_task_lead_time(project_id, auth_token)
    else:
        raise HTTPException(status_code = 401, detail = "Missing or invalid access token")

@leadtime_router.get("/lead_time_time_range")
def get_task_lead_time_in_time_range(request: Request, start_date, end_date, project_id: int):
    auth_token = request.headers.get('Authorization')

    if (auth_token):
        return get_task_lead_time_time_range(project_id, start_date, end_date, auth_token)
    else:
        raise HTTPException(status_code = 401, detail = "Missing or invalid access token")
    