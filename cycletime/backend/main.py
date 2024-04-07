from fastapi import FastAPI
from controller.cycletime_controller import cycletime_router
from controller.project_controller import project_router
from controller.login_controller import login_router

app = FastAPI()

app.include_router(cycletime_router, prefix='/api/cycletime')
app.include_router(project_router, prefix='/api/project')
app.include_router(login_router, prefix='/api')