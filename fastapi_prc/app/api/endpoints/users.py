from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from .. import schemas
from ..db.init_db import get_db
from ... import crud

router = APIRouter()


@router.post("/", response_model=schemas.users.UserResponse)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = await crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already exist")
    created = await crud.create_user(db=db, user=user)
    return schemas.users.UserResponse(id=created.id, email=created.email, birth=created.birth)


@router.get("/", response_model=List[schemas.users.UserResponse])
async def all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = await crud.get_users(db, skip=skip, limit=limit)
    return [schemas.users.UserResponse(id=user.id, email=user.email, birth=user.birth) for user in users]


@router.post("/{user_id}/items/", response_model=schemas.ItemResponse)
async def create_item_for_user(user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    item = await crud.create_user_item(db, item, user_id)
    return schemas.ItemResponse(title=item.title, price=item.price)
