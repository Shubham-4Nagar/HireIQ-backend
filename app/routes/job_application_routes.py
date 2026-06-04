from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm  import Session
from uuid import UUID
from datetime import datetime, timezone
from app.database.database import get_db
from app.models.job_applicattion_model import JobApplication
from app.schemas.job_application_schema import(
    CreateJobApplication,
    JobApplicationResponse,
    UpdateJobStatus
)
from app.auth.oauth2 import get_current_user
from app.models.user_model import User

router = APIRouter(
    prefix="/applications",
    tags=["Job Applications"]
)

# Saving a New application
@router.post("/", response_model=JobApplicationResponse)
def create_application(
    application: CreateJobApplication,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) 
):
    new_application = JobApplication(
        user_id = current_user.user_id,
        job_title = application.job_title,
        company = application.company,
        job_description = application.job_description,
        match_score = application.match_score,
        analysis = application.analysis,
        status = application.status 
    )

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return new_application

# Get all my applications
@router.get("/", response_model=list[JobApplicationResponse])
def get_all_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    applications = db.query(JobApplication).filter(
        JobApplication.user_id == current_user.user_id
    ).all()

    return applications

#Get job application by ID
@router.get("/{job_id}", response_model=JobApplicationResponse)
def get_application_by_id(
    job_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    application = db.query(JobApplication).filter(
        JobApplication.job_id == job_id,
        JobApplication.user_id == current_user.user_id
    ).first()

    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    return application

#Update application status
@router.patch("/{job_id}", response_model=JobApplicationResponse)
def update_status(
    job_id: UUID,
    updated: UpdateJobStatus,
    db: Session = Depends(get_db),
    current_user: User =Depends(get_current_user)
):
    application = db.query(JobApplication).filter(
        JobApplication.job_id == job_id,
        JobApplication.user_id == current_user.user_id
    ).first()

    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found "
        )
    
    application.status = updated.status
    db.commit()
    db.refresh(application)

    return application

# Delete an Application
@router.delete("/{job_id}")
def delete_application(
    job_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    application = db.query(JobApplication).filter(
        JobApplication.job_id == job_id,
        JobApplication.user_id == current_user.user_id,
        JobApplication.is_deleted == False
    ).first()

    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not Found"
        )
    
    application.is_deleted == True
    application.deleted_at = datetime.now(timezone.utc)
    db.commit()

    return{
        "message": "Application Deleted successfully"
    }
    
