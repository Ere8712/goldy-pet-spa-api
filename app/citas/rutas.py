from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.errores import (
    BadRequestException,
    ResourceNotFoundException,
    DuplicateResourceException
)

from app.citas.modelos import Cita
from app.citas.esquemas import CitaCreate, CitaResponse

from app.pets.modelos import Pet


router = APIRouter(
    prefix="/citas",
    tags=["Citas"]
)


def _get_cita_by_id(
    db: Session,
    cita_id: int
):

    cita = db.query(Cita).filter(
        Cita.id == cita_id
    ).first()

    if not cita:
        raise ResourceNotFoundException(
            f"Cita con ID {cita_id} no encontrada."
        )

    return cita



def _validate_cita(
    db: Session,
    cita: CitaCreate,
    exclude_id: int | None = None
):

    # Validación: mascota existente
    mascota = db.query(Pet).filter(
        Pet.id == cita.pet_id
    ).first()

    if not mascota:
        raise ResourceNotFoundException(
            "La mascota indicada no existe."
        )


    # Regla de negocio:
    # No permitir citas en fechas pasadas
    if cita.fecha < date.today():

        raise BadRequestException(
            "No se pueden registrar citas en fechas pasadas."
        )


    # Validación de campos
    if not cita.servicio.strip():

        raise BadRequestException(
            "El servicio es obligatorio."
        )


    # Regla de negocio:
    # Una mascota debe tener al menos una hora entre servicios

    nueva_hora_inicio = datetime.combine(
        cita.fecha,
        cita.hora
    )

    nueva_hora_fin = nueva_hora_inicio + timedelta(hours=1)


    citas_existentes = db.query(Cita).filter(
        Cita.pet_id == cita.pet_id,
        Cita.fecha == cita.fecha
    )


    # Evitar comparar contra la misma cita al actualizar
    if exclude_id is not None:

        citas_existentes = citas_existentes.filter(
            Cita.id != exclude_id
        )


    for cita_existente in citas_existentes.all():

        hora_existente_inicio = datetime.combine(
            cita_existente.fecha,
            cita_existente.hora
        )

        hora_existente_fin = (
            hora_existente_inicio
            + timedelta(hours=1)
        )


        if (
            nueva_hora_inicio < hora_existente_fin
            and nueva_hora_fin > hora_existente_inicio
        ):

            raise DuplicateResourceException(
                "La mascota ya tiene una cita cercana a ese horario. "
                "Debe existir al menos una hora entre servicios."
            )



# CREATE

@router.post(
    "/",
    response_model=CitaResponse,
    status_code=201
)
def crear_cita(
    cita: CitaCreate,
    db: Session = Depends(get_db)
):

    _validate_cita(
        db,
        cita
    )


    nueva_cita = Cita(
        **cita.model_dump()
    )

    db.add(nueva_cita)
    db.commit()
    db.refresh(nueva_cita)

    return nueva_cita



# READ ALL CON FILTRO

@router.get(
    "/",
    response_model=list[CitaResponse]
)
def listar_citas(
    fecha: date | None = None,
    db: Session = Depends(get_db)
):

    query = db.query(Cita)


    if fecha:

        query = query.filter(
            Cita.fecha == fecha
        )


    return query.all()



# READ ONE

@router.get(
    "/{cita_id}",
    response_model=CitaResponse
)
def obtener_cita(
    cita_id: int,
    db: Session = Depends(get_db)
):

    return _get_cita_by_id(
        db,
        cita_id
    )



# UPDATE

@router.put(
    "/{cita_id}",
    response_model=CitaResponse
)
def actualizar_cita(
    cita_id: int,
    cita: CitaCreate,
    db: Session = Depends(get_db)
):

    db_cita = _get_cita_by_id(
        db,
        cita_id
    )


    _validate_cita(
        db,
        cita,
        exclude_id=cita_id
    )


    for key, value in cita.model_dump().items():

        setattr(
            db_cita,
            key,
            value
        )


    db.commit()
    db.refresh(db_cita)

    return db_cita



# DELETE

@router.delete(
    "/{cita_id}"
)
def eliminar_cita(
    cita_id: int,
    db: Session = Depends(get_db)
):

    db_cita = _get_cita_by_id(
        db,
        cita_id
    )


    db.delete(db_cita)
    db.commit()


    return {
        "mensaje": "Cita eliminada correctamente"
    }