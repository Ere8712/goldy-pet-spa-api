from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.pets.modelos import Pet
from app.pets.esquemas import (
    PetCreate,
    PetUpdate,
    PetResponse
)

router = APIRouter(
    prefix="/pets",
    tags=["Pets"]
)


@router.post("/", response_model=PetResponse)
def crear_pet(
    pet: PetCreate,
    db: Session = Depends(get_db)
):
    nueva_pet = Pet(**pet.model_dump())

    db.add(nueva_pet)
    db.commit()
    db.refresh(nueva_pet)

    return nueva_pet


@router.get("/", response_model=list[PetResponse])
def listar_pets(
    db: Session = Depends(get_db)
):
    return db.query(Pet).all()


@router.get("/{pet_id}", response_model=PetResponse)
def obtener_pet(
    pet_id: int,
    db: Session = Depends(get_db)
):
    return db.query(Pet).filter(
        Pet.id == pet_id
    ).first()


@router.put("/{pet_id}", response_model=PetResponse)
def actualizar_pet(
    pet_id: int,
    pet: PetCreate,
    db: Session = Depends(get_db)
):

    mascota = db.query(Pet).filter(
        Pet.id == pet_id
    ).first()

    for key, value in pet.model_dump().items():
        setattr(mascota, key, value)

    db.commit()
    db.refresh(mascota)

    return mascota


@router.patch("/{pet_id}", response_model=PetResponse)
def actualizar_parcial_pet(
    pet_id: int,
    pet: PetUpdate,
    db: Session = Depends(get_db)
):

    mascota = db.query(Pet).filter(
        Pet.id == pet_id
    ).first()

    datos = pet.model_dump(exclude_unset=True)

    for key, value in datos.items():
        setattr(mascota, key, value)

    db.commit()
    db.refresh(mascota)

    return mascota


@router.delete("/{pet_id}")
def eliminar_pet(
    pet_id: int,
    db: Session = Depends(get_db)
):

    mascota = db.query(Pet).filter(
        Pet.id == pet_id
    ).first()

    db.delete(mascota)
    db.commit()

    return {
        "mensaje": "Mascota eliminada"
    }