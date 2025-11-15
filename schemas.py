from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    is_admin: bool = False


class UserLogin(BaseModel):
    username: str
    password: str


class SweetBase(BaseModel):
    name: str
    category: str
    price: float
    quantity: int


class SweetUpdate(BaseModel):
    name: str | None = None
    category: str | None = None
    price: float | None = None
    quantity: int | None = None
