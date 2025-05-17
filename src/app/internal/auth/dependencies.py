from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException
from jose import jwt, JWTError
from app.internal.core import settings
from app.internal.models import User
# from app.internal.schemas.token import TokenData
from app.internal.core import AsyncSessionLocal
from sqlalchemy import select


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/jwt/login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, settings.hash_secret_key, algorithms=[settings.algorithm])
        email = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        # token_data = TokenData(sub=email)

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token decode error")

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user
