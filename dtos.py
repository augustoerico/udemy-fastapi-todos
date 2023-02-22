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
