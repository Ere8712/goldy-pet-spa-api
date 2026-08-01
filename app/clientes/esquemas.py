from pydantic import BaseModel
from typing import Optional


class ClienteBase(BaseModel):
    nombre: str
    telefono: str
    correo: Optional[str] = None


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[str] = None


class ClienteResponse(ClienteBase):
    id: int

    class Config:
        from_attributes = True