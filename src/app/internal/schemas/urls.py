from pydantic import (
    BaseModel,
    HttpUrl,
    Field,
)

from app.const import (
    URL_SHEMA_MIN_LEN,
    NAME_SHEMA_MIN_LEN,
)

class DeafultUrlNames(BaseModel):
    """
    Абстрактная схема валидации имен и ссылок.

    Attributes
    ----------

    name : str
        Название для ссылки.
    url : str
        Ссылка на ресурс.

    """

    name: str = Field(gt=NAME_SHEMA_MIN_LEN)
    url: HttpUrl = Field(gt=URL_SHEMA_MIN_LEN)


class UrlNamesCreate(DeafultUrlNames):
    """
    Cхема валидации создания имен и ссылок.
    
    Атрибуты наследованы от `DeafultUrlNames`

    """



class UrlNamesRead(DeafultUrlNames):
    """
    Cхема валидации чтенния имен и ссылок.
    
    Атрибуты наследованы от `DeafultUrlNames`

    """


class UrlNamesUpdate(DeafultUrlNames):
    """
    Cхема валидации обновления имен и ссылок.
    
    Атрибуты наследованы от `DeafultUrlNames`

    """


class UrlNamesDelete(BaseModel):
    """
    Cхема валидации удаления имен и ссылок.

    Attributes
    ----------

    name : str
        Название для ссылки.

    """

    name: str = Field(gt=NAME_SHEMA_MIN_LEN)
