from pydantic import BaseModel
from typing import List, Dict, Any

class Exercise(BaseModel):
    exercise_id: int
    type: str
    question: str
    options: List[str] = []
    correct_option: str = None
    correct_answer: str = None

class Lesson(BaseModel):
    lesson_id: int
    name: str
    exercises: List[Exercise]

class Level(BaseModel):
    level_id: int
    name: str
    lessons: List[Lesson]

class Module(BaseModel):
    module_id: int
    name: str
    levels: List[Level]

class LanguageContent(BaseModel):
    module_id: int
    module_name: str
    levels: List[Dict[str, Any]]
