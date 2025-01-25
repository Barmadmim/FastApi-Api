from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from fastapi import HTTPException, Depends, APIRouter
from app.core.database import get_db_session
from app.core.middlewares import verify_jwt_token
from app.models.course_content import CoursesAndModules, LevelsAndLessons, Exercises

course_router = APIRouter(prefix="/courses", tags=["courses"])

@course_router.get("/content", response_model=Dict[str, Any])
async def course_content(
    course: str,
    db: AsyncSession = Depends(get_db_session),
    token: str = Depends(verify_jwt_token),
):
    """
    Devuelve el contenido de un curso específico con módulos, niveles, lecciones y ejercicios.
    """

    if not token:
        raise HTTPException(status_code=401, detail="Token inválido o no proporcionado")

    # Buscar curso y sus módulos
    result = await db.execute(
        text("""SELECT * FROM courses_and_modules WHERE name = :course_name AND type = 'course'"""),
        {"course_name": course},
    )
    course_data = result.fetchone()

    if not course_data:
        raise HTTPException(status_code=404, detail="Curso no encontrado")

    # Obtener módulos del curso
    modules_result = await db.execute(
        text("""SELECT * FROM courses_and_modules WHERE parent_id = :course_id AND type = 'module'"""),
        {"course_id": course_data.id},
    )
    modules = modules_result.fetchall()

    # Construir la respuesta
    structured_content = {"course_name": course_data.name, "modules": []}

    for module in modules:
        module_data = {"module_id": module.id, "module_name": module.name, "levels": []}

        # Obtener niveles y lecciones para cada módulo
        levels_result = await db.execute(
            text("""
                SELECT l.id, l.name, l.description
                FROM levels_and_lessons l
                WHERE l.parent_id = :module_id AND l.type = 'level'
            """),
            {"module_id": module.id},
        )
        levels = levels_result.fetchall()

        if not levels:
            print(f"No levels found for module {module.name}")  # Depuración si no se encuentran niveles

        for level in levels:
            level_data = {"level_id": level.id, "level_name": level.name, "lessons": []}

            # Obtener lecciones para cada nivel
            lessons_result = await db.execute(
                text("""
                    SELECT ll.id, ll.name, ll.description
                    FROM levels_and_lessons ll
                    WHERE ll.parent_id = :level_id AND ll.type = 'lesson'
                """),
                {"level_id": level.id},
            )
            lessons = lessons_result.fetchall()

            if not lessons:
                print(f"No lessons found for level {level.name}")  # Depuración si no se encuentran lecciones

            for lesson in lessons:
                lesson_data = {
                    "lesson_id": lesson.id,
                    "lesson_name": lesson.name,
                    "exercises": [],
                }

                # Obtener ejercicios para cada lección
                exercises_result = await db.execute(
                    text("""
                        SELECT * FROM exercises
                        WHERE lesson_id = :lesson_id
                    """),
                    {"lesson_id": lesson.id},
                )
                exercises = exercises_result.fetchall()

                for exercise in exercises:
                    exercise_data = {
                        "exercise_id": exercise.id,
                        "type": exercise.type,
                        "question": exercise.question,
                        "options": exercise.options,
                        "correct_option": exercise.correct_option,
                    }
                    lesson_data["exercises"].append(exercise_data)

                level_data["lessons"].append(lesson_data)

            module_data["levels"].append(level_data)

        structured_content["modules"].append(module_data)

    return structured_content

@course_router.post("/content", response_model=Dict[str, Any])
async def add_course_content(
    course_name: str,
    modules: list[Dict[str, Any]],  # Esperamos recibir módulos con niveles y lecciones
    db: AsyncSession = Depends(get_db_session),
    token: str = Depends(verify_jwt_token),
):
    """
    Agrega un nuevo curso con módulos, niveles, lecciones y ejercicios.
    """

    if not token:
        raise HTTPException(status_code=401, detail="Token inválido o no proporcionado")

    # Crear el curso
    new_course = CoursesAndModules(type="course", name=course_name)
    db.add(new_course)
    await db.commit()

    # Agregar los módulos
    for module in modules:
        new_module = CoursesAndModules(
            type="module",
            parent_id=new_course.id,
            name=module["name"],
            description=module.get("description", ""),
        )
        db.add(new_module)
        await db.commit()

        # Agregar niveles y lecciones
        for level in module.get("levels", []):
            new_level = LevelsAndLessons(
                type="level",
                parent_id=new_module.id,
                name=level["name"],
                description=level.get("description", ""),
            )
            db.add(new_level)
            await db.commit()

            for lesson in level.get("lessons", []):
                new_lesson = LevelsAndLessons(
                    type="lesson",
                    parent_id=new_level.id,
                    name=lesson["name"],
                    description=lesson.get("description", ""),
                )
                db.add(new_lesson)
                await db.commit()

                # Agregar ejercicios
                for exercise in lesson.get("exercises", []):
                    new_exercise = Exercises(
                        lesson_id=new_lesson.id,
                        type=exercise["type"],
                        question=exercise["question"],
                        options=exercise.get("options", []),
                        correct_option=exercise["correct_option"],
                    )
                    db.add(new_exercise)
                    await db.commit()

    return {"message": "Contenido del curso agregado exitosamente"}

