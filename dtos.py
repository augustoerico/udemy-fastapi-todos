from pydantic import BaseModel, Field
from typing import Optional


class CreateTodoDto(BaseModel):
    title: str = Field(min_length=1)
    description: Optional[str]
    priority: int = Field(gt=0, lt=6)


class UpdateTodoDto(BaseModel):
    title: Optional[str] = Field(min_length=1)
    description: Optional[str]
    priority: Optional[int] = Field(gt=0, lt=6)


class CreateUserDto(BaseModel):
    username: str = Field(min_length=1)
    email: Optional[str]
    first_name: str
    last_name: str
    password: str = Field(min_length=1)
    phone_number: Optional[str]


class UpdatePasswordDto(BaseModel):
    password: str = Field(min_length=3)


class CreateAddressDto(BaseModel):
    address1: str
    address2: str
    city: str
    state: str
    country: str
    postal_code: str
