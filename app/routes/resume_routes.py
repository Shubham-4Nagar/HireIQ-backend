import os
import PyPDF2
from fastapi import UploadFile, File, APIRouter, Form, Depends
from app.models.user_model import User
from app.auth.oauth2 import get_current_user
from app.services.ai_services import analyze_resume

router = APIRouter()

# UPLOADING RESUME 
@router.post("/upload-resume")
async def upload_resume(
    resume: UploadFile = File(...) # Receives uploaded PDF
):
    upload_folder = "uploads"
    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(
        upload_folder,
        resume.filename
    )

# Store pdf in the /uploads
    with open(file_path, "wb") as file: # wb = write binary
        content = await resume.read()
        file.write(content)

    extracted_text = ""

    with open(file_path, "rb") as pdf_file: #rb = read binary
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in pdf_reader.pages:
            extracted_text += page.extract_text()

    return {
        "filename": resume.filename,
        "extracted_text": extracted_text
    }

# Upload Resume + Analyze 
@router.post("/upload-and-analyze")
async def upload_and_analyze(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    current_user: User = Depends(get_current_user)
):
    upload_folder = "uploads"
    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(
        upload_folder,
        resume.filename
    )

    with open(file_path, "wb") as file:
        content = await resume.read()
        file.write(content)
    
    extracted_text = ""

    with open(file_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in pdf_reader.pages:
            extracted_text += page.extract_text()
    
    analysis = analyze_resume(extracted_text, job_description)

    return{
        "filename": resume.filename,
        "User": current_user.email,
        "analysis": analysis,
        "extracted_text": extracted_text
    }