from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import CheckConstraint
from app.internal.core import Base
from app.const import DEFAULT_QUANTITY


class Book(Base):
    name: Mapped[str]
    author: Mapped[str]
    pub_date: Mapped[int | None]
    isbn: Mapped[str | None] = mapped_column(unique=True)
    quantity: Mapped[int] = mapped_column(default=DEFAULT_QUANTITY)

    __table_args__ = (
        CheckConstraint('quantity >= 0', name='check_quantity_not_negative'),
    )
