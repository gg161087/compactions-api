from pydantic import BaseModel

class DistritoBase(BaseModel):
    renglon: int
    municipio: str

class DistritoCreate(DistritoBase):
    pass

class DistritoResponse(DistritoBase):
    id: int

    class Config:
        from_attributes = True