from sqlalchemy.orm import Session

from .api.db import tables
from .api.schemas import users, items
from .security import pwd_context, verify_password


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


async def user_auth(db: Session, *, email: str, password: str):
    user = await get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user


async def create_user_item(db: Session, item: items.ItemCreate, user_id: int):
    db_item = tables.Item(title=item.title, price=item.price, description=item.description, owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


async def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(tables.Item).offset(skip).limit(limit).all()
