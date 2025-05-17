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

        # Проверяем существование пользователя
            # if existing:
            #     (status.ALREADY_EXISTS, "Пользователь уже существует")

        async with grpc.aio.insecure_channel(settings.grpc_url) as channel:

            stub = user_pb2_grpc.AuthServiceStub(channel)

            response = await stub.Login(user_pb2.LoginRequest(**credentials.model_dump()))
            
            return JWTToken(
                access_token=response.access_token,
                token_type=response.token_type,
            )

    except grpc.aio.AioRpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.details())
            elif e.code() == grpc.StatusCode.UNAUTHENTICATED:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.details())
            else:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@router.post(
    "/register",
    summary="",
    response_model=JWTToken,
)
async def register(user: UserCreate) -> JWTToken:


    # Проверяем существование пользователя
        # if existing:
        #     (status.ALREADY_EXISTS, "Пользователь уже существует")

    async with grpc.aio.insecure_channel(settings.grpc_url) as channel:

        stub = user_pb2_grpc.AuthServiceStub(channel)

        response = await stub.Register(user_pb2.RegisterRequest(**user.model_dump()))

        return JWTToken(
            access_token=response.access_token,
            token_type=response.token_type
        )
