from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db_session
from app.repositories.examen_repository import ExamenRepository
from app.schemas.exams import ExamSchema, ExamResponse
from app.core.middlewares import verify_jwt_token
from app.core.tokens import decode_token

exams_router = APIRouter(
    prefix="/exams", tags=["exams"]
)

@exams_router.post("/", response_model=ExamResponse)
async def crear_examen(
    examen: ExamSchema,
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

@exams_router.get("/todos/", response_model=List[ExamResponse])
async def obtener_exams_todos(db: AsyncSession = Depends(get_db_session)):
    """
    Obtener todos los exámenes sin necesidad de un token.
    """
    examen_repo = ExamenRepository(db)
    exams = await examen_repo.get_all_exams()
    return exams

@exams_router.get("/", response_model=List[ExamResponse])
async def obtener_exams_usuario(
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
    exams = await examen_repo.get_exams_by_user_uid(user_uid)
    return exams

@exams_router.put("/{examen_id}", response_model=ExamResponse)
async def editar_examen(
    examen_id: int,
    examen: ExamSchema,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(verify_jwt_token),
):
    """
    Editar un examen específico por su ID.
    """
    examen_repo = ExamenRepository(db)

    # Verificar si el examen existe
    examen_existente = await examen_repo.get_examen_by_id(examen_id)
    if not examen_existente:
        raise HTTPException(status_code=404, detail="Examen no encontrado")

    # Actualizar el examen
    examen_actualizado = await examen_repo.update_examen(examen_id, examen)
    return examen_actualizado

@exams_router.delete("/{examen_id}", response_model=ExamResponse)
async def eliminar_examen(
    examen_id: int,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(verify_jwt_token),
):
    """
    Eliminar un examen específico por su ID.
    """
    examen_repo = ExamenRepository(db)

    # Verificar si el examen existe
    examen = await examen_repo.get_examen_by_id(examen_id)
    if not examen:
        raise HTTPException(status_code=404, detail="Examen no encontrado")

    # Eliminar el examen
    rows_deleted = await examen_repo.delete_examen(examen_id)
    if rows_deleted == 0:
        raise HTTPException(status_code=400, detail="No se pudo eliminar el examen")

    return examen


