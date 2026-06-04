import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key = os.getenv("GROQ_API_KEY")
)

def analyze_resume(
        resume_text,
        job_description
):
    prompt = f"""
    Analyze this resume against the job description.

    Resume: {resume_text}
    Job Description : {job_description}

    Give:
    1. Match score out of 100
    2. Missing skills
    3. Resume improvement suggestions
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role":"user", "content": prompt}]
    )

    return response.choices[0].message.content

def generate_cover_letter(
        resume_text,
        job_description
):
    prompt = f"""
    Write a professional cover letter based on this resume and job description.

    Resume: {resume_text}
    Job Description: {job_description}

    The cover letter should:
    1. Be professional and concise
    2. Highlight matching skills from the resume
    3. Show enthusiasm for the role
    4. Be ready to send — no placeholders
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role":"user", "content": prompt}]
    )

    return response.choices[0].message.content

#Generting Interview Questions according to the Job_description
def generate_interview_questions(
        resume_text,
        job_description
):
    prompt = f"""
    Generate interview questions based on this resume and job description.

    Resume: {resume_text}
    Job Description: {job_description}

    Give:
    1. 5 technical questions based on the job requirements
    2. 3 behavioral questions
    3. 2 questions based on gaps between resume and job description
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role":"user", "content": prompt}]
    )

    return response.choices[0].message.content