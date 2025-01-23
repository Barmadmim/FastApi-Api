from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from enum import Enum

# Enum para el rol
class RoleEnum(Enum):
    ADMIN = "admin"
    USER = "usuario"

# Enum para los niveles de idioma
class LanguageLevel(str, Enum):
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B1_PLUS = "B1+"
    B2 = "B2"
    B2_PLUS = "B2+"
    C1 = "C1"
    C2 = "C2"
    C2_PLUS = "C2+"

# Enum para los idiomas disponibles
class AvailableLanguages(str, Enum):
    ENGLISH = "English"
    SPANISH = "Spanish"
    FRENCH = "French"
    GERMAN = "German"
    ITALIAN = "Italian"
    PORTUGUESE = "Portuguese"
    CHINESE = "Chinese"
    JAPANESE = "Japanese"
    KOREAN = "Korean"

# Enum para los géneros
class GenderEnum(str, Enum):
    MASCULINO = "Masculino"
    FEMENINO = "Femenino"
    PREFIERO_NO_DECIRLO = "Prefiero no decirlo"

# Modelo para habilidades lingüísticas
class LanguageSkill(BaseModel):
    language: str = AvailableLanguages.ENGLISH
    reading: LanguageLevel
    writing: LanguageLevel
    listening: LanguageLevel
    speaking: LanguageLevel

# Modelo para el inicio de sesión
class LoginRequest(BaseModel):
    username: str
    password: str

# Modelo para el registro
class RegisterRequest(BaseModel):
    username: str
    last_name: str
    password: str
    phone_number: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[GenderEnum] = None  # Cambio aquí
    institucion: Optional[str] = None
    grade: Optional[str] = None
    country_origin: Optional[str] = None
    language_skills: Optional[List[LanguageSkill]] = None
    courses: Optional[List[AvailableLanguages]] = None
    email: Optional[str] = None
    photo: Optional[str] = None