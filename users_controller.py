from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm

import models
from dtos import CreateUserDto
from http_exceptions import UnauthorizedException
from database import SessionLocal, engine


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_password_hash(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


def authenticate_user(username, password, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.username == username).first()

    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


@app.post("/users")
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


@app.post("/users/login")
async def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(data.username, data.password, db)
    if not user:
        raise UnauthorizedException()
    return "Aehoo, user authenticated"
