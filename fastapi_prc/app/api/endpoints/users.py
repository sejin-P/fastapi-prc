from typing import Any, List

import sqlalchemy
from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext

from .. import schemas
from ..db import tables
from ..db.init_db import database

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/", response_model=schemas.users.UserIn)
async def create_user(user_info: schemas.UserCreate) -> Any:
    query = tables.Users.select(sqlalchemy.text('email = {}'.format(user_info.email)))
    user = await database.fetch_one(query)
    if user:
        raise HTTPException(
            status_code=400,
            detail="This user already exist"
        )

    query = tables.Users.insert().values(email=user_info.email, password_hash=pwd_context.hash(user_info.password),
                                         birth=user_info.birth)
    last_record_id = await database.execute(query)
    return schemas.users.UserIn(email=user_info.email, birth=user_info.birth)


@router.get("/", response_model=List[schemas.users.UserResponse])
async def all_user() -> Any:
    query = tables.Users.select()
    users = await database.fetch_all(query)
    return users