@course_router.put("/content", response_model=Dict[str, Any])
async def update_course_content(
    course: str,
    content: Dict[str, Any],
    db: AsyncSession = Depends(get_db_session),
    token: str = Depends(verify_jwt_token),
):
    """
    Actualiza el contenido de un curso para un idioma específico.
    """

    if not token:
        raise HTTPException(status_code=401, detail="Token inválido o no proporcionado")

    # Verifica si el contenido ya existe para el idioma
    existing_course = await db.execute(
        text("SELECT * FROM course_content WHERE language = :language"),
        {"language": course},
    )
    existing_course = existing_course.fetchone()

    if not existing_course:
        raise HTTPException(
            status_code=404, detail="Contenido no encontrado para este curso"
        )

    # Actualizamos el contenido
    await db.execute(
        text("UPDATE course_content SET content = :content WHERE language = :language"),
        {"content": content, "language": course},
    )
    await db.commit()

    return {
        "message": "Contenido de curso actualizado exitosamente",
        "language": course,
    }

@course_router.put("/content/course/{course_id}", response_model=Dict[str, Any])
async def update_course(
    course_id: int,
    course_name: str,
    description: str = "",
    db: AsyncSession = Depends(get_db_session),
    token: str = Depends(verify_jwt_token),
):
    """
    Actualiza el nombre y la descripción de un curso.
    """

    if not token:
        raise HTTPException(status_code=401, detail="Token inválido o no proporcionado")

    # Buscar el curso
    course = await db.execute(
        text("""SELECT * FROM courses_and_modules WHERE id = :course_id AND type = 'course'"""),
        {"course_id": course_id},
    )
    course_data = course.fetchone()

    if not course_data:
        raise HTTPException(status_code=404, detail="Curso no encontrado")

    # Actualizar curso
    course_data.name = course_name
    course_data.description = description
    await db.commit()

    return {"message": "Curso actualizado exitosamente"}

@course_router.put("/content/module/{module_id}", response_model=Dict[str, Any])
async def update_module(
    module_id: int,
    module_name: str,
    description: str = "",
    db: AsyncSession = Depends(get_db_session),
    token: str = Depends(verify_jwt_token),
):
    """
    Actualiza el nombre y la descripción de un módulo.
    """

    if not token:
        raise HTTPException(status_code=401, detail="Token inválido o no proporcionado")

    # Buscar el módulo
    module = await db.execute(
        text("""SELECT * FROM courses_and_modules WHERE id = :module_id AND type = 'module'"""),
        {"module_id": module_id},
    )
    module_data = module.fetchone()

    if not module_data:
        raise HTTPException(status_code=404, detail="Módulo no encontrado")

    # Actualizar módulo
    module_data.name = module_name
    module_data.description = description
    await db.commit()

    return {"message": "Módulo actualizado exitosamente"}

@course_router.put("/content/level/{level_id}", response_model=Dict[str, Any])
async def update_level(
    level_id: int,
    level_name: str,
    description: str = "",
    db: AsyncSession = Depends(get_db_session),
    token: str = Depends(verify_jwt_token),
):
    """
    Actualiza el nombre y la descripción de un nivel.
    """

    if not token:
        raise HTTPException(status_code=401, detail="Token inválido o no proporcionado")

    # Buscar el nivel
    level = await db.execute(
        text("""SELECT * FROM levels_and_lessons WHERE id = :level_id AND type = 'level'"""),
        {"level_id": level_id},
    )
    level_data = level.fetchone()

    if not level_data:
        raise HTTPException(status_code=404, detail="Nivel no encontrado")

    # Actualizar nivel
    level_data.name = level_name
    level_data.description = description
    await db.commit()

    return {"message": "Nivel actualizado exitosamente"}

