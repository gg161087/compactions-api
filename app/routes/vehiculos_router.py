from fastapi import Depends, Path, HTTPException,APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from app.models.vehiculo_model import Vehiculo
from app.schemas.vehiculo_schema import VehiculoCreate
from app.config.database import SessionLocal
from .auth_router import get_current_user

router = APIRouter(
    prefix='/vehiculos',
    tags=['vehiculos']
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
def traer_vehiculos(user:user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Autenticación fallida')
    return db.query(Vehiculo).all()

@router.get("/{id_vehiculo}", status_code=status.HTTP_200_OK)
def traer_vehiculo(user:user_dependency, db: db_dependency, id_vehiculo: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Autenticación fallida')
    vehiculo_model = db.query(Vehiculo).filter(Vehiculo.id==id_vehiculo).first()
    if vehiculo_model is not None:
        return vehiculo_model
    else:
        raise HTTPException(status_code=404, detail="No se encontró el vehículo.")
    
@router.post("/crear/", status_code=status.HTTP_201_CREATED)
def crear_vehiculo(user:user_dependency, db: db_dependency, vehiculo_request:VehiculoCreate):
    if user is None:
        raise HTTPException(status_code=401, detail='Autenticación fallida')
    vehiculo_model=Vehiculo(**vehiculo_request.dict())
    db.add(vehiculo_model)
    db.commit()

@router.put("/{vehiculo_id}", status_code=status.HTTP_204_NO_CONTENT)
def modificar_vehiculo(user:user_dependency, db: db_dependency, vehiculo_request:VehiculoCreate, vehiculo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Autenticación fallida')
    vehiculo_model=db.query(Vehiculo).filter(Vehiculo.id==vehiculo_id).first()
    if vehiculo_model is None:
        raise HTTPException(status_code=404, detail="No se encontró el vehiculo.")
    
    vehiculo_model.dominio=vehiculo_request.dominio
    vehiculo_model.motor=vehiculo_request.motor
    vehiculo_model.marca=vehiculo_request.marca
    vehiculo_model.modelo=vehiculo_request.modelo
    vehiculo_model.tipo=vehiculo_request.tipo
    vehiculo_model.nro_ruvs=vehiculo_request.nro_ruvs
    vehiculo_model.nro_cargo_policial=vehiculo_request.nro_cargo_policial
    vehiculo_model.chasis_cuadro=vehiculo_request.chasis_cuadro
    vehiculo_model.dependencia_policial=vehiculo_request.dependencia_policial
    db.commit()

@router.delete("/eliminar/{vehiculo_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_vehiculo(user:user_dependency, db:db_dependency,vehiculo_id:int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Autenticación fallida')
    todo_model=db.query(Vehiculo).filter(Vehiculo.id==vehiculo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="No se encontró el vehiculo")
    db.query(Vehiculo).filter(Vehiculo.id==vehiculo_id).delete()
    db.commit()