import os
import PyPDF2

from fastapi import UploadFile, File, APIRouter

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

    extracted_file = ""

    with open(file_path, "rb") as pdf_file: #rb = read binary

        pdf_reader = PyPDF2.PdfReader(pdf_file) # Read PDF pages

        extracted_text = ""

        for page in pdf_reader.pages:
            extracted_text += page.extract_text() # extracted resume content

    
    return {
        "filename": resume.filename,
        "extracted_text": extracted_text
    }