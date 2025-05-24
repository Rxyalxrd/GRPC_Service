import asyncio

import grpc
from loguru import logger
from app.internal.stubs import (
    healthz_pb2_grpc,
    user_pb2_grpc,
)
from .settings import settings
from app.internal.servicer import Status, AuthService


async def serve() -> None:
    server = grpc.aio.server()
    healthz_pb2_grpc.add_StatusServicer_to_server(Status(), server)
    user_pb2_grpc.add_AuthServiceServicer_to_server(AuthService(), server)
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