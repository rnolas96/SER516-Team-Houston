from fastapi import FastAPI
from controller.userstory_controller import userstory_router
from controller.task_controller import task_router
from controller.login_controller import login_router

app = FastAPI()
app.include_router(userstory_router, prefix='/api/userstory')
app.include_router(task_router, prefix='/api/task')
app.include_router(login_router, prefix='/api')

