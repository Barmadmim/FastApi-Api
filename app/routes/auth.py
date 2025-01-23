from fastapi import APIRouter, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auth import LoginRequest, RegisterRequest
from app.repositories.user_respository import create_user, authenticate_user, refresh_user_token
from app.core.database import get_db_session

auth_router = APIRouter(
    prefix="/api/auth",
    tags=["Autenticación de Usuarios"]
)

@auth_router.post("/register")
async def register_user(
    register_request: RegisterRequest,
    response: Response,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Endpoint para registrar un nuevo usuario.
    """
    return await create_user(register_request, response, db)

@auth_router.post("/login", summary="Autenticar usuario y generar token de acceso")
async def login_user(
    login_request: LoginRequest,
    response: Response,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Endpoint para autenticar un usuario y generar un token de acceso.
    """
    return await authenticate_user(login_request, response, db)

@auth_router.post("/refresh-token", summary="Refrescar el token de acceso")
async def refresh_token_endpoint(
    refresh_token: str,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Endpoint para refrescar un token de acceso.
    """
    return await refresh_user_token(refresh_token, db)
