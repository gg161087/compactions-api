from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.models.base import Base

class ActaCompactacion(Base):
    __tablename__ = 'acta_compactacion'
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False)
    lugar = Column(String(255), nullable=False)
    predio_id = Column(Integer, ForeignKey("predio.id"))
    testigo_id = Column(Integer, ForeignKey("persona.id"))
    responsable_dao_id = Column(Integer, ForeignKey("persona.id"))
    responsable_policial_id = Column(Integer, ForeignKey("persona.id"))
    pdf = Column(String(255), nullable=True)
    paquetes = Column(Integer)
    toneladas = Column(Float)
    fecha_retiro = Column(Date)
    observaciones = Column(String(255))

    predio = relationship("Predio", back_populates="actas")
    testigo = relationship("Persona", back_populates="testigo_actas", foreign_keys=[testigo_id])
    responsable_dao = relationship("Persona", back_populates="responsable_dao_actas", foreign_keys=[responsable_dao_id])
    responsable_policial = relationship("Persona", back_populates="responsable_policial_actas", foreign_keys=[responsable_policial_id])
    vehiculos = relationship("Vehiculo", back_populates="acta_compactacion")
