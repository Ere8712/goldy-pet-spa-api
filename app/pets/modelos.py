from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Pet(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, index=True)

    nombre = Column(String, nullable=False)
    especie = Column(String, nullable=False)
    raza = Column(String, nullable=True)
    edad = Column(Integer, nullable=False)

    cliente_id = Column(
        Integer,
        ForeignKey("clientes.id"),
        nullable=False
    )

    cliente = relationship(
        "Cliente",
        back_populates="mascotas"
    )

    citas = relationship(
        "Cita",
        back_populates="pet",
        cascade="all, delete-orphan"
    )