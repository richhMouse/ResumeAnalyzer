from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from app.services.ats_engine import ATSEngine
import io
from PyPDF2 import PdfReader
from docx import Document
from PIL import Image
import pytesseract

router = APIRouter()

ALLOWED_ROLES = [
    # Management Roles
    "Product Manager",
    "Project Manager",
    "Business Analyst",
    "Operations Manager",
    "HR Manager",
    # Tech Roles
    "Software Engineer",
    "Full Stack Developer",
    "Data Scientist",
    "Data Analyst",
    "DevOps Engineer",
    "Cloud Engineer"
]

class ResumeRequest(BaseModel):
    resume_text: str = Field(..., min_length=1, description="Plain extracted resume text only")
    target_role: str = Field(..., description="Target management role from allowed list")

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from PDF file."""
    try:
        pdf_reader = PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse PDF: {str(e)}")

def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract text from Word document."""
    try:
        doc = Document(io.BytesIO(file_bytes))
        text = "\n".join([para.text for para in doc.paragraphs])
        return text.strip()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse Word document: {str(e)}")

def extract_text_from_image(file_bytes: bytes) -> str:
    """Extract text from image using OCR."""
    try:
        image = Image.open(io.BytesIO(file_bytes))
        # Convert to RGB if necessary
        if image.mode not in ('RGB', 'L'):
            image = image.convert('RGB')
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to extract text from image: {str(e)}")

class ATSResponse(BaseModel):
    ats_score: int = Field(..., description="Overall ATS score out of 100")
    shortlist_probability: str = Field(..., description="High, Medium, or Low")
    role_relevance_score: int
    leadership_score: int
    impact_metrics_score: int
    resume_structure_score: int
    language_quality_score: int
    factual_strengths: list[str]
    factual_weaknesses: list[str]
    improvement_suggestions: list[str]

@router.post("/analyze", response_model=ATSResponse)
async def analyze_resume(request: ResumeRequest):
    """Analyze a resume for management roles using ATS evaluation."""
    
    if not request.resume_text or not request.resume_text.strip():
        raise HTTPException(status_code=400, detail="MISSING: Resume text is required")
    
    if not request.target_role:
        raise HTTPException(status_code=400, detail="MISSING: Target role is required")
    
    if request.target_role not in ALLOWED_ROLES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid role. Allowed roles: {', '.join(ALLOWED_ROLES)}"
        )
    
    engine = ATSEngine()
    result = engine.evaluate(request.resume_text, request.target_role)
    
    return ATSResponse(**result)

@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    target_role: str = "Product Manager"
):
    """Upload and parse a resume file (PDF or Word), then analyze it."""
    
    if target_role not in ALLOWED_ROLES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid role. Allowed roles: {', '.join(ALLOWED_ROLES)}"
        )
    
    # Validate file type
    file_extension = file.filename.split('.')[-1].lower() if file.filename else ''
    
    allowed_extensions = ['pdf', 'docx', 'png', 'jpg', 'jpeg', 'webp']
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload a PDF, DOCX, PNG, JPG, or WebP file."
        )
    
    # Read file content
    file_bytes = await file.read()
    
    # Extract text based on file type
    if file_extension == 'pdf':
        resume_text = extract_text_from_pdf(file_bytes)
    elif file_extension == 'docx':
        resume_text = extract_text_from_docx(file_bytes)
    elif file_extension in ['png', 'jpg', 'jpeg', 'webp']:
        resume_text = extract_text_from_image(file_bytes)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    
    if not resume_text or not resume_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Could not extract text from the file. The file may be empty or corrupted."
        )
    
    # Analyze the extracted text
    engine = ATSEngine()
    result = engine.evaluate(resume_text, target_role)
    
    return ATSResponse(**result)
