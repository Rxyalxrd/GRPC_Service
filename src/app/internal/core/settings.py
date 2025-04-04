from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class AppSettings(BaseSettings):
    """
    Насторойки FastAPI пирложения.

    Attributes
    ----------
    app_title : Literal
        Название приложения.
    app_description : Literal
        Описание приложения.
    secret : Literal
        FastAPI ключ.
 
    """
    
    app_title: str
    app_description: str
    secret: str


class GRPCServerSettings(BaseSettings):
    """
    Настройки grpc сервера.

    Attributes
    ----------
    grpc_url : Literal
        Подключение grpc сервера.

    """
    
    grpc_url: str


class Settings(
    AppSettings,
    GRPCServerSettings,
):
    """
    Главный класс настроек.

    Attributes
    ----------
    model_config : SettingsConfigDict
        Загрузка чувствительных данных из .env

    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()  # type: ignore