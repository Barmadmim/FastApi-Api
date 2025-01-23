from fastapi import Depends, HTTPException, Request, APIRouter, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserResponse, TokenRequest, UserCoursesUpdate
from app.core.database import get_db_session
from app.core.tokens import decode_token

userme_router = APIRouter(
    tags=["Datos del Usuario"]
)

@userme_router.post("/me", response_model=UserResponse)
async def get_user_me(request: Request, db: AsyncSession = Depends(get_db_session), token_request: TokenRequest = Body(None)):
    """
    Ruta para obtener los datos del usuario autenticado según el access token.
    El token puede ser proporcionado en las cookies, cabecera Authorization o en el cuerpo JSON.
    """
    # Intentar obtener el token desde las cookies
    token = request.cookies.get("access_token")
    
    if not token:
        # Si no está en las cookies, verificar si el token fue proporcionado en el cuerpo (en formato JSON).
        if token_request and token_request.access_token:
            token = token_request.access_token
        else:
            # Si no se proporciona el token ni en cookies ni en el cuerpo, lanzar error.
            raise HTTPException(status_code=401, detail="Token no proporcionado")
    
    # Decodificar el token y obtener los datos del usuario
    try:
        decoded_token = decode_token(token)
        user_id = decoded_token.get("user_uid")
        if not user_id:
            raise HTTPException(status_code=401, detail="Token inválido")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Error al decodificar el token: {str(e)}")

    # Consultar el usuario en la base de datos por su ID
    async with db.begin():
        result = await db.execute(select(User).filter(User.user_uid == user_id))
        user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Retornar los datos del usuario usando el esquema Pydantic
    return user

@userme_router.patch("/me/courses", response_model=UserResponse)
async def update_courses(request: Request, db: AsyncSession = Depends(get_db_session), courses_update: str = Body(...)):
    """
    Ruta para actualizar los cursos del usuario autenticado.
    El curso proporcionado en la solicitud se agregará a los cursos actuales del usuario.
    """
    # Intentar obtener el token desde las cookies o la cabecera Authorization
    token = request.cookies.get("access_token")  # Obtener el token de las cookies
    if not token:
        # Si no está en las cookies, verificar en la cabecera Authorization
        authorization = request.headers.get("Authorization")
        if authorization:
            token = authorization.split("Bearer ")[-1]  # Obtener el token después de 'Bearer'
    
    if not token:
        raise HTTPException(status_code=401, detail="Token no proporcionado")

    # Decodificar el token y obtener los datos del usuario
    try:
        decoded_token = decode_token(token)
        user_id = decoded_token.get("user_uid")
        if not user_id:
            raise HTTPException(status_code=401, detail="Token inválido")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Error al decodificar el token: {str(e)}")

    # Consultar el usuario en la base de datos por su ID
    async with db.begin():
        result = await db.execute(select(User).filter(User.user_uid == user_id))
        user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Obtener los cursos actuales del usuario
    current_courses = set(user.courses) if user.courses else set()

    # Agregar el nuevo curso a los cursos actuales si no existe ya
    current_courses.add(courses_update)  # Esto agrega el curso sin eliminar los anteriores

    # Actualizar la lista de cursos en el usuario
    user.courses = list(current_courses)  # Convertimos de nuevo a lista

    # Guardar los cambios en la base de datos
    db.add(user)
    await db.commit()

    # Retornar el usuario con los cursos actualizados
    return user
