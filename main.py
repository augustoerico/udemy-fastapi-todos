from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import models
from database import engine, SessionLocal
from http_exceptions import NotFoundException
from dtos import CreateTodoDto, UpdateTodoDto
from routers.users_controller import get_current_user
from http_exceptions import UnauthorizedException
from routers import users_controller

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(users_controller.router)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_todo_by_id(id: int, user_id: int, db: Session):
    todo = db.query(models.Todo)\
            .filter(models.Todo.id == id)\
            .filter(models.Todo.user_id == user_id)\
            .first()
    if todo is None:
        raise NotFoundException()
    return todo


@app.post("/todos", status_code=201)
async def create(dto: CreateTodoDto,
                user: dict = Depends(get_current_user),
                db: Session = Depends(get_db)):
    todo = models.Todo()
    todo.title = dto.title
    todo.description = dto.description
    todo.priority = dto.priority
    todo.complete = False
    todo.user_id = user.get('user_id')

    db.add(todo)
    db.commit()
    return {
        "transaction": "successful"
    }


@app.get("/admin/todos")
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Todo).all()


@app.get("/todos")
async def read_all_by_user(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise UnauthorizedException()
    return db.query(models.Todo)\
            .filter(models.Todo.user_id == user.get("user_id"))\
            .all()


@app.get("/todos/{id}")
async def read(id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise UnauthorizedException()
    
    return get_todo_by_id(id, user.get('user_id'), db)


@app.patch("/todos/{id}")
async def update(id: int, dto: UpdateTodoDto,
                    user: dict = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    todo = get_todo_by_id(id, user.get('user_id'), db)
    if todo is None:
        raise NotFoundException()
    if dto.title is not None:
        todo.title = dto.title
    if dto.description is not None:
        todo.description = dto.description
    if dto.priority is not None:
        todo.priority = dto.priority

    db.add(todo)
    db.commit()
    return {
        "transaction": "successful"
    }


@app.delete("/todos/{id}", status_code=204)
async def delete(id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    todo = get_todo_by_id(id, user.get("user_id"), db)
    if todo is None:
        raise NotFoundException()
    
    db.delete(todo)
    db.commit()


@app.post("/todos/{id}/complete")
async def complete(id: int, user: dict = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    todo = get_todo_by_id(id, user.get('user_id'), db)
    todo.complete = True

    db.add(todo)
    db.commit()
    return {
        "transaction": "successful"
    }