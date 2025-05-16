from pydantic import BaseModel, EmailStr


class JWTToken(BaseModel):

    access_token: str
    token_type: str


class AbstractUser(BaseModel):

    email: EmailStr
    password: str


class UserCreate(AbstractUser):
    """
    """