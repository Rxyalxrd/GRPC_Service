from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.internal.core import Base

class UrlNames(Base):
    """
    Модель БД для предстваления названия для ссылок.

    Attributes
    ----------

    name : str
        Название для ссылки.
    url : str
        Ссылка на ресурс.
    
    """

    name: Mapped[str] = mapped_column(unique=True)
    url: Mapped[str]
