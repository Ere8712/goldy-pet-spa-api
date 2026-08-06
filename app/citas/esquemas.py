from datetime import date, time
from pydantic import BaseModel, Field
from typing import Optional


class CitaBase(BaseModel):

    fecha: date

    hora: time

    servicio: str = Field(
        ...,
        min_length=3,
        max_length=100
    )

    estado: str = Field(
        default="Pendiente",
        min_length=3
    )

    pet_id: int


class CitaCreate(CitaBase):
    pass


class CitaUpdate(BaseModel):

    fecha: Optional[date] = None

    hora: Optional[time] = None

    servicio: Optional[str] = Field(
        default=None,
        min_length=3
    )

    estado: Optional[str] = None

    pet_id: Optional[int] = None


class CitaResponse(CitaBase):

    id: int

    class Config:
        from_attributes = True