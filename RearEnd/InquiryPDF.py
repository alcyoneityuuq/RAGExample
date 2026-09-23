from fastapi import FastAPI, APIRouter
from pathlib import Path

router = APIRouter()

@router.get("/InquiryPDF")
def get_pdfs():
    BASE_DIR = Path(__file__).parent.parent
    pdf_dir = BASE_DIR / "pdf"
    pdfs = [f.name for f in pdf_dir.glob("*.pdf")]
    return {"pdfs": pdfs}
