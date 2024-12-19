import uuid
from fastapi import Depends, HTTPException, APIRouter, Path, UploadFile
from typing import Annotated, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from starlette import status
from pathlib import Path as Pathlib
from app.models.acta_model import ActaCompactacion
from app.schemas.acta_schema import ActaCompactacionCreate, ActaCompactacionResponse, ActaCompactacionUpdate
from app.models.predio_model import Predio
from app.models.persona_model import Persona
from app.models.vehiculo_model import Vehiculo
from app.config.database import SessionLocal
from .auth_router import get_current_user

router = APIRouter(
    prefix='/actas',
    tags=['actas']
)

UPLOAD_DIR = Pathlib("uploads")

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/", response_model= List[ActaCompactacionResponse], status_code=status.HTTP_200_OK)
def traer_actas(user:user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Autenticación fallida')
    return db.query(ActaCompactacion).all()

@router.get("/{acta_id}", response_model=ActaCompactacionResponse, status_code=status.HTTP_200_OK)
def obtener_acta_compactacion(acta_id: int, db: Session = Depends(get_db)):
    acta = (
        db.query(ActaCompactacion).filter(ActaCompactacion.id == acta_id)
        .first()
    )
    if not acta:
        raise HTTPException(status_code=404, detail="Acta de compactación no encontrada")

    return acta

@router.post("/crear/", status_code=status.HTTP_201_CREATED)
async def crear_acta_compactacion(
    acta_data: ActaCompactacionCreate, db: Session = Depends(get_db)
):
    # Verificar existencia del depósito
    predio = db.query(Predio).filter(Predio.id == acta_data.predio_id).first()
    if not predio:
        raise HTTPException(status_code=404, detail="Depósito no encontrado")

    # Verificar existencia de las personas solo si los campos no son None
    testigo = None
    responsable_dao = None
    responsable_policial = None

    if acta_data.testigo_id:
        testigo = db.query(Persona).filter(Persona.id == acta_data.testigo_id).first()
        if not testigo:
            raise HTTPException(status_code=404, detail="Testigo especificado no encontrado")
    if acta_data.responsable_dao_id:
        responsable_dao = db.query(Persona).filter(Persona.id == acta_data.responsable_dao_id).first()
        if not responsable_dao:
            raise HTTPException(status_code=404, detail="Responsable DAO especificado no encontrado")
    if acta_data.responsable_policial_id:
        responsable_policial = db.query(Persona).filter(Persona.id == acta_data.responsable_policial_id).first()
        if not responsable_policial:
            raise HTTPException(status_code=404, detail="Responsable policial especificado no encontrado")

    # Verificar que la lista de vehículos no esté vacía
    if not acta_data.vehiculos:
        raise HTTPException(status_code=400, detail="La lista de vehículos no puede estar vacía")
    
    nro_ruvss = [vehiculo.nro_ruvs for vehiculo in acta_data.vehiculos]
    vehiculos_existentes = db.query(Vehiculo).filter(Vehiculo.nro_ruvs.in_(nro_ruvss)).all()
    if vehiculos_existentes:
        raise HTTPException(status_code=400, detail="Uno o más vehículos ya están asociados a otra acta")

    # Crear la nueva acta
    try:
        nueva_acta = ActaCompactacion(**acta_data.model_dump(exclude={"vehiculos"}, by_alias=True))

        try:
            db.add(nueva_acta)
            db.flush()

            for vehiculo_data in acta_data.vehiculos:
                nuevo_vehiculo = Vehiculo(**vehiculo_data.dict(exclude={"acta_compactacion_id"}), acta_compactacion_id=nueva_acta.id)
                db.add(nuevo_vehiculo)

            db.commit()
            db.refresh(nueva_acta)
        except SQLAlchemyError as e:
            db.rollback()  # Deshacer cambios en caso de error
            raise HTTPException(status_code=500, detail=f"Error al guardar en la base de datos: {str(e)}")

        # return nueva_acta
    
    except HTTPException as http_exc:
        # Propagar errores de FastAPI
        raise http_exc
    except Exception as e:
        # Manejar errores generales
        raise HTTPException(status_code=500, detail=f"Ocurrió un error inesperado: {e}")

@router.put("/{acta_id}", status_code=status.HTTP_204_NO_CONTENT)
def modificar_acta(user:user_dependency, db: db_dependency, acta_request:ActaCompactacionUpdate, acta_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Autenticación fallida')
    acta_model=db.query(acta_model.ActaCompactacion).filter(acta_model.ActaCompactacion.id==acta_id).first()
    if acta_model is None:
        raise HTTPException(status_code=404, detail="No se encontró el vehiculo.")
    
    # Actualizar dinámicamente todos los campos
    for field, value in acta_request.dict(exclude_unset=True).items():
        setattr(acta_model, field, value)

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al guardar en la base de datos: {str(e)}")

    return {"detail": "Acta actualizada correctamente"}

@router.post("/{acta_id}/cargar_pdf")
async def cargar_pdf_de_acta(
    file: UploadFile,
    user: user_dependency,
    db: db_dependency,
    acta_id: int = Path(gt=0),
):
    if user is None:
        raise HTTPException(status_code=401, detail="Autenticación fallida")

    acta_model = db.query(acta_model.ActaCompactacion).filter(acta_model.ActaCompactacion.id == acta_id).first()
    if not acta_model:
        raise HTTPException(status_code=404, detail="Acta no encontrada")

    try:
        # Verificar que el archivo sea un PDF
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="El archivo proporcionado no es un PDF válido.")

        # Leer el archivo PDF
        pdf_data = await file.read()

        # Guardar el archivo con un nombre único
        filename = f"acta{acta_id}_{uuid.uuid4()}.pdf"
        file_path = UPLOAD_DIR / filename
        with file_path.open("wb") as buffer:
            buffer.write(pdf_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el archivo PDF: {e}")

    try:
        # Actualizar el modelo con la ruta del archivo PDF
        acta_model.pdf = str(file_path)
        db.commit()
        db.refresh(acta_model)
    except SQLAlchemyError as e:
        db.rollback()  # Deshacer cambios en caso de error
        raise HTTPException(status_code=500, detail=f"Error al guardar en la base de datos: {str(e)}")

    return {"detail": "Archivo PDF cargado correctamente", "file_path": str(file_path)}