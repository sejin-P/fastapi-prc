from datetime import date
from pydantic import BaseModel, EmailStr


class UserIn(BaseModel):
    id: int
    email: EmailStr
    password_hash: str
    birth: date

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    birth: date
