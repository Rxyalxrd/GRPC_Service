from datetime import datetime, timedelta, timezone

import grpc
from passlib.context import CryptContext
from jose import jwt
from sqlalchemy import select
from app.internal.stubs import (
    user_pb2,
    user_pb2_grpc,
)
from app.internal.core import settings, AsyncSessionLocal
from app.internal.models import Librarian


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
        
            stmt = await session.execute(select(Librarian).where(Librarian.email == request.email))
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
            
            new_user = Librarian(email=request.email, password=hashed_password)

            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)

            token = await self.create_access_token({"sub": new_user.email})

            return user_pb2.TokenResponse(access_token=token, token_type="bearer")
