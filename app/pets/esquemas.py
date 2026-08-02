from pydantic import BaseModel


class PetBase(BaseModel):
    nombre: str
    especie: str
    raza: str | None = None
    edad: int
    cliente_id: int


class PetCreate(PetBase):
    pass


class PetUpdate(BaseModel):
    nombre: str | None = None
    especie: str | None = None
    raza: str | None = None
    edad: int | None = None
    cliente_id: int | None = None


class PetResponse(PetBase):
    id: int

    class Config:
        from_attributes = True