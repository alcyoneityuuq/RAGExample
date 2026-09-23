from fastapi import FastAPI, APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import chromadb
from openai import OpenAI
import configparser
from RearEnd.dependencies import bge_model, get_col

router = APIRouter()

config = configparser.ConfigParser()
config.read("config.ini", encoding="utf-8")
api_key = config["deepseek"]["api_key"]

chroma_client = chromadb.PersistentClient(path="./db")

deepseek = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]
    question: str

@router.post("/ai")
async def chat(req: ChatRequest):
    col = get_col()
    # 用当前问题检索向量库
    query_embedding = bge_model.encode_queries([req.question]).tolist()
    results = col.query(query_embeddings=query_embedding, n_results=5)
    chunks = "\n".join(results["documents"][0])

    system_prompt = f"""你是一个问答助手，请根据以下参考内容回答用户的问题。
如果参考内容中没有相关信息，请说明无法回答。

参考内容：
{chunks}"""

    # 取最近五轮上下文
    history = req.messages[-10:]

    messages = [{"role": "system", "content": system_prompt}]
    for msg in history:
        messages.append({"role": msg.role, "content": msg.content})
    messages.append({"role": "user", "content": req.question})

    def stream():
        response = deepseek.chat.completions.create(
            model="deepseek-flash",
            messages=messages,
            stream=True
        )
        for chunk in response:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta

    return StreamingResponse(stream(), media_type="text/plain")
