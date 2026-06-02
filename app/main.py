from fastapi import FastAPI

from app.database.database import engine
from app.models.user_model import User
from app.database.database import Base
from app.routes.auth_routes import router as auth_router

app = FastAPI()

Base.metadata.create_all(bind=engine)
# Registering Router in the main.py file 
app.include_router(auth_router)

@app.get("/")
def home():
    return {"message": "HireIQ Backend Running"}