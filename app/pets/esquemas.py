from pydantic import BaseModel, Field


class PetBase(BaseModel):

    nombre: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    especie: str = Field(
        ...,
        min_length=2,
        max_length=50
    )

    raza: str | None = None

    edad: int = Field(
        ...,
        ge=0,
        le=30
    )

    cliente_id: int


class PetCreate(PetBase):
    pass


class PetUpdate(BaseModel):

    nombre: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    especie: str | None = Field(
        default=None,
        min_length=2,
        max_length=50
    )

    raza: str | None = None

    edad: int | None = Field(
        default=None,
        ge=0,
        le=30
    )

    cliente_id: int | None = None


class PetResponse(PetBase):

    id: int

    class Config:
        from_attributes = True