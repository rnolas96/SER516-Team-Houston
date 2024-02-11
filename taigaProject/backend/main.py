from fastapi import FastAPI
from controller.userstory_burndown_controller import router
from controller.login_controller import router2
app = FastAPI()
app.include_router(router, prefix='/api')
app.include_router(router2, prefix='/api')




