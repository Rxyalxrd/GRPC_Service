import asyncio
from datetime import datetime, timedelta, timezone

import grpc
from fastapi import status
from loguru import logger
from passlib.context import CryptContext
from jose import jwt
from sqlalchemy import select
from .internal.stubs import (
    healthz_pb2,
    healthz_pb2_grpc,
    user_pb2,
    user_pb2_grpc,
)
from .internal.core import settings, AsyncSessionLocal
from .internal.models import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Status(healthz_pb2_grpc.StatusServicer):
    async def Healthz(self, request, context):

        return healthz_pb2.HealthzResponse(status=status.HTTP_200_OK)


class AuthService(user_pb2_grpc.AuthServiceServicer):

    @staticmethod
    async def create_access_token(data: dict, expires_delta=None):

        expire = (
            datetime.now(timezone.utc) +
            (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
        )

        data.update({"exp": expire})

        return jwt.encode(data, settings.hash_secret_key, algorithm=settings.algorithm)

    async def Login(self, request, context):

        async with AsyncSessionLocal() as session:
        
            stmt = await session.execute(select(User).where(User.email == request.email))
            user = stmt.scalar_one_or_none()

            if user is None:
                await context.abort(grpc.StatusCode.NOT_FOUND, "User not found")

            if not pwd_context.verify(request.password, user.password):
                await context.abort(grpc.StatusCode.UNAUTHENTICATED, "Incorrect password")
            
            token = await self.create_access_token({"sub": user.email})

            return user_pb2.TokenResponse(access_token=token, token_type="bearer")

    async def Register(self, request, context):

        async with AsyncSessionLocal() as session:

            hashed_password = pwd_context.hash(request.password)
            
            new_user = User(email=request.email, password=hashed_password)

            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)

            token = await self.create_access_token({"sub": new_user.email})

            return user_pb2.TokenResponse(access_token=token, token_type="bearer")
        

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
