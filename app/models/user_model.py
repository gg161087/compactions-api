from sqlalchemy import Column, Integer, String, Boolean
from app.models.base import Base

class Users(Base):
    __tablename__='users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True)
    username = Column(String(20), unique=True)
    first_name= Column(String(50))
    last_name=Column(String(50))
    telefono=Column(String(50))
    hashed_password=Column(String(100))
    is_active=Column(Boolean, default=True)
    role=Column(String(50))
