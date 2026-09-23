# RearEnd/clearVec.py
from fastapi import APIRouter
from pathlib import Path
from RearEnd.dependencies import chroma_client

router = APIRouter()

BASE_DIR = Path(__file__).parent.parent

@router.delete("/clearVec")
def clear_vec():
    for collection in chroma_client.list_collections():
        chroma_client.delete_collection(collection.name)
    txt_path = BASE_DIR / "RearEnd" / "pdf.txt"
    open(txt_path, "w", encoding="utf-8").close()
    return {"message": "向量库已清空"}
