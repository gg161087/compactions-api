from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Predio(Base):
    __tablename__ = 'predio'
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    direccion = Column(String(255), nullable=False)
    
    distrito_id = Column(Integer, ForeignKey('distritos.id'), nullable=False)
    
    distrito = relationship("Distrito", back_populates="predios")
    actas = relationship("ActaCompactacion", back_populates="predio")
