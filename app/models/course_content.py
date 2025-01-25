from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.core.database import Base

class CoursesAndModules(Base):
    __tablename__ = 'courses_and_modules'

    id = Column(Integer, primary_key=True)
    type = Column(String(20), nullable=False)  # 'course' o 'module'
    parent_id = Column(Integer, ForeignKey('courses_and_modules.id', ondelete='CASCADE'))
    name = Column(String(50), nullable=False)
    description = Column(String, nullable=True)

    # Relación recursiva para cursos y módulos
    parent = relationship('CoursesAndModules', remote_side=[id], backref='children')

class LevelsAndLessons(Base):
    __tablename__ = 'levels_and_lessons'

    id = Column(Integer, primary_key=True)
    type = Column(String(20), nullable=False)  # 'level' o 'lesson'
    parent_id = Column(Integer, ForeignKey('levels_and_lessons.id', ondelete='CASCADE'))
    name = Column(String(50), nullable=False)
    description = Column(String, nullable=True)

    parent = relationship('LevelsAndLessons', remote_side=[id], backref='children')

class Exercises(Base):
    __tablename__ = 'exercises'

    id = Column(Integer, primary_key=True)
    lesson_id = Column(Integer, ForeignKey('levels_and_lessons.id', ondelete='CASCADE'))
    type = Column(String(20), nullable=False)
    question = Column(String, nullable=False)
    options = Column(JSONB, nullable=True)
    correct_option = Column(String, nullable=False)

    lesson = relationship('LevelsAndLessons', backref='exercises')
