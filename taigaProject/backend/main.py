from fastapi import FastAPI
from controller.story_controller import router
app = FastAPI()
app.include_router(router)


