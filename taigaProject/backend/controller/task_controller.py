from fastapi import APIRouter, Header, Request, HTTPException
from service.task_service import get_sprintwise_cycle_time, get_sprintwise_lead_time, get_sprintwise_task_count, get_sprintwise_task_cycle_time

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
