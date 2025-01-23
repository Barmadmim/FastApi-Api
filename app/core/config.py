import os
from pathlib import Path
from dotenv import load_dotenv


env_path = Path('app') / '.env'
load_dotenv(dotenv_path=env_path, override=True)

class Settings:
    # Base de datos
    DATABASE_URL: str = (
        f"postgresql+asyncpg://{os.getenv('DB_USER')}:"
        f"{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:"
        f"{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )

    # Configuración de JWT
    JWT_SECRET: str = os.getenv("JWT_SECRET")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))


# Instancia de configuración
settings = Settings()

