import asyncio

from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.internal.api import main_router
from app.internal.core import settings
from app.server import serve


@asynccontextmanager
async def lifespan(app: FastAPI):

    grpc_task = asyncio.create_task(serve())

    try:
        yield
    finally:
        grpc_task.cancel()
        try:
            await grpc_task
        except asyncio.CancelledError:
            pass


app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    lifespan=lifespan,
)

app.include_router(main_router)
