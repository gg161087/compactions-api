from pydantic import BaseModel
from app.schemas.distrito_schema import DistritoCreate, DistritoResponse

class PredioBase(BaseModel):
    nombre: str
    direccion: str


class PredioCreate(PredioBase):
    distrito: DistritoCreate


class PredioResponse(PredioBase):
    id: int
    distrito: DistritoResponse
    class Config:
        from_attributes = True