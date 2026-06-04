from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class CreateJobApplication(BaseModel):
    job_title: str
    company: str
    job_description: str
    match_score: Optional[str] = None
    analysis: Optional[str] = None
    status: Optional[str] = "Applied"

class UpdateJobStatus(BaseModel):
    status: str

class JobApplicationResponse(BaseModel):
    job_id: UUID
    user_id: UUID
    job_title: str
    company: str
    job_description: str
    match_score: Optional[str] = None
    analysis: Optional[str] = None
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True
