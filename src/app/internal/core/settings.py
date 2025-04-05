from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class AppSettings(BaseSettings):
    """
    Насторойки FastAPI пирложения.

    Attributes
    ----------
    app_title : str
        Название приложения.
    app_description : str
        Описание приложения.
    secret : str
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
    grpc_url : str
        Подключение grpc сервера.

    """
    
    grpc_url: str


class PostgreSQLSettings(BaseSettings):
    """
    Настройки подключения к базе данных.

    Attributes
    ----------
    database_url : str
        Подключение к базе данных.

    """

    database_url: str


class Settings(
    AppSettings,
    GRPCServerSettings,
    PostgreSQLSettings,
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
