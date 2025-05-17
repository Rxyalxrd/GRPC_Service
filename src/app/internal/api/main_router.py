from fastapi import APIRouter

from app.internal.api.enpoints import (
    healthz_router,
    user_router,
)


main_router = APIRouter()

main_router.include_router(
    router=healthz_router,
    prefix="/status",
    tags=["K8s health check"],
)
main_router.include_router(
    router=user_router,
    prefix="/auth/jwt",
    tags=["Auth"],
)
