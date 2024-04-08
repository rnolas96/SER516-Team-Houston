from fastapi import FastAPI
from controller.burndown_controller import burndown_router
from controller.project_controller import project_router
from controller.login_controller import login_router

app = FastAPI()
app.include_router(burndown_router, prefix='/api/burndown')
app.include_router(project_router, prefix='/api/project')
app.include_router(login_router, prefix='/api')
