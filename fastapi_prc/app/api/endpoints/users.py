from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from .. import schemas
from ... import crud

router = APIRouter()


@router.post("/", response_model=schemas.users.UserResponse)
async def create_user(user: schemas.users.UserCreate, db: Session = Depends(crud.get_db)):
    db_user = await crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already exist")
    created = await crud.create_user(db=db, user=user)
    return created


@router.get("/", response_model=List[schemas.users.UserResponse])
async def all_users(skip: int = 0, limit: int = 100, db: Session = Depends(crud.get_db)):
    users = await crud.get_users(db, skip=skip, limit=limit)
    return [schemas.users.UserResponse(id=user.id, email=user.email, birth=user.birth) for user in users]
