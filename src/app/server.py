import time
from concurrent import futures

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

        logger.info("Получен запрос")

        return healthz_pb2.HealthzResponse(status=status.HTTP_200_OK)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    healthz_pb2_grpc.add_StatusServicer_to_server(Status(), server)
    server.add_insecure_port(settings.grpc_url)
    server.start()

    logger.debug("Запуск grpc сервера ...")

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
