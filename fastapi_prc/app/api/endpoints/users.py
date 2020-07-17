from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.api import schemas, deps, models

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/", response_model=schemas.users.UserIn)
def create_user(*, db: Session = Depends(deps.get_db), user_info=schemas.UserCreate) -> Any:
    db_obj = models.User(email=user_info.email, password_hash=pwd_context.hash(user_info.password),
                         birth=user_info.birth)
    user = db.query(models.User).filter(models.User.email==user_info.email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="This user already exist"
        )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