@course_router.put("/content/lesson/{lesson_id}", response_model=Dict[str, Any])
async def update_lesson(
    lesson_id: int,
    lesson_name: str,
    description: str = "",
    db: AsyncSession = Depends(get_db_session),
    token: str = Depends(verify_jwt_token),
):
    """
    Actualiza el nombre y la descripción de una lección.
    """

    if not token:
        raise HTTPException(status_code=401, detail="Token inválido o no proporcionado")

    # Buscar la lección
    lesson = await db.execute(
        text("""SELECT * FROM levels_and_lessons WHERE id = :lesson_id AND type = 'lesson'"""),
        {"lesson_id": lesson_id},
    )
    lesson_data = lesson.fetchone()

    if not lesson_data:
        raise HTTPException(status_code=404, detail="Lección no encontrada")

    # Actualizar lección
    lesson_data.name = lesson_name
    lesson_data.description = description
    await db.commit()

    return {"message": "Lección actualizada exitosamente"}

@course_router.put("/content/exercise/{exercise_id}", response_model=Dict[str, Any])
async def update_exercise(
    exercise_id: int,
    type: str,
    question: str,
    options: list = [],
    correct_option: str = "",
    db: AsyncSession = Depends(get_db_session),
    token: str = Depends(verify_jwt_token),
):
    """
    Actualiza un ejercicio específico de una lección.
    """

    if not token:
        raise HTTPException(status_code=401, detail="Token inválido o no proporcionado")

    # Buscar ejercicio
    exercise = await db.execute(
        text("""SELECT * FROM exercises WHERE id = :exercise_id"""),
        {"exercise_id": exercise_id},
    )
    exercise_data = exercise.fetchone()

    if not exercise_data:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")

    # Actualizar ejercicio
    exercise_data.type = type
    exercise_data.question = question
    exercise_data.options = options
    exercise_data.correct_option = correct_option
    await db.commit()

    return {"message": "Ejercicio actualizado exitosamente"}

@course_router.get("/modules", response_model=Dict[str, Any])
async def get_all_modules(
    db: AsyncSession = Depends(get_db_session),
    token: str = Depends(verify_jwt_token),
):
    """
    Devuelve todos los módulos de todos los cursos.
    """

    if not token:
        raise HTTPException(status_code=401, detail="Token inválido o no proporcionado")

    # Obtener todos los módulos
    modules_result = await db.execute(
        text("""SELECT * FROM courses_and_modules WHERE type = 'module'""")
    )
    modules = modules_result.fetchall()

    if not modules:
        raise HTTPException(status_code=404, detail="No hay módulos disponibles")

    modules_data = [{"module_id": module.id, "module_name": module.name, "description": module.description} for module in modules]

    return {"modules": modules_data}

@course_router.get("/levels", response_model=Dict[str, Any])
async def get_all_levels(
    db: AsyncSession = Depends(get_db_session),
    token: str = Depends(verify_jwt_token),
):
    """
    Devuelve todos los niveles de todos los módulos.
    """

    if not token:
        raise HTTPException(status_code=401, detail="Token inválido o no proporcionado")

    # Obtener todos los niveles
    levels_result = await db.execute(
        text("""SELECT * FROM levels_and_lessons WHERE type = 'level'""")
    )
    levels = levels_result.fetchall()

    if not levels:
        raise HTTPException(status_code=404, detail="No hay niveles disponibles")

    levels_data = [{"level_id": level.id, "level_name": level.name, "description": level.description} for level in levels]

    return {"levels": levels_data}

@course_router.get("/exercises", response_model=Dict[str, Any])
async def get_all_exercises(
    db: AsyncSession = Depends(get_db_session),
    token: str = Depends(verify_jwt_token),
):
    """
    Devuelve todos los ejercicios de todas las lecciones.
    """

    if not token:
        raise HTTPException(status_code=401, detail="Token inválido o no proporcionado")

    # Obtener todos los ejercicios
    exercises_result = await db.execute(
        text("""SELECT * FROM exercises""")
    )
    exercises = exercises_result.fetchall()

    if not exercises:
        raise HTTPException(status_code=404, detail="No hay ejercicios disponibles")

    exercises_data = [
        {
            "exercise_id": exercise.id,
            "type": exercise.type,
            "question": exercise.question,
            "options": exercise.options,
            "correct_option": exercise.correct_option,
        }
        for exercise in exercises
    ]

    return {"exercises": exercises_data}

