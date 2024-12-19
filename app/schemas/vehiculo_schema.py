
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.vehiculo_model import EstadoVehiculo

class VehiculoBase(BaseModel):
    nro_ruvs: str
    nro_cargo_policial: Optional[str] = None
    dominio: Optional[str] = None
    chasis_cuadro: Optional[str] = None
    motor: Optional[str] = None
    dependencia_policial: Optional[str] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None
    tipo: Optional[str] = None
    estado: Optional[EstadoVehiculo] = None
    # usuario_creacion: Optional[int] = None
    # usuario_modificacion: Optional[int] = None

class VehiculoCreate(VehiculoBase):
    acta_compactacion_id: Optional[int] = None

class VehiculoActaCreate(VehiculoBase):
    pass

class VehiculoResponse(VehiculoBase):
    id: int
    acta_compactacion_id: Optional[int] = None
    fecha_creacion: datetime
    fecha_modificacion: datetime
    class Config:
        from_attributes = True

class VehiculoActaCreate(VehiculoBase):
    pass