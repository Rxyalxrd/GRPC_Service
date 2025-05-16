import grpc
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from app.internal.schemas import UserCreate, JWTToken
from app.internal.stubs import (
    user_pb2_grpc,
    user_pb2,
)
from app.internal.core import settings


router = APIRouter()

@router.post(
    "/login",
    summary="",
    response_model=JWTToken
)
async def login(credentials: UserCreate) -> JWTToken:
    try:

        async with grpc.aio.insecure_channel(settings.grpc_url) as channel:

            stub = user_pb2_grpc.AuthServiceStub(channel)

            grpc_response = await stub.Login(user_pb2.LoginRequest(credentials.model_dump()))
            
            return JWTToken(
                access_token=grpc_response.access_token,
                token_type=grpc_response.token_type,
            )
    except grpc.aio.AioRpcError as e:
        if e.code() == status.HTTP_401_UNAUTHORIZED:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный email или пароль"
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при обращении к gRPC сервису"
        )
    
@router.post(
    "/register",
    summary="",
    response_model=JWTToken
)
async def register_user(user: UserCreate) -> JWTToken:

    async with grpc.aio.insecure_channel(settings.grpc_url) as channel:

        stub = user_pb2_grpc.AuthServiceStub(channel)

        response = await stub.Register(user_pb2.RegisterRequest(user.model_dump()))

        return JWTToken(
            access_token=response.access_token,
            token_type=response.token_type
        )