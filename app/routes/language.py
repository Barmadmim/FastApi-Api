from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends, APIRouter
from app.core.database import get_db_session
from app.core.middlewares import verify_jwt_token
from app.repositories.language_respository import LanguageService
from app.schemas.language_content import LanguageContent, Module, Level, Lesson, Exercise

language_router = APIRouter(
    prefix="/courses",
    tags=["courses"],
    dependencies=[Depends(verify_jwt_token)]
)

@language_router.get("/contenido", response_model=Dict[str, Any])
async def obtener_contenido_por_idioma(
    language: str, db: AsyncSession = Depends(get_db_session)
):
    """
    Devuelve el contenido de un idioma específico con un solo módulo, niveles, lecciones y ejercicios.
    """
    language_service = LanguageService()
    try:
        content = await language_service.get_language_content(language)
    except HTTPException:
        raise HTTPException(status_code=404, detail="Idioma no encontrado")

    # Filtrar el módulo (solo uno por idioma)
    module = content["modules"][0] if content["modules"] else None
    if not module:
        raise HTTPException(status_code=404, detail="No module found for the language")

    # Reestructuramos los datos de manera que solo se devuelvan un módulo
    structured_content = {
        "modules": [
            {
                "module_id": module["module_id"],
                "module_name": module["name"],
                "levels": []
            }
        ]
    }

    for level in module["levels"]:
        level_data = {
            "level_id": level["level_id"],
            "level_name": level["name"],
            "lessons": []
        }
        for lesson in level["lessons"]:
            lesson_data = {
                "lesson_id": lesson["lesson_id"],
                "lesson_name": lesson["name"],
                "lesson_icon": lesson["icon"],
                "exercises": []
            }
            # Aquí manejamos la lista de ejercicios anidada
            for exercise in lesson["exercises"]:  # Directamente iteramos por la lista de ejercicios
                exercise_data = {
                    "exercise_id": exercise["exercise_id"],
                    "type": exercise["type"],
                    "question": exercise["question"],
                    "options": exercise.get("options", []),
                    "audio_url": exercise.get("audio_url", ""),
                    "correct_option": exercise.get("correct_option", ""),
                    "correct_answer": exercise.get("correct_answer", "")
                }
                lesson_data["exercises"].append(exercise_data)

            level_data["lessons"].append(lesson_data)

        structured_content["modules"][0]["levels"].append(level_data)

    return structured_content
