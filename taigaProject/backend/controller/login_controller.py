import os
import json
from fastapi import APIRouter, Request
from service.userstory_burndown_service import get_userstory_burndown_by_project_id
from taigaApi.authenticate import authenticate

router2 = APIRouter()

@router2.post("/login")
async def login(request:Request):
    body = await request.body()
    try: 
        body = json.loads(body)
        auth_token = authenticate(body['username'], body['password'])
        os.environ['auth_token'] = auth_token
        return True, "Authentication Successful", os.environ['auth_token']
    except Exception as e:
        return False, "Authentication failed with", e