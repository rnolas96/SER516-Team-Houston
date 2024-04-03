from typing import Union

from fastapi import FastAPI

app = FastAPI()

@app.get("/api")
def read_root():
    return "Response coming from API file in the backend folder"