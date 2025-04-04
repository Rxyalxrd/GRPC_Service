from fastapi import FastAPI

from app.internal.api import main_router


app = FastAPI()

app.include_router(main_router)