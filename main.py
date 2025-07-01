from fastapi import FastAPI
from database import Base, engine
from models import Task
import routers.tasks

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Management API")

app.include_router(routers.tasks.router)