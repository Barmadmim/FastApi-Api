from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

class ExamenModel(Base):
    __tablename__ = "examenes"
    
    id_examen = Column(Integer, primary_key=True, index=True)
    user_uid = Column(Integer, index=True)
    user_name = Column(String)
    exam_type = Column(String)
    res_1 = Column(Float)
    res_2 = Column(Float)
    res_3 = Column(Float)
    res_4 = Column(Float)
    res_5 = Column(Float)
    res_6 = Column(Float)
    res_7 = Column(Float)
    res_8 = Column(Float)
    res_9 = Column(Float)
    res_10 = Column(Float)
    total_percentage = Column(Float)
    creation_date = Column(DateTime, default=datetime.utcnow)
