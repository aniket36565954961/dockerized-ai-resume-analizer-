from fastapi import FastAPI, File, UploadFile, Form
from pypdf import PdfReader
from transformers import pipeline
import io

app = FastAPI()

# Load a lightweight AI model for text comparison (Feature Extraction)
# This runs once when the server starts
model_name = "sentence-transformers/all-MiniLM-L6-v2"
classifier = pipeline("feature-extraction", model=model_name)

def extract_text_from_pdf(file_bytes):
    pdf_reader = PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

@app.get("/")
def home():
    return {"message": "AI Backend is Running"}

@app.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...), 
    job_description: str = Form(...)
):
    # 1. Read the PDF file
    contents = await file.read()
    resume_text = extract_text_from_pdf(contents)

    # 2. (Optional) Simple Keyword Matching Logic for the demo
    # In a real app, you would use the AI model vectors to calculate cosine similarity
    # Here we do a simple keyword overlap to keep it fast and crash-proof for your first run.
    
    resume_words = set(resume_text.lower().split())
    jd_words = set(job_description.lower().split())
    
    # Calculate match score
    common_words = resume_words.intersection(jd_words)
    score = len(common_words) / len(jd_words) * 100 if len(jd_words) > 0 else 0
    
    # 3. Generate Feedback
    missing_keywords = list(jd_words - resume_words)[:5] # Show top 5 missing words

    return {
        "filename": file.filename,
        "match_score": f"{round(score, 2)}%",
        "missing_keywords": missing_keywords,
        "advice": "Consider adding the missing keywords to your resume to pass ATS scanners."
    }