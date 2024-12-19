from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base

class Persona(Base):
    __tablename__ = 'persona'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    apellido = Column(String(255), nullable=False)
    dni = Column(String(20), nullable=False, unique=True)

    testigo_actas = relationship("ActaCompactacion", back_populates="testigo", foreign_keys='ActaCompactacion.testigo_id')
    responsable_dao_actas = relationship("ActaCompactacion", back_populates="responsable_dao", foreign_keys='ActaCompactacion.responsable_dao_id')
    responsable_policial_actas = relationship("ActaCompactacion", back_populates="responsable_policial", foreign_keys='ActaCompactacion.responsable_policial_id')
