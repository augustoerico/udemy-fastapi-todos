from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import models
from database import engine, SessionLocal
from http_exceptions import NotFoundException
from dtos import CreateTodoDto, UpdateTodoDto


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.post("/todos", status_code=201)
async def create(dto: CreateTodoDto, db: Session = Depends(get_db)):
    todo = models.Todo()
    todo.title = dto.title
    todo.description = dto.description
    todo.priority = dto.priority
    todo.complete = False

    db.add(todo)
    db.commit()
    return {
        "transaction": "successful"
    }


@app.get("/todos")
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Todo).all()


@app.get("/todos/{id}")
async def read(id: int, db: Session = Depends(get_db)):
    todo = db.get(models.Todo, id)
    if todo is None:
        raise NotFoundException()
    return todo


@app.patch("/todos/{id}")
async def update(id: int, dto: UpdateTodoDto, db: Session = Depends(get_db)):
    todo = db.get(models.Todo, id)
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
async def delete(id: int, db: Session = Depends(get_db)):
    todo = db.get(models.Todo, id)
    if todo is None:
        raise NotFoundException()
    
    db.delete(todo)
    db.commit()
