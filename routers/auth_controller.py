from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import timedelta

import models
from http_exceptions import UnauthorizedException
from database import engine, get_db
from auth import authenticate_user, create_access_token


models.Base.metadata.create_all(bind=engine)


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/login")
async def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(data.username, data.password, db)
    if not user:
        raise UnauthorizedException()
    token_expires = timedelta(minutes=20)
    token = create_access_token(user.username, user.id, expires_delta=token_expires)
    print(token)
    return {"token": token}
