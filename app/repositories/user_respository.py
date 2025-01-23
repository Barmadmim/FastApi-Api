from app.models.user import User, RefreshToken
from app.schemas.auth import RegisterRequest, LoginRequest
from app.core.tokens import create_access_token, create_refresh_token, decode_token
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from sqlalchemy.sql import text
from fastapi import HTTPException, Response
from passlib.context import CryptContext
from datetime import timedelta, datetime
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Función para eliminar tokens expirados
async def delete_expired_tokens(db: AsyncSession):
    current_time = datetime.utcnow()
    await db.execute(
        text("DELETE FROM refresh_tokens WHERE expires_at < :current_time"),
        {"current_time": current_time}
    )
    await db.commit()

async def create_user(register_request: RegisterRequest, response: Response, db: AsyncSession):
    """
    Lógica para registrar un nuevo usuario y generar un token de acceso.
    """
    # Verificar si el usuario ya existe
    stmt = select(User).where(User.username == register_request.username)
    result = await db.execute(stmt)
    
    existing_user = result.scalars().first() if result else None
    
    if existing_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe.")
    
    # Convertir language_skills a formato JSON
    language_skills_json = None
    if register_request.language_skills:
        language_skills_json = [
            {
                "language": skill.language,
                "reading": skill.reading.value,
                "writing": skill.writing.value,
                "listening": skill.listening.value,
                "speaking": skill.speaking.value
            }
            for skill in register_request.language_skills
        ]

    # Convertir courses a lista de strings
    courses_list = None
    if register_request.courses:
        courses_list = [course.value for course in register_request.courses]

    # Crear y guardar el nuevo usuario
    hashed_password = pwd_context.hash(register_request.password)
    new_user = User(
        username=register_request.username,
        last_name=register_request.last_name,
        password=hashed_password,
        phone_number=register_request.phone_number,
        age=register_request.age,
        gender=register_request.gender,
        institucion=register_request.institucion,
        grade=register_request.grade,
        country_origin=register_request.country_origin,
        language_skills=language_skills_json,
        courses=courses_list,
        email=register_request.email,
        photo=register_request.photo,
        creation_date=datetime.utcnow(),
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # Generar el token de acceso para el usuario registrado
    token_data = {
        "user_uid": new_user.user_uid,   # ID único del usuario
        "username": new_user.username,   # Nombre de usuario
        "last_name": new_user.last_name, # Apellido del usuario
    }
    access_token = create_access_token(data=token_data, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))

    # Generar un refresh token
    refresh_token = create_refresh_token(data={"sub": new_user.username, "user_uid": new_user.user_uid})

    # Calcular la fecha de expiración del refresh token
    expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    # Eliminar los tokens antiguos del usuario (por si existe algún problema previo) y expirados
    await db.execute(delete(RefreshToken).where(RefreshToken.user_uid == new_user.user_uid))
    await delete_expired_tokens(db)

    # Guardar el refresh token en la base de datos
    new_refresh_token = RefreshToken(user_uid=new_user.user_uid, refresh_token=refresh_token, expires_at=expires_at)
    db.add(new_refresh_token)
    await db.commit()

    # Establecer el token en las cookies
    response.set_cookie(
        key="access_token", 
        value=access_token, 
        httponly=True,
        secure=False,  # Usar secure=True en producción con HTTPS
        samesite="Strict"
    )

    # Establecer el refresh_token en las cookies
    response.set_cookie(
        key="refresh_token", 
        value=refresh_token, 
        httponly=True,
        secure=False,  # Usar secure=True en producción con HTTPS
        samesite="Strict"
    )
    
    return {
        "message": "Usuario registrado exitosamente",
        "user_id": new_user.user_uid,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

async def authenticate_user(login_request: LoginRequest, response: Response, db: AsyncSession):
    # Buscar usuario
    stmt = select(User).where(User.username == login_request.username)
    result = await db.execute(stmt)
    user = result.scalar()

    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado.")

    if not pwd_context.verify(login_request.password, user.password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas.")
    
    # Datos para el token de acceso
    token_data = {"user_uid": user.user_uid, "username": user.username, "last_name": user.last_name}

    # Crear el token de acceso
    access_token = create_access_token(data=token_data, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    
    # Crear el token de refresco
    refresh_token = create_refresh_token(data={"sub": user.username, "user_uid": user.user_uid})
    
    # Calcular la fecha de expiración del refresh token
    expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    # Eliminar tokens antiguos y Expirados
    await db.execute(delete(RefreshToken).where(RefreshToken.user_uid == user.user_uid))
    await delete_expired_tokens(db)

    # Guardar el nuevo refresh token con expires_at
    new_refresh_token = RefreshToken(user_uid=user.user_uid, refresh_token=refresh_token, expires_at=expires_at)
    db.add(new_refresh_token)
    await db.commit()

    # Establecer cookies
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=False, samesite="Strict")
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure=False, samesite="Strict")

    return {
        "access_token": access_token, 
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


async def refresh_user_token(refresh_token: str, db: AsyncSession):
    """
    Lógica para refrescar un token de acceso.
    """
    try:
        # Decodificar el token de refresco
        payload = decode_token(refresh_token)
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Token inválido.")
        
        # Verificar que el usuario exista
        stmt = select(User).where(User.username == username)
        result = await db.execute(stmt)
        user = result.scalar()

        if not user:
            raise HTTPException(status_code=401, detail="Usuario no encontrado.")
        
        # Verificar que el refresh token esté en la base de datos
        refresh_token_entry = await db.execute(select(RefreshToken).where(RefreshToken.user_uid == user.user_uid))
        refresh_token_entry = refresh_token_entry.scalar()

        if not refresh_token_entry:
            raise HTTPException(status_code=401, detail="No se encontró el refresh token en la base de datos.")

        if refresh_token_entry.refresh_token.strip() != refresh_token.strip():
            print(f"Token esperado: {refresh_token_entry.refresh_token.strip()}")
            print(f"Token recibido: {refresh_token.strip()}")
            raise HTTPException(status_code=401, detail="Refresh token inválido.")

        
        # Crear un nuevo token de acceso
        new_access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        
        # Regresar el nuevo access token
        return {"access_token": new_access_token, "token_type": "bearer"}
    
    except Exception as e:
        import traceback
        print("Traceback completo del error:")
        print(traceback.format_exc())  # Imprimir el traceback completo para depuración
        print(f"Error al refrescar el token: {e}")
        raise HTTPException(status_code=401, detail=f"Error específico: {e}") from e

