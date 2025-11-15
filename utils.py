from passlib.context import CryptContext
from jose import jwt
import datetime

SECRET_KEY = "secret123"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str):
    return pwd_context.verify(password, hashed)


def create_token(data: dict):
    to_encode = data.copy()
    to_encode["exp"] = datetime.datetime.utcnow() + datetime.timedelta(hours=5)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
