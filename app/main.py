from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import engine
from app.database.database import Base

#Models
from app.models.user_model import User
from app.models.job_applicattion_model import JobApplication

# Registering the Routes
from app.routes.auth_routes import router as auth_router
from app.routes.resume_routes import router as resume_router
from app.routes.ai_routes import router as ai_router
from app.routes.job_application_routes import router as job_router

app = FastAPI()

#CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

# Registering Router in the main.py file 
app.include_router(auth_router)
app.include_router(resume_router)
app.include_router(ai_router)
app.include_router(job_router)

@app.get("/")
def home():
    return {"message": "HireIQ Backend Running"}