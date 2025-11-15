from fastapi import Depends, HTTPException, Header
from jose import jwt, JWTError
from utils import SECRET_KEY, ALGORITHM
from database import SessionLocal
from models import User

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Extract user from Bearer token
def get_user_from_token(authorization: str = Header(None), db=Depends(get_db)):
    if authorization is None:
        raise HTTPException(401, "Missing Authorization header")

    try:
        scheme, token = authorization.split()

        if scheme.lower() != "bearer":
            raise HTTPException(401, "Invalid Authorization scheme")

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = db.query(User).filter(User.id == payload["id"]).first()

        if not user:
            raise HTTPException(401, "User not found")

        return user

    except Exception:
        raise HTTPException(401, "Invalid or expired token")
