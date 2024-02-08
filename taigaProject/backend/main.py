from fastapi import FastAPI
from controller.userstory_burndown_controller import router
app = FastAPI()
app.include_router(router, prefix='/api')


