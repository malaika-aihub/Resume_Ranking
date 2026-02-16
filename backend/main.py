from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Header
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from resume_parser import parse_resumes
from ranking_engine import rank_candidates_bert
from dotenv import load_dotenv
from pdf_generator import generate_pdf
import os
import json

# load.env
load_dotenv()

# API key from .env
API_KEY = os.getenv("API_KEY")

app = FastAPI()

# CORS allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Verify API Key
def verify_api_key(api_key: str):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.post("/analyze")
async def analyze(
    api_key: str = Header(...),
    resumes: list[UploadFile] = File(...),
    job_description: str = Form(...)
):
    verify_api_key(api_key)

    # Save uploaded resumes
    upload_folder = "uploads"
    os.makedirs(upload_folder, exist_ok=True)
    saved_files = []
    for file in resumes:
        file_path = os.path.join(upload_folder, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        saved_files.append(file_path)

    # Parse resumes
    resume_texts = parse_resumes(saved_files)

    # Rank using BERT
    top_10 = rank_candidates_bert(resume_texts, job_description)

    # Save top 10 to json for PDF generation
    with open("top_10.json", "w") as f:
        json.dump(top_10, f, indent=2)

    return {"top_10": top_10}

@app.get("/download_pdf")
def download_pdf(api_key: str = Header(...)):
    verify_api_key(api_key)
    pdf_path = generate_pdf()
    if not pdf_path or not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF not found")
    return FileResponse(pdf_path, media_type='application/pdf', filename="Top10_Resume_Report.pdf")
