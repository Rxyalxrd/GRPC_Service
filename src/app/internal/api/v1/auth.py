from fastapi import (
    APIRouter,
    Depends,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
import grpc
from loguru import logger

from app.internal.schemas import (
    LibrarianCreate,
    JWTToken,
)
from app.internal.stubs import (
    user_pb2_grpc,
    user_pb2,
)
from app.internal.core import settings


router = APIRouter()


@router.post(
    "/login",
    response_model=JWTToken,
    summary="",
    description="",
)
async def login_oauth2(form_data: OAuth2PasswordRequestForm = Depends()) -> JWTToken:

    #TODO: валидировать form_data

    try:
        async with grpc.aio.insecure_channel(settings.grpc_url) as channel:
            stub = user_pb2_grpc.AuthServiceStub(channel)
            response = await stub.Login(user_pb2.LoginRequest(
                email=form_data.username,
                password=form_data.password
            ))

            logger.success("Пользователь аунтифицировался")

            return JWTToken(access_token=response.access_token, token_type=response.token_type)

    except grpc.aio.AioRpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                logger.error("Пользователь не найден")
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.details())
            elif e.code() == grpc.StatusCode.UNAUTHENTICATED:
                logger.warning("Пользователь не аунтифицирован")
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.details())
            else:
                logger.error("Ошибка сервера")
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


@router.post(
    "/register",
    summary="",
    description="",
    response_model=JWTToken,
)
async def register(user: LibrarianCreate) -> JWTToken:


    # Проверяем существование пользователя
        # if existing:
        #     (status.ALREADY_EXISTS, "Пользователь уже существует")
    try:
        async with grpc.aio.insecure_channel(settings.grpc_url) as channel:

            stub = user_pb2_grpc.AuthServiceStub(channel)

            response = await stub.Register(user_pb2.RegisterRequest(**user.model_dump()))

            logger.success("Пользователь зарегистрировался")

            return JWTToken(
                access_token=response.access_token,
                token_type=response.token_type
            )

    except grpc.aio.AioRpcError as e:
        if e.code() == status.HTTP_409_CONFLICT:
            logger.warning(f"Пользователь уже существует: {e.details()}")
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Пользователь уже существует")
        elif e.code() == status.HTTP_400_BAD_REQUEST:
            logger.warning(f"Некорректные данные при регистрации: {e.details()}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.details())
        else:
            logger.error(f"Ошибка gRPC при регистрации: {e.code()} - {e.details()}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Внутренняя ошибка сервера")
