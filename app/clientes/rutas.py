from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.errores import (
    BadRequestException,
    DuplicateResourceException,
    ResourceNotFoundException,
)

from .esquemas import (
    ClienteCreate,
    ClienteResponse,
    ClienteUpdate,
)
from .modelos import Cliente

router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)


# ---------- FUNCIONES AUXILIARES ----------

def _get_cliente_by_id(db: Session, cliente_id: int) -> Cliente:
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()

    if not cliente:
        raise ResourceNotFoundException(
            f"Cliente con ID {cliente_id} no encontrado."
        )

    return cliente


def _validate_cliente_name_available(
    db: Session,
    nombre: str,
    exclude_id: Optional[int] = None
) -> None:

    query = db.query(Cliente).filter(
        Cliente.nombre == nombre.strip()
    )

    if exclude_id is not None:
        query = query.filter(
            Cliente.id != exclude_id
        )

    if query.first():
        raise DuplicateResourceException(
            f"El cliente '{nombre}' ya existe."
        )


def _validate_input_strings(
    nombre: str,
    telefono: str
) -> None:

    if not nombre.strip():
        raise BadRequestException(
            "El nombre es obligatorio."
        )

    if not telefono.strip():
        raise BadRequestException(
            "El teléfono es obligatorio."
        )


# ---------- CREATE ----------

@router.post(
    "/",
    response_model=ClienteResponse,
    status_code=201
)
def create_cliente(
    cliente_in: ClienteCreate,
    db: Session = Depends(get_db)
):

    _validate_input_strings(
        cliente_in.nombre,
        cliente_in.telefono
    )

    _validate_cliente_name_available(
        db,
        cliente_in.nombre
    )

    nuevo_cliente = Cliente(
        nombre=cliente_in.nombre.strip(),
        telefono=cliente_in.telefono.strip(),
        correo=cliente_in.correo
    )

    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)

    return nuevo_cliente


# ---------- READ ALL ----------

@router.get(
    "/",
    response_model=List[ClienteResponse]
)
def list_clientes(
    nombre: Optional[str] = None,
    db: Session = Depends(get_db)
):

    query = db.query(Cliente)

    if nombre and nombre.strip():
        query = query.filter(
            Cliente.nombre.ilike(f"%{nombre.strip()}%")
        )

    return query.all()


# ---------- READ ONE ----------

@router.get(
    "/{cliente_id}",
    response_model=ClienteResponse
)
def get_cliente(
    cliente_id: int,
    db: Session = Depends(get_db)
):

    return _get_cliente_by_id(
        db,
        cliente_id
    )


# ---------- UPDATE ----------

@router.put(
    "/{cliente_id}",
    response_model=ClienteResponse
)
def update_cliente(
    cliente_id: int,
    cliente_in: ClienteCreate,
    db: Session = Depends(get_db)
):

    _validate_input_strings(
        cliente_in.nombre,
        cliente_in.telefono
    )

    db_cliente = _get_cliente_by_id(
        db,
        cliente_id
    )

    if cliente_in.nombre.strip() != db_cliente.nombre:

        _validate_cliente_name_available(
            db,
            cliente_in.nombre,
            exclude_id=cliente_id
        )

    db_cliente.nombre = cliente_in.nombre.strip()
    db_cliente.telefono = cliente_in.telefono.strip()
    db_cliente.correo = cliente_in.correo

    db.commit()
    db.refresh(db_cliente)

    return db_cliente


# ---------- PARTIAL UPDATE ----------

@router.patch(
    "/{cliente_id}",
    response_model=ClienteResponse
)
def partial_update_cliente(
    cliente_id: int,
    cliente_in: ClienteUpdate,
    db: Session = Depends(get_db)
):

    db_cliente = _get_cliente_by_id(
        db,
        cliente_id
    )

    if cliente_in.nombre is not None:

        nombre = cliente_in.nombre.strip()

        if not nombre:
            raise BadRequestException(
                "El nombre es obligatorio."
            )

        if nombre != db_cliente.nombre:

            _validate_cliente_name_available(
                db,
                nombre,
                exclude_id=cliente_id
            )

        db_cliente.nombre = nombre

    if cliente_in.telefono is not None:

        telefono = cliente_in.telefono.strip()

        if not telefono:
            raise BadRequestException(
                "El teléfono es obligatorio."
            )

        db_cliente.telefono = telefono

    if cliente_in.correo is not None:
        db_cliente.correo = cliente_in.correo

    db.commit()
    db.refresh(db_cliente)

    return db_cliente


# ---------- DELETE ----------

@router.delete(
    "/{cliente_id}",
    status_code=204
)
def delete_cliente(
    cliente_id: int,
    db: Session = Depends(get_db)
):

    db_cliente = _get_cliente_by_id(
        db,
        cliente_id
    )

    db.delete(db_cliente)
    db.commit()