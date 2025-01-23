from fastapi import Request, HTTPException, Depends
from starlette.middleware.base import BaseHTTPMiddleware
import jwt
from app.core.config import settings

async def verify_jwt_token(request: Request):
    """Verifica el token JWT y retorna el payload si es válido."""
    
    # Primero, buscamos el token en las cookies
    token = request.cookies.get("access_token")

    # Si no encontramos el token en las cookies, buscamos en el encabezado de autorización
    if not token:
        token = request.headers.get("Authorization")
        if token and token.startswith("Bearer "):
            token = token.split(" ")[1]  # Extraemos el token del encabezado

    if not token:
        raise HTTPException(
            status_code=403,
            detail="Autenticación requerida: falta el token"
        )

    try:
        # Decodificamos el token con la clave secreta
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/api/examenes"):
            # Verificar el token en las cookies o encabezado de la solicitud
            token = request.cookies.get("access_token")

            if not token:
                token = request.headers.get("Authorization")
                if token and token.startswith("Bearer "):
                    token = token.split(" ")[1]  # Extraemos el token del encabezado

            if not token:
                raise HTTPException(
                    status_code=403,
                    detail="Autenticación requerida: falta el token"
                )

            try:
                # Decodificamos el token y lo asignamos al estado del request
                payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
                request.state.user = payload
            except jwt.ExpiredSignatureError:
                raise HTTPException(status_code=401, detail="Token expirado")
            except jwt.InvalidTokenError:
                raise HTTPException(status_code=401, detail="Token inválido")

        response = await call_next(request)
        return response
