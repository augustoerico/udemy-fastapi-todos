from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError
from typing import Optional

import models
from dtos import CreateUserDto
from http_exceptions import UnauthorizedException
from database import SessionLocal, engine


SECRET_KEY = "super-secret-stuff-key"
ALGORITHM = "HS256"


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

models.Base.metadata.create_all(bind=engine)

# oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/users/login")

router = APIRouter()


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


def create_access_token(username: str, user_id: int, expires_delta: Optional[timedelta] = None):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    claims = {"sub": username, "id": user_id, "exp": expire}
    return jwt.encode(claims, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            details = "user data missing"
            raise UnauthorizedException(details=details)
        return {"username": username, "user_id": user_id}
    except JWTError:
        details = "invalid JWT"
        raise UnauthorizedException(details=details)


@router.post("/users")
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


@router.post("/users/login")
async def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(data.username, data.password, db)
    if not user:
        raise UnauthorizedException()
    token_expires = timedelta(minutes=20)
    token = create_access_token(user.username, user.id, expires_delta=token_expires)
    print(token)
    return {"token": token}
