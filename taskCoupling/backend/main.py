from fastapi import FastAPI
from controller.taskCouplingController import task_coupling_router
from controller.project_controller import project_router


app = FastAPI()

app.include_router(task_coupling_router, prefix='/api/taskCoupling')
app.include_router(project_router, prefix='/api/project')
