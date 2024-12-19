import os
from dotenv import load_dotenv
from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from app.models.user_model import Users
from app.schemas.user_schema import UserResponse, CreateUserRequest, Token
from app.config.database import SessionLocal

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

load_dotenv(dotenv_path="/api/.env")
SECRET_KEY= os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

bcrypt_context=CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username==username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No se pudo validar el usuario')
        return {'username': username, 'id': user_id, 'user_role': user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='No se pudo validar el usuario')

def create_access_token(username: str, user_id: int,role:str, expires_delta: timedelta):
    encode = {'sub':username, 'id': user_id, 'role':role}
    expire = datetime.utcnow() + expires_delta
    encode.update({'exp':expire})
    return jwt.encode(encode, SECRET_KEY,algorithm=ALGORITHM)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(db:db_dependency,create_user_request:CreateUserRequest):
    create_user_model=Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True
    )

    db.add(create_user_model)
    db.commit()

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No se pudo validar el usuario')
    token = create_access_token(user.username, user.id, user.role, timedelta(days=1))
    return {'access_token':token, 'token_type': 'bearer'}

@router.get("/current_user", response_model=UserResponse)
def current_user(user:Annotated[dict, Depends(get_current_user)]):
    if user is None:
        raise HTTPException(status_code=401, detail='Autenticación fallida')
    return user
