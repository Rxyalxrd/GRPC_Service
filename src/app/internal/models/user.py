from sqlalchemy.orm import Mapped

from app.internal.core import Base


class User(Base):

    email: Mapped[str]
    password: Mapped[str]
