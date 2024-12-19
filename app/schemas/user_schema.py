from pydantic import BaseModel
from typing import Optional

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    telefono: Optional[str] = None
    is_active: bool
    role: Optional[str] = None

    class Config:
        from_attributes = True

class CreateUserRequest(BaseModel):
    username:str
    email:str
    first_name:str
    last_name:str
    password:str
    role:str

class Token(BaseModel):
    access_token:str
    token_type:str