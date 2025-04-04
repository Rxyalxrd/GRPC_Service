from fastapi import APIRouter

from app.internal.api.enpoints import (
    healthz_router,
)


main_router = APIRouter()


main_router.include_router(
    router=healthz_router,
    prefix="/status",
    tags=["K8s health check"],
)