from fastapi import FastAPI
from controller.costofdelay_controller import cost_of_delay_router
from controller.project_controller import project_router

app = FastAPI()
app.include_router(cost_of_delay_router, prefix='/api/cost_of_delay')
app.include_router(project_router, prefix='/api/project')
