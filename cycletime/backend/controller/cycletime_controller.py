from fastapi import APIRouter, Header, Request, HTTPException
from service.cycletime_service import get_sprintwise_task_cycle_time, get_cycle_time_for_date_range

cycletime_router = APIRouter()
    
@cycletime_router.get("/cycle_time")
def get_task_cycle_time(request: Request, project_id: int):
    auth_token = request.headers.get('Authorization')

    if (auth_token):
        return get_sprintwise_task_cycle_time(project_id, auth_token)
    else:
        raise HTTPException(status_code = 401, detail = "Missing or invalid access token")

@cycletime_router.get("/cycle_time_time_range")
def get_task_cycle_time_in_time_range(request: Request, start_date, end_date, project_id: int):
    auth_token = request.headers.get('Authorization')

    if (auth_token):
        return get_cycle_time_for_date_range(project_id, start_date, end_date, auth_token)
    else:
        raise HTTPException(status_code = 401, detail = "Missing or invalid access token")    
