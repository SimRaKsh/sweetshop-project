from fastapi import FastAPI, Depends, HTTPException
from fastapi.openapi.utils import get_openapi
from sqlalchemy.orm import Session

from database import Base, engine
from models import User, Sweet
from schemas import UserCreate, UserLogin, SweetBase, SweetUpdate
from utils import hash_password, verify_password, create_token
from auth import get_db, get_user_from_token
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins (React)
    allow_credentials=True,
    allow_methods=["*"],  # allow GET, POST, DELETE, OPTIONS...
    allow_headers=["*"],  # allow Authorization header
)



# ------------------ AUTH --------------------
@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(400, "Username exists")

    hashed = hash_password(user.password)
    new_user = User(username=user.username, password=hashed, is_admin=user.is_admin)
    db.add(new_user)
    db.commit()
    return {"message": "User registered"}


@app.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(401, "Invalid credentials")

    token = create_token({"id": user.id})
    return {"token": token, "is_admin": user.is_admin}


# ------------------ SWEETS CRUD --------------------
@app.post("/sweets")
def add_sweet(sweet: SweetBase, db: Session = Depends(get_db), user=Depends(get_user_from_token)):
    new_sweet = Sweet(**sweet.dict())
    db.add(new_sweet)
    db.commit()
    return {"message": "Sweet added"}


@app.get("/sweets")
def list_sweets(db: Session = Depends(get_db), user=Depends(get_user_from_token)):
    return db.query(Sweet).all()


@app.get("/sweets/search")
def search_sweets(keyword: str, db: Session = Depends(get_db), user=Depends(get_user_from_token)):
    return db.query(Sweet).filter(Sweet.name.contains(keyword)).all()


@app.put("/sweets/{id}")
def update_sweet(id: int, data: SweetUpdate, db: Session = Depends(get_db), user=Depends(get_user_from_token)):
    sweet = db.query(Sweet).filter(Sweet.id == id).first()
    if not sweet:
        raise HTTPException(404, "Sweet not found")

    for k, v in data.dict(exclude_none=True).items():
        setattr(sweet, k, v)

    db.commit()
    return {"message": "Sweet updated"}


@app.delete("/sweets/{id}")
def delete_sweet(id: int, db: Session = Depends(get_db), user=Depends(get_user_from_token)):
    if not user.is_admin:
        raise HTTPException(403, "Admin only")

    sweet = db.query(Sweet).filter(Sweet.id == id).first()
    if not sweet:
        raise HTTPException(404, "Sweet not found")

    db.delete(sweet)
    db.commit()
    return {"message": "Sweet deleted"}


# ------------------ PURCHASE --------------------
@app.post("/sweets/{id}/purchase")
def purchase(id: int, db: Session = Depends(get_db), user=Depends(get_user_from_token)):
    sweet = db.query(Sweet).filter(Sweet.id == id).first()
    if not sweet:
        raise HTTPException(404, "Sweet not found")

    if sweet.quantity <= 0:
        raise HTTPException(400, "Out of stock")

    sweet.quantity -= 1
    db.commit()
    return {"message": "Purchased"}


# ------------------ RESTOCK --------------------
@app.post("/sweets/{id}/restock")
def restock(id: int, amount: int = 10, db: Session = Depends(get_db), user=Depends(get_user_from_token)):
    if not user.is_admin:
        raise HTTPException(403, "Admin only")

    sweet = db.query(Sweet).filter(Sweet.id == id).first()
    sweet.quantity += amount
    db.commit()
    return {"message": "Restocked"}
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Sweet Shop API",
        version="1.0",
        description="API for Sweet Shop Management",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    # Add security requirement to **all** paths
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"BearerAuth": []}])

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

