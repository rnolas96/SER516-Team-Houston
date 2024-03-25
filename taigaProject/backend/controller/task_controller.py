from fastapi import APIRouter, Header, Request, HTTPException
from service.task_service import get_sprintwise_task_cycle_time, get_task_cycle_time_time_range, get_sprintwise_task_lead_time, get_cost_of_delay_for_sprint

task_router = APIRouter()

    # @task_router.get("/cycle_time")
# def get_cycle_time(request: Request, project_id: int):
#     auth_token = request.headers.get('Authorization')
#     if (auth_token):
#         return get_sprintwise_cycle_time(project_id, auth_token)
#     else:
#         raise HTTPException(status_code = 401, detail = "Missing or invalid access token")
    
# @task_router.get("/task_burndown")
# def get_task_burndown(request: Request, project_id: int):
#     auth_token = request.headers.get("Authorization")

#     if auth_token:
#         return get_sprintwise_task_count(project_id, auth_token)
#     else:
#         raise HTTPException(status_code = 401, detail = "Missing or invalid access token")
    
@task_router.get("/cycle_time")
def get_task_cycle_time(request: Request, project_id: int):
    auth_token = request.headers.get('Authorization')

    if (auth_token):
        return get_sprintwise_task_cycle_time(project_id, auth_token)
    else:
        raise HTTPException(status_code = 401, detail = "Missing or invalid access token")

@task_router.get("/cycle_time_time_range")
def get_task_cycle_time_in_time_range(request: Request, start_date, end_date, project_id: int):
    auth_token = request.headers.get('Authorization')

    if (auth_token):
        return get_task_cycle_time_time_range(project_id, start_date, end_date, auth_token)
    else:
        raise HTTPException(status_code = 401, detail = "Missing or invalid access token")    

@task_router.get("/lead_time")
def get_task_lead_time(request: Request, project_id: int):
    auth_token = request.headers.get('Authorization')

    if (auth_token):
        return get_sprintwise_task_lead_time(project_id, auth_token)
    else:
        raise HTTPException(status_code = 401, detail = "Missing or invalid access token")
    
@task_router.get("/cost_of_delay")
def get_cost_of_delay(request: Request, project_id: int, sprint_id: int, business_value_cost_factor: int):
    auth_token = request.headers.get('Authorization')

    if (auth_token):
        return get_cost_of_delay_for_sprint(project_id, sprint_id, business_value_cost_factor, auth_token)
    else:
        raise HTTPException(status_code = 401, detail = "Missing or invalid access token")