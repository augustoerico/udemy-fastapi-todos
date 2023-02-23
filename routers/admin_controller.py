from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

import models
from database import get_db
from http_exceptions import UnauthorizedException


ADMIN_API_KEY =  'some-api-key'


async def get_api_key(x_api_key: str = Header(...)):
    if x_api_key != ADMIN_API_KEY:
        raise UnauthorizedException()

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_api_key)]
)


@router.get("/users")
async def read_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@router.get("/todos")
async def read_all_todos(db: Session = Depends(get_db)):
    return db.query(models.Todo).all()
