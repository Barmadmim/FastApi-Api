from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.audios import audios_router
from app.routes.auth import auth_router
from app.routes.examenes import examenes_router
from app.routes.language import language_router
from app.routes.userme import userme_router
from app.core.middlewares import JWTMiddleware
from app.core.database import async_engine, Base
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Micling Api",
    summary="API para gestionar el sistema Micling",
    version="0.0.1",
)

# Configuración de los orígenes permitidos para CORS
# pg_ctl -D "C:\Program Files\PostgreSQL\17\data" start
origins = [
    "http://localhost:8100",
    "http://127.0.0.1:8100",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://x89xntx3-8000.use2.devtunnels.ms",
    "exp://192.168.1.104:8082",
    "https://micling.com",
]

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Agregar middleware JWT
app.add_middleware(JWTMiddleware)

# Incluir routers para las distintas secciones de la app
app.include_router(auth_router)
app.include_router(examenes_router)
app.include_router(audios_router)
app.include_router(language_router)
app.include_router(userme_router)


# Montar la carpeta 'static' para servir archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")


# Evento para conectar a la base de datos al iniciar el servidor
@app.on_event("startup")
async def startup():
    # Crear tablas de forma asincrónica usando el motor asincrónico
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("Base de datos conectada y tablas creadas")


# Ruta principal para verificar el funcionamiento del servidor
@app.get("/", tags=["home"])
def home():
    return {"message": "Servidor corriendo"}
