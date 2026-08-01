from sqlalchemy import Column, Integer, String
from app.database import Base


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), unique=True, index=True)
    telefono = Column(String(150))
    correo = Column(String(150), index=True, nullable=True)