from pydantic import (
    PostgresDsn,
)
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)
from loguru import logger


class gRPCSettings(BaseSettings):
    """
    Настройки gRPC сервера.

    Attributes
    ----------
    grpc_url : str
        URL для подключения к gRPC серверу.

    """

    grpc_host: str
    grpc_port: int

    @property
    def grpc_url(self) -> str:
        return f"{self.grpc_host}:{self.grpc_port}"


class FastAPISettings(BaseSettings):
    """
    Настройки `FastAPI` приложения.

    Attributes
    ----------
    app_title : str
        Название приложения.
    app_description : str
        Описание приложения.
    secret : str
        Секретный ключ приложения, используется для подписи JWT и других нужд.

    """

    app_host: str
    app_port: int
    app_title: str
    app_description: str


class PostgreSQLSettings(BaseSettings):
    """
    Настройки подключения к базе данных PostgreSQL.

    Attributes
    ----------
    postgres_user : str
        Имя пользователя БД.
    postgres_password : str
        Пароль пользователя БД.
    postgres_host : str
        Хост, на котором работает сервер БД.
    postgres_port : int
        Порт сервера БД.
    postgres_db : str
        Название базы данных.

    Methods
    -------
    database_url()
        Составляет полный url для подключения к БД.

    """

    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    postgres_db: str

    @property
    def database_url(self) -> str:
        """
        Формирует строку подключения к базе данных PostgreSQL
        с использованием драйвера asyncpg.

        Returns
        -------
        str
            Строка подключения в формате:
            postgresql+asyncpg://user:password@host:port/db

        """

        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            port=self.postgres_port,
            path=self.postgres_db
        ).unicode_string()


class HashSettings(BaseSettings):
    """
    
    """

    hash_secret_key: str
    algorithm: str
    access_token_expire_minutes: int

class Settings(
    FastAPISettings,
    PostgreSQLSettings,
    gRPCSettings,
    HashSettings,
):
    """
    Основные настройки проекта, загружаемые из .env файла.

    Attributes
    ----------
    model_config : SettingsConfigDict
        Конфигурация загрузки настроек из .env файла.

    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )



settings = Settings() # type: ignore
logger.info("Настройки успешно загружены.")

