from pydantic import BaseModel, EmailStr


class AbstractLibrarian(BaseModel): # Librarian

    email: EmailStr
    password: str


class LibrarianCreate(AbstractLibrarian):
    """

    """