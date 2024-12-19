from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base import Base

class Distrito(Base):
    __tablename__ = 'distritos'

    id = Column(Integer, primary_key=True, index=True)
    renglon = Column(Integer, nullable=False)
    municipio = Column(String(255), nullable=False)

    predios = relationship("Predio", back_populates="distrito")
