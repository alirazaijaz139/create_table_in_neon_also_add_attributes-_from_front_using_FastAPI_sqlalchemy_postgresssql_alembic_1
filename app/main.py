from fastapi import FastAPI
from models import Base, User
from database.database import engine
from routers.user import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="JWT Auth API")

app.include_router(user_router)