# app/models/refresh_token.py
from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.user import User  # Importa la clase User

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    token_uid = Column(Integer, primary_key=True, autoincrement=True)
    user_uid = Column(Integer, ForeignKey('users.user_uid'), nullable=False)
    refresh_token = Column(Text, nullable=False)

    # Relación con la clase User
    user = relationship("User", backref="refresh_tokens")
