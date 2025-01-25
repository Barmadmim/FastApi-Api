# schemas/examenes.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ExamSchema(BaseModel):
    exam_type: str
    res_1: float
    res_2: float
    res_3: float
    res_4: float
    res_5: float
    res_6: float
    res_7: float
    res_8: float
    res_9: float
    res_10: float
    total_percentage: float

class ExamResponse(ExamSchema):
    id_examen: int
    user_uid: int
    user_name: str
    creation_date: datetime

    class Config:
        from_attributes = True