@course_router.get("/modules/{course_id}", response_model=Dict[str, Any])
async def get_modules_by_course(
    course_id: int,
    db: AsyncSession = Depends(get_db_session),
    token: str = Depends(verify_jwt_token),
):
    """
    Devuelve todos los módulos de un curso específico.
    """

    if not token:
        raise HTTPException(status_code=401, detail="Token inválido o no proporcionado")

    # Obtener los módulos de un curso específico
    modules_result = await db.execute(
        text("""SELECT * FROM courses_and_modules WHERE parent_id = :course_id AND type = 'module'"""),
        {"course_id": course_id},
    )
    modules = modules_result.fetchall()

    if not modules:
        raise HTTPException(status_code=404, detail="No hay módulos disponibles para este curso")

    modules_data = [{"module_id": module.id, "module_name": module.name, "description": module.description} for module in modules]

    return {"modules": modules_data}

@course_router.delete("/module/{module_id}", response_model=Dict[str, Any])
async def delete_module(
    module_id: int,
    db: AsyncSession = Depends(get_db_session),
    token: str = Depends(verify_jwt_token),
):
    """
    Elimina un módulo específico.
    """

    if not token:
        raise HTTPException(status_code=401, detail="Token inválido o no proporcionado")

    # Buscar el módulo en la base de datos
    module_result = await db.execute(
        text("""SELECT * FROM courses_and_modules WHERE id = :module_id AND type = 'module'"""),
        {"module_id": module_id},
    )
    module = module_result.fetchone()

    if not module:
        raise HTTPException(status_code=404, detail="Módulo no encontrado")

    # Eliminar el módulo
    await db.execute(
        text("""DELETE FROM courses_and_modules WHERE id = :module_id"""),
        {"module_id": module_id},
    )
    await db.commit()

    return {"message": "Módulo eliminado exitosamente"}

@course_router.delete("/level/{level_id}", response_model=Dict[str, Any])
async def delete_level(
    level_id: int,
    db: AsyncSession = Depends(get_db_session),
    token: str = Depends(verify_jwt_token),
):
    """
    Elimina un nivel específico.
    """

    if not token:
        raise HTTPException(status_code=401, detail="Token inválido o no proporcionado")

    # Buscar el nivel en la base de datos
    level_result = await db.execute(
        text("""SELECT * FROM levels_and_lessons WHERE id = :level_id AND type = 'level'"""),
        {"level_id": level_id},
    )
    level = level_result.fetchone()

    if not level:
        raise HTTPException(status_code=404, detail="Nivel no encontrado")

    # Eliminar el nivel
    await db.execute(
        text("""DELETE FROM levels_and_lessons WHERE id = :level_id"""),
        {"level_id": level_id},
    )
    await db.commit()

    return {"message": "Nivel eliminado exitosamente"}

@course_router.delete("/lesson/{lesson_id}", response_model=Dict[str, Any])
async def delete_lesson(
    lesson_id: int,
    db: AsyncSession = Depends(get_db_session),
    token: str = Depends(verify_jwt_token),
):
    """
    Elimina una lección específica.
    """

    if not token:
        raise HTTPException(status_code=401, detail="Token inválido o no proporcionado")

    # Buscar la lección en la base de datos
    lesson_result = await db.execute(
        text("""SELECT * FROM levels_and_lessons WHERE id = :lesson_id AND type = 'lesson'"""),
        {"lesson_id": lesson_id},
    )
    lesson = lesson_result.fetchone()

    if not lesson:
        raise HTTPException(status_code=404, detail="Lección no encontrada")

    # Eliminar la lección
    await db.execute(
        text("""DELETE FROM levels_and_lessons WHERE id = :lesson_id"""),
        {"lesson_id": lesson_id},
    )
    await db.commit()

    return {"message": "Lección eliminada exitosamente"}

@course_router.delete("/exercise/{exercise_id}", response_model=Dict[str, Any])
async def delete_exercise(
    exercise_id: int,
    db: AsyncSession = Depends(get_db_session),
    token: str = Depends(verify_jwt_token),
):
    """
    Elimina un ejercicio específico.
    """

    if not token:
        raise HTTPException(status_code=401, detail="Token inválido o no proporcionado")

    # Buscar el ejercicio en la base de datos
    exercise_result = await db.execute(
        text("""SELECT * FROM exercises WHERE id = :exercise_id"""),
        {"exercise_id": exercise_id},
    )
    exercise = exercise_result.fetchone()

    if not exercise:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")

    # Eliminar el ejercicio
    await db.execute(
        text("""DELETE FROM exercises WHERE id = :exercise_id"""),
        {"exercise_id": exercise_id},
    )
    await db.commit()

    return {"message": "Ejercicio eliminado exitosamente"}

