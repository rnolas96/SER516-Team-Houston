from fastapi import FastAPI
from controller.leadtime_controller import leadtime_router

app = FastAPI()

app.include_router(leadtime_router , prefix='/api/leadtime')

