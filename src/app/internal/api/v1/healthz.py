import grpc
from fastapi import (
    APIRouter,
    Depends,
    status,
)
from fastapi.responses import JSONResponse

from app.internal.stubs import (
    healthz_pb2_grpc,
    healthz_pb2,
)
from app.internal.core import settings
from app.internal.models import Librarian
from app.internal.auth import get_current_user

router = APIRouter()


@router.get(
    "/healthz",
    summary="",
    description="",
)
async def check_status(user: Librarian = Depends(get_current_user)) -> JSONResponse:
    """
    Проверка состояния сервиса.

    Этот маршрут используется для проверки доступности и состояния сервиса. Возвращает
    статус `200 OK` и сообщение с текущим состоянием.

    Returns
    -------
    JSONResponse
        Ответ с JSON-данными, содержащий ключ `status` со значением `ok`.

    Status Code
    ------------
    `200 OK`
        Успешный ответ, означающий, что сервис работает нормально.

    """

    async with grpc.aio.insecure_channel(settings.grpc_url) as channel:

        stub = healthz_pb2_grpc.StatusStub(channel)
        response = await stub.Healthz(healthz_pb2.HealthzRequest())
        
        return JSONResponse(
            content={"status": response.status},
            status_code=status.HTTP_200_OK
        )