@course_router.post("/module", response_model=Dict[str, Any])
async def add_module(
    module_data: Dict[str, Any],
    db: AsyncSession = Depends(get_db_session),
    token: str = Depends(verify_jwt_token),
):
    """
    Agrega un nuevo módulo a un curso específico.
    """

    if not token:
        raise HTTPException(status_code=401, detail="Token inválido o no proporcionado")

    course_name = module_data["course_name"]
    module_name = module_data["name"]
    module_description = module_data.get("description", "")

    # Buscar curso al que se le agregará el módulo
    result = await db.execute(
        text("""SELECT * FROM courses_and_modules WHERE name = :course_name AND type = 'course'"""),
        {"course_name": course_name},
    )
    course = result.fetchone()

    if not course:
        raise HTTPException(status_code=404, detail="Curso no encontrado")

    # Crear el módulo
    new_module = CoursesAndModules(
        type="module",
        parent_id=course.id,
        name=module_name,
        description=module_description,
    )
    db.add(new_module)
    await db.commit()

    return {"message": "Módulo agregado exitosamente", "module_id": new_module.id}

@course_router.post("/level", response_model=Dict[str, Any])
async def add_level(
    level_data: Dict[str, Any],
    db: AsyncSession = Depends(get_db_session),
    token: str = Depends(verify_jwt_token),
):
    """
    Agrega un nuevo nivel a un módulo específico.
    """

    if not token:
        raise HTTPException(status_code=401, detail="Token inválido o no proporcionado")

    module_id = level_data["module_id"]
    level_name = level_data["name"]
    level_description = level_data.get("description", "")

    # Buscar módulo al que se le agregará el nivel
    result = await db.execute(
        text("""SELECT * FROM courses_and_modules WHERE id = :module_id AND type = 'module'"""),
        {"module_id": module_id},
    )
    module = result.fetchone()

    if not module:
        raise HTTPException(status_code=404, detail="Módulo no encontrado")

    # Crear el nivel
    new_level = LevelsAndLessons(
        type="level",
        parent_id=module.id,
        name=level_name,
        description=level_description,
    )
    db.add(new_level)
    await db.commit()

    return {"message": "Nivel agregado exitosamente", "level_id": new_level.id}

@course_router.post("/lesson", response_model=Dict[str, Any])
async def add_lesson(
    lesson_data: Dict[str, Any],
    db: AsyncSession = Depends(get_db_session),
    token: str = Depends(verify_jwt_token),
):
    """
    Agrega una nueva lección a un nivel específico.
    """

    if not token:
        raise HTTPException(status_code=401, detail="Token inválido o no proporcionado")

    level_id = lesson_data["level_id"]
    lesson_name = lesson_data["name"]
    lesson_description = lesson_data.get("description", "")

    # Buscar nivel al que se le agregará la lección
    result = await db.execute(
        text("""SELECT * FROM levels_and_lessons WHERE id = :level_id AND type = 'level'"""),
        {"level_id": level_id},
    )
    level = result.fetchone()

    if not level:
        raise HTTPException(status_code=404, detail="Nivel no encontrado")

    # Crear la lección
    new_lesson = LevelsAndLessons(
        type="lesson",
        parent_id=level.id,
        name=lesson_name,
        description=lesson_description,
    )
    db.add(new_lesson)
    await db.commit()

    return {"message": "Lección agregada exitosamente", "lesson_id": new_lesson.id}

@course_router.post("/exercise", response_model=Dict[str, Any])
async def add_exercise(
    exercise_data: Dict[str, Any],
    db: AsyncSession = Depends(get_db_session),
    token: str = Depends(verify_jwt_token),
):
    """
    Agrega un nuevo ejercicio a una lección específica.
    """

    if not token:
        raise HTTPException(status_code=401, detail="Token inválido o no proporcionado")

    lesson_id = exercise_data["lesson_id"]
    exercise_type = exercise_data["type"]
    question = exercise_data["question"]
    options = exercise_data.get("options", [])
    correct_option = exercise_data["correct_option"]

    # Buscar lección a la que se le agregará el ejercicio
    result = await db.execute(
        text("""SELECT * FROM levels_and_lessons WHERE id = :lesson_id AND type = 'lesson'"""),
        {"lesson_id": lesson_id},
    )
    lesson = result.fetchone()

    if not lesson:
        raise HTTPException(status_code=404, detail="Lección no encontrada")

    # Crear el ejercicio
    new_exercise = Exercises(
        lesson_id=lesson.id,
        type=exercise_type,
        question=question,
        options=options,
        correct_option=correct_option,
    )
    db.add(new_exercise)
    await db.commit()

    return {"message": "Ejercicio agregado exitosamente", "exercise_id": new_exercise.id}
