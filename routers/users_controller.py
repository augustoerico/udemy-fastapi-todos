from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

import models
from dtos import CreateUserDto, UpdatePasswordDto
from database import engine, get_db
from auth import get_password_hash, get_current_user

# models.Base.metadata.create_all(bind=engine) # database already created


router = APIRouter(
    tags=["users"]
)


def get_user(user_id: int, db: Session):
    return db.query(models.User)\
            .filter(models.User.id == user_id)\
            .first()


@router.post("/users")
async def create_user(dto: CreateUserDto, db: Session = Depends(get_db)):
    user = models.User()
    user.username = dto.username
    user.email = dto.email
    user.first_name = dto.first_name
    user.last_name = dto.last_name
    user.hashed_password = get_password_hash(dto.password)
    user.is_active = True
    user.phone_number = dto.phone_number

    db.add(user)
    db.commit()

    return user


@router.get("/user")
async def read_user(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_user(user.get("user_id"), db)


@router.post("/user/password")
async def update_password(dto: UpdatePasswordDto, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user = get_user(user.get("user_id"), db)
    user.hashed_password = get_password_hash(dto.password)
    
    db.add(user)
    db.commit()
    return {"transaction": "successful"}


@router.delete("/user", status_code=204)
async def delete_user(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user = get_user(user.get("user_id"), db)

    db.delete(user)
    db.commit()
