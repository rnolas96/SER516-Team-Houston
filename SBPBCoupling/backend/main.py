from fastapi import FastAPI
from controller.sbPbCouplingController import sp_pb_coupling_router
from controller.project_controller import project_router
from controller.login_controller import login_router

app = FastAPI()

app.include_router(sp_pb_coupling_router , prefix='/api/SbPbCoupling')
app.include_router(project_router, prefix='/api/project')
app.include_router(login_router, prefix='/api')


