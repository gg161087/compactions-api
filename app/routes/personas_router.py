from fastapi import Depends, Path, HTTPException,APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from app.models.persona_model import Persona
from app.schemas.persona_schema import PersonaCreate
from app.config.database import SessionLocal
from .auth_router import get_current_user

router = APIRouter(
    prefix='/personas',
    tags=['personas']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/", status_code=status.HTTP_200_OK)
def traer_personas(user:user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Autenticación fallida')
    return db.query(Persona).all()

@router.get("/{id_persona}", status_code=status.HTTP_200_OK)
def traer_persona(user:user_dependency, db: db_dependency, id_persona: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Autenticación fallida')
    persona_model = db.query(Persona).filter(Persona.id==id_persona).first()
    if persona_model is not None:
        return persona_model
    else:
        raise HTTPException(status_code=404, detail="No se encontró la persona.")
    
@router.post("/crear/", status_code=status.HTTP_201_CREATED)
def crear_persona(user:user_dependency, db: db_dependency,persona_request:PersonaCreate):
    if user is None:
        raise HTTPException(status_code=401, detail='Autenticación fallida')
    persona_model=Persona(**persona_request.dict())
    db.add(persona_model)
    db.commit()

@router.put("/{persona_id}", status_code=status.HTTP_204_NO_CONTENT)
def modificar_persona(user:user_dependency, db: db_dependency, persona_request:PersonaCreate, persona_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Autenticación fallida')
    persona_model=db.query(Persona).filter(Persona.id==persona_id).first()
    if persona_model is None:
        raise HTTPException(status_code=404, detail="No se encontró la persona.")
    
    persona_model.nombre=persona_request.nombre
    persona_model.apellido=persona_request.apellido
    persona_model.dni=persona_request.dni
    db.commit()

@router.delete("/eliminar/{persona_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_persona(user:user_dependency, db:db_dependency,persona_id:int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Autenticación fallida')
    todo_model=db.query(Persona).filter(Persona.id==persona_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="No se encontró la persona")
    db.query(Persona).filter(Persona.id==persona_id).delete()
    db.commit()