import os
import json
from fastapi import APIRouter, Request
from taigaApi.authenticate import authenticate

login_router = APIRouter()

@login_router.post("/login")
async def login(request:Request):
    body = await request.body()
    try: 
        body = json.loads(body)
        auth_token = authenticate(body['username'], body['password'])
        os.environ['auth_token'] = auth_token
        return True, "Authentication Successful", os.environ['auth_token']
    except Exception as e:
        return False, "Authentication failed with", e