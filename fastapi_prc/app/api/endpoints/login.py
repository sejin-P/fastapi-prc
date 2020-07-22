from datetime import timedelta
from typing import Any

from fastapi import APIRouter, HTTPException, Body
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from fastapi_prc.app import crud, config, security, utils
from fastapi_prc.app.api import schemas
from fastapi_prc.app.api.db.init_db import get_db
from fastapi_prc.app.security import pwd_context
from fastapi_prc.app.utils import generate_password_token, send_reset_password_email

router = APIRouter()


@router.post("/access-token/", response_model=schemas.Token)
async def login_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    user = await crud.user_auth(db=db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTE)
    return {
        "access_token": security.create_access_token(user.email, expires_delta=access_token_expires),
        "token_type": "bearer",
    }


@router.post("/password-recover/", response_model=schemas.Msg)
async def recover_password(user_info: schemas.UserRecover, db: Session = Depends(get_db)):
    user = await crud.get_user_by_email(db, user_info.email)
    if not user:
        raise HTTPException(status_code=400, detail=f"There is no user email {user_info.email}")
    if user.birth != user_info.birth:
        raise HTTPException(status_code=400, detail=f"Birth is not correct")
    new_password = generate_password_token(user_info.email)
    await crud.reset_password(db, email=user_info.email, new_password=new_password)
    send_reset_password_email(email_to=user.email, email=user_info.email, token=new_password)
    return {"message": "New Password email sent"}


@router.post("/password-reset/", response_model=schemas.Msg)
async def reset_password(token: str = Body(...), new_password: str = Body(...), db: Session = Depends(get_db)) -> Any:
    email = utils.verify_token(token)
    if not email:
        raise HTTPException(status_code=404, detail="Unauthorized, login again")
    new_password_hash = pwd_context.hash(new_password)
    await crud.reset_password(db, email, new_password_hash)
    return {"message": "password reset successfully"}

