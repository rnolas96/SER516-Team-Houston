from fastapi import FastAPI
from controller.project_controller import project_router
from controller.engagement_controller import engagement_router
from controller.login_controller import login_router

app = FastAPI()
app.include_router(project_router, prefix='/api/project')
app.include_router(engagement_router, prefix = '/api/engagement')
app.include_router(login_router, prefix='/api')

