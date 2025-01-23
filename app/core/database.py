from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from sqlalchemy.ext.declarative import declarative_base

# Creación del objeto Base que será utilizado por los modelos
Base = declarative_base()

# Crear el motor asincrónico
async_engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)

# Configuración de la sesión asincrónica de SQLAlchemy
AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

# Función para obtener una sesión asincrónica de SQLAlchemy
async def get_db_session():
    """
    Retorna una sesión de base de datos asincrónica.
    """
    async with AsyncSessionLocal() as session:
        yield session
