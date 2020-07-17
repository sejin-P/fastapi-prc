from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .api.db import tables
from .api.schemas import users
from .api.db.init_db import SessionLocal

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_user(db: Session, user_id: int):
    return db.query(tables.Users).filter(tables.Users.id == user_id).first()


async def get_user_by_email(db: Session, email: str):
    return db.query(tables.Users).filter(tables.Users.email == email).first()


async def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(tables.Users).offset(skip).limit(limit).all()


async def create_user(db: Session, user: users.UserCreate):
    password_hash = pwd_context.hash(user.password)
    db_user = tables.Users(email=user.email, password_hash=password_hash, birth=user.birth)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user