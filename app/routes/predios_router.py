from fastapi import Depends, Path, HTTPException,APIRouter
from typing import Annotated, List
from sqlalchemy.orm import Session
from starlette import status
from app.models.predio_model import Predio
from app.schemas.predio_schema import PredioCreate, PredioResponse
from app.models.distrito_model import Distrito
from app.config.database import SessionLocal
from .auth_router import get_current_user

router = APIRouter(
    prefix='/predios',
    tags=['predios']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/", response_model=List[PredioResponse], status_code=status.HTTP_200_OK)
def traer_predios(user:user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Autenticación fallida')
    return db.query(Predio).all()

@router.get("/{id_predio}", response_model=PredioResponse, status_code=status.HTTP_200_OK)
def traer_predio(user:user_dependency, db: db_dependency, id_predio: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Autenticación fallida')
    predio_model = db.query(Predio).filter(Predio.id==id_predio).first()
    if predio_model is not None:
        return predio_model
    else:
        raise HTTPException(status_code=404, detail="No se encontró el predio.")
    
@router.post("/crear/", status_code=status.HTTP_201_CREATED)
def crear_predio(user:user_dependency, db: db_dependency,predio_request:PredioCreate):
    if user is None:
        raise HTTPException(status_code=401, detail='Autenticación fallida')
    # Obtener datos del predio
    distrito_data = predio_request.distrito
    if not distrito_data or not distrito_data.municipio:
        raise HTTPException(status_code=400, detail="Distrito no especificado correctamente")
    
    # Buscar distrito por nombre (insensible a mayúsculas/minúsculas)
    distrito = db.query(Distrito).filter(Distrito.municipio.ilike(distrito_data.municipio)).first()
    
    if not distrito:
        raise HTTPException(status_code=404, detail=f"Distrito '{distrito_data.municipio}' no encontrado")
    
    # Crear modelo de predio
    predio_model = Predio(
        nombre=predio_request.nombre,
        direccion=predio_request.direccion,
        distrito_id=distrito.id  # Asociar distrito encontrado
    )
    
    # Guardar predio en la base de datos
    db.add(predio_model)
    db.commit()
    db.refresh(predio_model)

@router.put("/{predio_id}", status_code=status.HTTP_204_NO_CONTENT)
def modificar_predio(user:user_dependency, db: db_dependency, predio_request:PredioCreate, predio_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Autenticación fallida')
    predio_model=db.query(Predio).filter(Predio.id==predio_id).first()
    if predio_model is None:
        raise HTTPException(status_code=404, detail="No se encontró el depósito.")
    
    predio_model.nombre=predio_request.nombre
    predio_model.direccion=predio_request.direccion
    db.commit()

@router.delete("/eliminar/{predio_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_predio(user:user_dependency, db:db_dependency,predio_id:int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Autenticación fallida')
    predio_model=db.query(Predio).filter(Predio.id==predio_id).first()
    if predio_model is None:
        raise HTTPException(status_code=404, detail="No se encontró el depósito")
    db.query(Predio).filter(Predio.id==predio_id).delete()
    db.commit()

@router.get("/distrito/{renglon}", status_code=status.HTTP_200_OK)
def traer_distritos(user:user_dependency, db: db_dependency, renglon: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Autenticación fallida')
    distrito_model = db.query(Distrito).filter(Distrito.renglon==renglon).all()
    if distrito_model is not None:
        return distrito_model
    else:
        raise HTTPException(status_code=404, detail="No se encontró el distrito.")