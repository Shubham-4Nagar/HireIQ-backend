from fastapi import APIRouter
from pydantic import  BaseModel

from app.services.ai_services import(
    analyze_resume,
    generate_cover_letter,
    generate_interview_questions
)

router = APIRouter()

class AnalyzeRequest(BaseModel):
    resume_text: str
    job_description: str

# Analyze the Upload resume according to the Job description 
@router.post("/analyze-resume")
def analyze_resume_route(request: AnalyzeRequest):

    result = analyze_resume(
        request.resume_text,
        request.job_description
    )

    return {
        "analysis": result
    }

# Generate Cover Letter
@router.post("/generate-cover-letter")
def cover_letter_route(request: AnalyzeRequest):

    result  = generate_cover_letter(
        request.resume_text,
        request.job_description
    )

    return {
        "cover_letter": result
    }

#Generate Interview Questions
@router.post("/generate-interview-questions")
def interview_questions_route(request: AnalyzeRequest):

    result = generate_interview_questions(
        request.resume_text,
        request.job_description
    )

    return{
        "interview_questions": result
    }