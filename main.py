from fastapi import FastAPI
from RearEnd import ai, PDFvector, InquiryPDF, UploadPDF, deletePDF
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from RearEnd import inquiryVecPDF
from RearEnd import clearVec

app = FastAPI()

app.include_router(ai.router)
app.include_router(PDFvector.router)
app.include_router(InquiryPDF.router)
app.include_router(UploadPDF.router)
app.include_router(deletePDF.router)
app.include_router(inquiryVecPDF.router)
app.include_router(clearVec.router)
app.mount("/static", StaticFiles(directory="FrontEnd"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def index():
    return FileResponse("FrontEnd/web.html")

if __name__ == "__main__":
    from huggingface_hub import snapshot_download

    snapshot_download(
        repo_id="BAAI/bge-large-zh-v1.5",
        local_dir="./models/bge-large-zh-v1.5"
    )
    print("模型下载完成")


