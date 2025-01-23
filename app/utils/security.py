import bcrypt
import jwt
import datetime
from app.core.config import JWT_SECRET, JWT_REFRESH_SECRET

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

def create_access_token(uid_usuario: str, usuario: str) -> str:
    payload = {
        "uid_usuario": uid_usuario,
        "usuario": usuario,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def create_refresh_token(uid_usuario: str) -> str:
    payload = {
        "uid_usuario": uid_usuario,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
    }
    return jwt.encode(payload, JWT_REFRESH_SECRET, algorithm="HS256")
