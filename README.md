
Legal RAG

基于 RAG 架构的本地文档问答系统。

技术栈

- 后端：FastAPI
- 向量模型：BGE (bge-large-zh-v1.5)
- 向量库：ChromaDB
- AI 接口：DeepSeek
- PDF 提取：PyMuPDF
- 内网穿透：natapp / cpolar

## 项目结构
- project/
  - main.py            # 入口文件
  - config.ini         # 配置文件（API Key）
  - FrontEnd/          # 前端页面
  - RearEnd/           # 后端接口
  - models/            # BGE 模型文件
  - db/                # ChromaDB 向量库
  - pdf/               # PDF 文件

## 使用方式

1.启动服务
```javascript
uvicorn main:app --port 8001
```
2.在浏览器直接访问命令行给出的网址即可使用

## 配置

在 `config.ini` 中填入 DeepSeek API Key：

```ini
[deepseek]
api_key = your_api_key
```
