# core/tokens.py

import jwt
from datetime import datetime, timedelta
from typing import Dict
from fastapi import HTTPException
from app.core.config import settings 

# Tiempo de expiración configurado en settings.py
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS
JWT_SECRET = settings.JWT_SECRET
JWT_ALGORITHM = settings.JWT_ALGORITHM

def verify_refresh_token(token: str) -> Dict:
    """
    Verifica y decodifica un refresh token, asegurando que sea válido y no esté expirado.
    Si el token es válido, devuelve los datos del token (por ejemplo, el user_uid).
    """
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        # Validar que el token contiene información de usuario
        if "user_uid" not in decoded_token:
            raise HTTPException(status_code=400, detail="Token de refresco no contiene información de usuario válida")
        
        # Asegurarse de que el refresh token no esté expirado
        if datetime.utcnow() > datetime.utcfromtimestamp(decoded_token["exp"]):
            raise HTTPException(status_code=401, detail="Refresh token expirado")

        return decoded_token  # Devolver los datos del token (como user_uid)

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Refresh token inválido")


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=60)):
    """
    Crea un token de acceso JWT con una expiración determinada.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def create_refresh_token(data: dict) -> str:
    """
    Genera un token de refresco con un tiempo de expiración más largo.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def decode_token(token: str) -> Dict:
    """
    Decodifica y valida un token JWT. Lanza excepciones si el token es inválido o está expirado.
    """
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        
        # Validar que el token contiene información requerida
        if "user_uid" not in decoded_token:
            raise HTTPException(status_code=400, detail="Token no contiene información de usuario válida")
        
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")
