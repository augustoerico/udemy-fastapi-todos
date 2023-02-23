from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, mapped_column
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    phone_number = Column(String, nullable=True)
    
    todos = relationship("Todo", back_populates="user")

    address_id = Column(Integer, ForeignKey("addresses.id"), nullable=True)
    address = relationship("Address", back_populates="user_address")


class Todo(Base):
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="todos")


class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True, nullable=False)
    address1 = Column(String)
    address2 = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    postal_code = Column(String)

    user_address = relationship("User", back_populates="address")