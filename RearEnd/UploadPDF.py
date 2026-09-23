from pathlib import Path

from fastapi import UploadFile, File, APIRouter
import shutil

router = APIRouter()

@router.post("/UploadPDF")
async def upload_pdf(file: UploadFile = File(...)):
    BASE_DIR = Path(__file__).parent.parent
    pdf_dir = BASE_DIR / "pdf"
    pdf_dir.mkdir(exist_ok=True)

    dest = pdf_dir / file.filename
    with dest.open("wb") as f:
        shutil.copyfileobj(file.file, f)

    return {"filename": file.filename}
