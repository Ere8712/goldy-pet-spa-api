from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.pets.modelos import Pet
from app.pets.esquemas import (
    PetCreate,
    PetUpdate,
    PetResponse
)

from app.clientes.modelos import Cliente
from app.errores import ResourceNotFoundException


router = APIRouter(
    prefix="/pets",
    tags=["Pets"]
)


def _get_pet_by_id(
    db: Session,
    pet_id: int
):

    mascota = db.query(Pet).filter(
        Pet.id == pet_id
    ).first()

    if not mascota:
        raise ResourceNotFoundException(
            f"Mascota con ID {pet_id} no encontrada."
        )

    return mascota


def _validate_cliente_exists(
    db: Session,
    cliente_id: int
):

    cliente = db.query(Cliente).filter(
        Cliente.id == cliente_id
    ).first()

    if not cliente:
        raise ResourceNotFoundException(
            "El cliente indicado no existe."
        )



# CREATE

@router.post(
    "/",
    response_model=PetResponse,
    status_code=201
)
def crear_pet(
    pet: PetCreate,
    db: Session = Depends(get_db)
):

    _validate_cliente_exists(
        db,
        pet.cliente_id
    )


    nueva_pet = Pet(
        **pet.model_dump()
    )

    db.add(nueva_pet)
    db.commit()
    db.refresh(nueva_pet)

    return nueva_pet



# READ ALL

@router.get(
    "/",
    response_model=list[PetResponse]
)
def listar_pets(
    db: Session = Depends(get_db)
):

    return db.query(Pet).all()



# READ ONE

@router.get(
    "/{pet_id}",
    response_model=PetResponse
)
def obtener_pet(
    pet_id: int,
    db: Session = Depends(get_db)
):

    return _get_pet_by_id(
        db,
        pet_id
    )



# UPDATE

@router.put(
    "/{pet_id}",
    response_model=PetResponse
)
def actualizar_pet(
    pet_id: int,
    pet: PetCreate,
    db: Session = Depends(get_db)
):

    mascota = _get_pet_by_id(
        db,
        pet_id
    )


    _validate_cliente_exists(
        db,
        pet.cliente_id
    )


    for key, value in pet.model_dump().items():

        setattr(
            mascota,
            key,
            value
        )


    db.commit()
    db.refresh(mascota)

    return mascota



# PATCH

@router.patch(
    "/{pet_id}",
    response_model=PetResponse
)
def actualizar_parcial_pet(
    pet_id: int,
    pet: PetUpdate,
    db: Session = Depends(get_db)
):

    mascota = _get_pet_by_id(
        db,
        pet_id
    )


    datos = pet.model_dump(
        exclude_unset=True
    )


    if "cliente_id" in datos:

        _validate_cliente_exists(
            db,
            datos["cliente_id"]
        )


    for key, value in datos.items():

        setattr(
            mascota,
            key,
            value
        )


    db.commit()
    db.refresh(mascota)

    return mascota



# DELETE

@router.delete(
    "/{pet_id}"
)
def eliminar_pet(
    pet_id: int,
    db: Session = Depends(get_db)
):

    mascota = _get_pet_by_id(
        db,
        pet_id
    )


    db.delete(mascota)
    db.commit()


    return {
        "mensaje": "Mascota eliminada correctamente"
    }