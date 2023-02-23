from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

import models
from dtos import CreateUserDto
from database import engine, get_db
from auth import get_password_hash, get_current_user

models.Base.metadata.create_all(bind=engine)


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("")
async def create_user(dto: CreateUserDto, db: Session = Depends(get_db)):
    user = models.User()
    user.username = dto.username
    user.email = dto.email
    user.first_name = dto.first_name
    user.last_name = dto.last_name
    user.hashed_password = get_password_hash(dto.password)
    user.is_active = True

    db.add(user)
    db.commit()

    return user


@router.post("/password")
async def update_password(password: str, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.get(user.get('user_id'))
    print(user)
    pass
