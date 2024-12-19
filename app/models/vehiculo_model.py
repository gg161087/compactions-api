from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum as SAEnum
from sqlalchemy.orm import relationship
from enum import Enum
from app.models.base import Base

class EstadoVehiculo(str, Enum):
    aprobado = "Aprobado"
    a_verificar = "A verificar"

class Vehiculo(Base):
    __tablename__ = 'vehiculo'
    id = Column(Integer, primary_key=True, index=True)
    nro_ruvs = Column(String(50), nullable=False, unique=True)
    nro_cargo_policial = Column(String(50))
    dominio = Column(String(10))
    chasis_cuadro = Column(String(50))
    motor = Column(String(50))
    dependencia_policial = Column(String(255))
    marca = Column(String(50))
    modelo = Column(String(50))
    tipo = Column(String(50))
    acta_compactacion_id = Column(Integer, ForeignKey("acta_compactacion.id"))
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    usuario_creacion = Column(String(255))
    usuario_modificacion = Column(String(255))
    
    estado = Column(SAEnum(EstadoVehiculo), default=EstadoVehiculo.a_verificar)
    acta_compactacion = relationship("ActaCompactacion", back_populates="vehiculos")
