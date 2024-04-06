from fastapi import FastAPI
from controller.cycletime_controller import cycletime_router

app = FastAPI()

app.include_router(cycletime_router, prefix='/api/cycletime')

