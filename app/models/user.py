from sqlalchemy import Column, Integer, String, Date, DateTime, Enum, ARRAY, JSON, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
import enum
import bcrypt

Base = declarative_base()


# Definición del Enum para el rol
class RoleEnum(enum.Enum):
    admin = "admin"
    user = "user"

# Creación de la clase User
class User(Base):
    __tablename__ = "users"

    user_uid = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False, index=True)
    last_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    rol = Column(Enum(RoleEnum), default=RoleEnum.user)
    gender = Column(String, nullable=True)
    institucion = Column(String, nullable=True)
    grade = Column(String, nullable=True)
    creation_date = Column(DateTime, default=datetime.utcnow)
    last_modified = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    country_origin = Column(String, nullable=True)
    courses = Column(ARRAY(String), nullable=True)
    language_skills = Column(JSONB, nullable=True)
    age = Column(Integer, nullable=True)
    email = Column(String, nullable=True)
    photo = Column(String, nullable=True)

    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def check_password(hashed_password: str, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))



class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    token_uid = Column(Integer, primary_key=True, autoincrement=True)
    user_uid = Column(Integer, ForeignKey('users.user_uid'), nullable=False)
    refresh_token = Column(Text, nullable=False)
    expires_at = Column(DateTime, nullable=False)

    # Relación con la clase User
    user = relationship("User", backref="refresh_tokens")

