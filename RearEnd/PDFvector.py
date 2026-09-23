from fastapi import FastAPI, APIRouter
from pathlib import Path
from pydantic import BaseModel
import pymupdf
import json
import chromadb
from FlagEmbedding import FlagModel
from RearEnd.dependencies import bge_model, get_col


router = APIRouter()

chroma_client = chromadb.PersistentClient(path="./db")

class ProcessRequest(BaseModel):
    filenames: list[str]

@router.post("/PDFvector")
def process_pdfs(req: ProcessRequest):
    all_text = ""
    col = get_col()

    for filename in req.filenames:
        filepath = Path("./pdf") / filename
        doc = pymupdf.open(filepath)
        for page_num, page in enumerate(doc):
            page_height = page.rect.height
            text = page.get_text("dict")
            for block in text.get("blocks", []):
                if block.get("type") == 1 and page_num > 1:
                    continue
                block_y = block.get("bbox", [0, 0, 0, 0])[1]
                if block_y < page_height * 0.05 or block_y > page_height * 0.95:
                    continue
                block_text = ""
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        text_content = span.get("text", "")
                        if text_content.strip():
                            block_text += text_content
                block_text = " ".join(block_text.split())
                if len(block_text.strip()) > 4:
                    all_text += block_text + "\n"
        doc.close()

    chunk_size = 512
    overlap = 100
    chunks = []
    chunk_index = 0
    start = 0
    text = " ".join(all_text.split())

    while start < len(text):
        chunk_text = text[start:start + chunk_size].strip()
        if chunk_text:
            chunks.append({
                "id": str(chunk_index),
                "text": chunk_text,
                "chunk_index": chunk_index
            })
            chunk_index += 1
        start += chunk_size - overlap

    texts = [c["text"] for c in chunks]
    ids = [c["id"] for c in chunks]
    embeddings = bge_model.encode(texts, batch_size=32).tolist()

    col.add(ids=ids, embeddings=embeddings, documents=texts)
    with open("RearEnd/pdf.txt", "a", encoding="utf-8") as f:
        for filename in req.filenames:
            f.write(filename + "\n")

    return {"message": f"处理完成，共存入 {len(chunks)} 条数据"}

