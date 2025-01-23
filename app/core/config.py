import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Carga las variables del archivo .env
env_path = Path('app') / '.env'
load_dotenv(dotenv_path=env_path, override=True)

class Settings:
    # Base de datos
    DATABASE_URL: str = (
        f"postgresql+asyncpg://{os.getenv('DB_USER')}:"  # Usamos asyncpg para conexión asincrónica
        f"{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:"  # Datos de conexión
        f"{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )

    # Configuración de JWT
    JWT_SECRET: str = os.getenv("JWT_SECRET", "your_jwt_secret")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))


# Instancia de configuración
settings = Settings()

