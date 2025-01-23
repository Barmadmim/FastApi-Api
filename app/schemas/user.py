from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


# Enum para el rol del usuario
class RoleEnumPydantic(str, Enum):
    admin = "admin"
    usuario = "usuario"


# Modelo Pydantic para la respuesta del usuario
class UserResponse(BaseModel):
    user_uid: int
    username: str
    last_name: str
    phone_number: Optional[str] = None
    rol: RoleEnumPydantic
    gender: Optional[str] = None
    institucion: Optional[str] = None
    grade: Optional[str] = None
    creation_date: datetime
    last_modified: datetime
    country_origin: Optional[str] = None
    courses: Optional[List[str]] = None
    language_skills: Optional[dict] = None
    age: Optional[int] = None
    email: Optional[str] = None
    photo: Optional[str] = None

    class Config:
        orm_mode = True  # Permite usar modelos de SQLAlchemy directamente


class TokenRequest(BaseModel):
    access_token: str

class UserCoursesUpdate(BaseModel):
    courses: List[str]