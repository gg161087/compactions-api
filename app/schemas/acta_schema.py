from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from app.schemas.vehiculo_schema import VehiculoActaCreate, VehiculoCreate
from app.schemas.predio_schema import PredioResponse
from app.schemas.persona_schema import PersonaResponse

# Base Schema
class ActaCompactacionBase(BaseModel):
    fecha: datetime
    lugar: str
    paquetes: Optional[int] = None
    toneladas: Optional[float] = None
    fecha_retiro: Optional[datetime] = None
    observaciones: Optional[str] = None

    class Config:
        from_attributes = True


# Create Schema
class ActaCompactacionCreate(ActaCompactacionBase):
    predio_id: int
    testigo_id: Optional[int] = None
    responsable_dao_id: Optional[int] = None
    responsable_policial_id: Optional[int] = None
    vehiculos: List[VehiculoActaCreate]

    class Config:
        from_attributes = True


# Update Schema
class ActaCompactacionUpdate(ActaCompactacionBase):
    predio_id: int
    testigo_id: Optional[int] = None
    responsable_dao_id: Optional[int] = None
    responsable_policial_id: Optional[int] = None
    foto: Optional[str] = None

    class Config:
        from_attributes = True


# Response Schema
class ActaCompactacionResponse(ActaCompactacionBase):
    id: int
    predio: PredioResponse
    testigo: Optional[PersonaResponse] = None
    responsable_dao: Optional[PersonaResponse] = None
    responsable_policial: Optional[PersonaResponse] = None
    vehiculos: List[VehiculoCreate]
    foto: Optional[str] = None

    class Config:
        from_attributes = True
