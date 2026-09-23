from pathlib import Path

from fastapi import APIRouter

router = APIRouter()

@router.delete("/deletePDF")
def delete_pdfs():
    BASE_DIR = Path(__file__).parent.parent
    pdf_dir = BASE_DIR / "pdf"
    for f in pdf_dir.glob("*.pdf"):
        f.unlink()
    txt_path = BASE_DIR / "RearEnd" / "pdf.txt"
    open(txt_path, "w", encoding="utf-8").close()
    return {"message": "删除成功"}

