from FlagEmbedding import FlagModel
import chromadb
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

bge_model = FlagModel(str(BASE_DIR / 'models' / 'bge-large-zh-v1.5'), use_fp16=True, normalize_embeddings=True)

chroma_client = chromadb.PersistentClient(path=str(BASE_DIR / "db"))
print(f"BASE_DIR: {BASE_DIR}")
print(f"db path: {BASE_DIR / 'db'}")

def get_col():
    return chroma_client.get_or_create_collection("documents")
    print(f"BASE_DIR: {BASE_DIR}")
    print(f"db path: {BASE_DIR / 'db'}")


