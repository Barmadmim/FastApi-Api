from fastapi import APIRouter, HTTPException, Request
from app.schemas.auth import Token
from app.core.tokens import verify_refresh_token, create_access_token
import logging

router = APIRouter(prefix="/api/auth", tags=["Autenticación"])
logger = logging.getLogger(__name__)

# Ruta para refrescar el token
@router.post("/refresh_token", response_model=Token)
async def refresh_token(request: Request, token: str):
    try:
        # Verificar si el token de refresh es válido
        new_access_token = verify_refresh_token(token)

        if not new_access_token:
            raise HTTPException(status_code=401, detail="Refresh token no válido")
        
        # Crear un nuevo access token
        access_token = create_access_token(new_access_token['user_uid'])

        return {"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        # Registrar el error detallado para depuración
        logger.error(f"Error al refrescar el token: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error interno del servidor")

