from pydantic import BaseModel, EmailStr


class AbstractReader(BaseModel):
    """
    
    """

    name: str
    email: EmailStr


class ReaderCreate(AbstractReader):
    """
    
    """

class ReaderRead(BaseModel):
    """
    
    """

    name: str

class ReaderUpdate(AbstractReader):
    """
    
    """

class ReaderDelete(BaseModel):
    """
    
    """

    name: str
