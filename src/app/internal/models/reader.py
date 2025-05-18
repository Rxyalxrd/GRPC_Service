from sqlalchemy.orm import Mapped

from app.internal.core import Base


class Reader(Base):

    name: Mapped[str]
    email: Mapped[str]
