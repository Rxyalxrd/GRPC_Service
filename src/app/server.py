import asyncio

import grpc
from fastapi import status
from loguru import logger

from internal.generated import (
    healthz_pb2,
    healthz_pb2_grpc,
)
from internal.core import settings


class Status(healthz_pb2_grpc.StatusServicer):
    def Healthz(self, request, context):

        logger.debug("Получен запрос")

        return healthz_pb2.HealthzResponse(status=status.HTTP_200_OK)


async def serve() -> None:
    server = grpc.aio.server()
    healthz_pb2_grpc.add_StatusServicer_to_server(Status(), server)
    server.add_insecure_port(settings.grpc_url)

    try:
        await server.start()
        logger.debug("gRPC сервер запущен ...")
        await server.wait_for_termination()

    except asyncio.CancelledError:
        logger.warning("gRPC сервер остановлен (CancelledError)")
        await server.stop(0)
        raise

    except KeyboardInterrupt:
        logger.warning("Остановка gRPC сервера пользователем")
        await server.stop(0)

    except Exception:
        logger.error("Непредвиденная ошибка", exc_info=True)
        await server.stop(0)

    finally:
        logger.debug("gRPC сервер корректно завершён.")

if __name__ == '__main__':
    try:
        asyncio.run(serve())
    except KeyboardInterrupt:
        logger.warning("Принудительная остановка gRPC сервера")