from pydantic import BaseModel, Field


class AbstractBook(BaseModel):
    """
    
    """

    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    publication_year: int | None
    isbn: str | None
    copies: int = Field(1, ge=0)


class BookCreate(AbstractBook):
    """

    """


class BookRead(BaseModel):
    """
    
    """

    title: str = Field(..., min_length=1)


class BookUpdate(AbstractBook):
    """
    
    """


class BookDelete(BaseModel):
    """
    
    """

    title: str = Field(..., min_length=1)
