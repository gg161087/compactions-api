import time
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from app.models.base import Base
from app.models.distrito_model import Distrito
from app.config.database import engine
from app.routes import vehiculos_router, auth_router, personas_router, actas_router, predios_router
from app.seed.distritos_seed import DISTRITOS

def wait_for_db():
    while True:
        try:
            connection = engine.connect()
            connection.close()
            print("Conexión a la base de datos exitosa.")
            break
        except OperationalError:
            print("Esperando que la base de datos esté disponible...")
            time.sleep(5)

# Esperar a que la base de datos esté lista
wait_for_db()

app = FastAPI()

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)
    load_seed_data()

def load_seed_data():
    with Session(engine) as session:
        # Verifica si la tabla ya tiene datos para evitar duplicados
        existing_count = session.query(Distrito).count()
        if existing_count == 0:
            # Inserta los datos iniciales
            session.bulk_insert_mappings(Distrito, DISTRITOS)
            session.commit()
            print(f"{len(DISTRITOS)} distritos insertados correctamente.")
        else:
            print("Los datos de distritos ya existen, no se insertarán de nuevo.")


if __name__ == "__main__":
    create_tables()

app.include_router(vehiculos_router.router)
app.include_router(personas_router.router)
app.include_router(predios_router.router)
app.include_router(actas_router.router)
app.include_router(auth_router.router)

#python main.py; uvicorn main:app --host 0.0.0.0 --port 8000 --reload