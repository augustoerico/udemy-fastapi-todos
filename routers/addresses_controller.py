from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine, get_db
from dtos import CreateAddressDto
from auth import get_current_user
from .users_controller import get_user


router = APIRouter(
    prefix="/address",
    tags=['address']
)


@router.post('/')
async def create(dto: CreateAddressDto, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    address = models.Address()
    address.address1 = dto.address1
    address.address2 = dto.address2
    address.city = dto.city
    address.state = dto.state
    address.country = dto.country
    address.postal_code = dto.postal_code

    db.add(address)
    db.flush()

    user = get_user(user.get('user_id'), db)
    user.address_id = address.id

    db.add(user)
    db.commit()

    return {'transaction': 'successful'}
