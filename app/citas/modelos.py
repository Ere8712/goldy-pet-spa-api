from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Cita(Base):
    __tablename__ = "citas"

    id = Column(Integer, primary_key=True, index=True)

    fecha = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)

    servicio = Column(String(100), nullable=False)
    estado = Column(String(50), default="Pendiente")

    pet_id = Column(
        Integer,
        ForeignKey("pets.id"),
        nullable=False
    )

    pet = relationship(
        "Pet",
        back_populates="citas"
    )