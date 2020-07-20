from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from . import oauth2_scheme
from .. import schemas
from ..db.init_db import get_db
from ... import crud

router = APIRouter()


@router.get("/", response_model=List[schemas.items.ItemResponse])
async def get_item(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = await crud.get_items(db, skip, limit)
    for item in items:
        print(item.price)
    return [schemas.items.ItemResponse(title=item.title, price=item.price) for item in items]
