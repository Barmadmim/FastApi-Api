from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db_session
from app.repositories.examen_repository import ExamenRepository
from app.schemas.examenes import ExamenSchema, ExamenResponse
from app.core.middlewares import verify_jwt_token
from app.core.tokens import decode_token

examenes_router = APIRouter(
    prefix="/examenes", tags=["examenes"]
)


@examenes_router.get("/", response_model=List[ExamenResponse])
async def obtener_examenes_usuario(
    request: Request, db: AsyncSession = Depends(get_db_session)
):
    """
    Obtener los exámenes de un usuario específico según el access token.
    """
    # Intentar obtener el token desde el encabezado Authorization (Bearer token)
    authorization_header = request.headers.get("Authorization")
    
    if not authorization_header:
        raise HTTPException(status_code=401, detail="Token no proporcionado")
    
    token = authorization_header.split(" ")[1] if len(authorization_header.split()) == 2 else None
    
    if not token:
        raise HTTPException(status_code=401, detail="Token no proporcionado")
    
    # Decodificar el token y obtener el user_uid
    try:
        decoded_token = decode_token(token)  # Esta función debería manejar la decodificación del token
        user_uid = decoded_token.get("user_uid")
        if not user_uid:
            raise HTTPException(status_code=401, detail="Token inválido")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Error al decodificar el token: {str(e)}")

    # Obtener los exámenes del usuario por su user_uid
    examen_repo = ExamenRepository(db)
    examenes = await examen_repo.get_examenes_by_user_uid(user_uid)
    return examenes


@examenes_router.get("/todos/", response_model=List[ExamenResponse])
async def obtener_examenes_todos(db: AsyncSession = Depends(get_db_session)):
    """
    Obtener todos los exámenes sin necesidad de un token.
    """
    examen_repo = ExamenRepository(db)
    examenes = await examen_repo.get_all_examenes()
    return examenes


@examenes_router.post("/", response_model=ExamenResponse)
async def crear_examen(
    examen: ExamenSchema,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(verify_jwt_token),
):
    examen_repo = ExamenRepository(db)

    # Usamos los campos correctos del token
    user_uid = user["user_uid"]
    username = user["username"]

    nuevo_examen = await examen_repo.create_examen(
        examen_data=examen, user_uid=user_uid, username=username
    )
    return nuevo_examen
