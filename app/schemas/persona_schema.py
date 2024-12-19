from pydantic import BaseModel

class PersonaBase(BaseModel):
    nombre: str
    apellido: str
    dni: str

class PersonaCreate(PersonaBase):
    pass

class PersonaResponse(PersonaBase):
    id: int
    class Config:
        from_attributes = True
