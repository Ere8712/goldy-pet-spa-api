from pydantic import BaseModel, Field
from typing import Optional


class ClienteBase(BaseModel):

    nombre: str = Field(
        ...,
        min_length=3,
        max_length=150
    )

    telefono: str = Field(
        ...,
        min_length=10,
        max_length=15
    )

    correo: Optional[str] = None


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):

    nombre: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=150
    )

    telefono: Optional[str] = Field(
        default=None,
        min_length=10,
        max_length=15
    )

    correo: Optional[str] = None


class ClienteResponse(ClienteBase):

    id: int

    class Config:
        from_attributes = True