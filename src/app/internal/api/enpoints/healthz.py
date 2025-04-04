import grpc
from fastapi import (
    APIRouter,
    status,
)
from fastapi.responses import JSONResponse

from app.internal.generated import (
    healthz_pb2_grpc,
    healthz_pb2,
)
from app.internal.core import settings


router = APIRouter()


@router.get("/healthz")
async def check_status() -> JSONResponse:
    """
    Проверка состояния сервиса.

    Этот маршрут используется для проверки доступности и состояния сервиса. Возвращает
    статус `200 OK` и сообщение с текущим состоянием.

    Parametrs
    ---------
    None

    Returns
    -------
    JSONResponse
        Ответ с JSON-данными, содержащий ключ `status` со значением `ok`.

    Status Code
    ------------
    `200 OK`
        Успешный ответ, означающий, что сервис работает нормально.

    """

    with grpc.insecure_channel(settings.grpc_url) as channel:

        stub = healthz_pb2_grpc.StatusStub(channel)
        response = stub.Healthz(healthz_pb2.HealthzRequest())
        
        return JSONResponse(
            content={"status": response.status},
            status_code=status.HTTP_200_OK
        )