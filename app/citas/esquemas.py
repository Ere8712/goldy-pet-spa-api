from datetime import date, time

from pydantic import BaseModel
from typing import Optional


class CitaBase(BaseModel):
    fecha: date
    hora: time
    servicio: str
    estado: str = "Pendiente"
    pet_id: int


class CitaCreate(CitaBase):
    pass


class CitaUpdate(BaseModel):
    fecha: Optional[date] = None
    hora: Optional[time] = None
    servicio: Optional[str] = None
    estado: Optional[str] = None
    pet_id: Optional[int] = None


class CitaResponse(CitaBase):
    id: int

    class Config:
        from_attributes = True