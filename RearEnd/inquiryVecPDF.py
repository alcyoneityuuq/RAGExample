# RearEnd/inquiryVecPDF.py
from fastapi import APIRouter
from pathlib import Path

router = APIRouter()

BASE_DIR = Path(__file__).parent.parent

@router.get("/inquiryVecPDF")
def get_vec_pdfs():
    txt_path = BASE_DIR / "RearEnd" / "pdf.txt"
    if not txt_path.exists():
        return {"pdfs": []}
    with open(txt_path, "r", encoding="utf-8") as f:
        pdfs = [line.strip() for line in f.readlines() if line.strip()]
    return {"pdfs": pdfs}
