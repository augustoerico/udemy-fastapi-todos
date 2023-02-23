from fastapi import FastAPI

import models
from database import engine
from routers import todos_controller, users_controller, auth_controller, admin_controller

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(admin_controller.router)
app.include_router(users_controller.router)
app.include_router(auth_controller.router)
app.include_router(todos_controller.router)
