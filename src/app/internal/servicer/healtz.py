from fastapi import status

from app.internal.stubs import (
    healthz_pb2,
    healthz_pb2_grpc,
)


class Status(healthz_pb2_grpc.StatusServicer):
    async def Healthz(self, request, context):

        return healthz_pb2.HealthzResponse(status=status.HTTP_200_OK)
