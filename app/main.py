from fastapi import FastAPI, UploadFile, File, HTTPException
import os
from api.upload import upload_file
from document.splitter import splitter
from document.parser import parser
from embedding.vector_store import vector_store
from dotenv import load_dotenv
from api.llm import chat_agent
from langchain_openai import ChatOpenAI

app = FastAPI()

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL")

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    # 文件上传
    res = await upload_file(file)
    print("文件上传成功")
    if not res["success"]:
        return res
    # bytes转字符串
    documents = parser(res["content"], res["filename"])
    print("文件解析成功")

    # 切分文档
    chunks = splitter(documents)
    print(f"分档切片成功，共切分：{len(chunks)}个")

    # 存储到向量库
    return vector_store(chunks)

@app.post("/chat")
async def chat(prompt: str):

    llm = ChatOpenAI(
        model = "deepseek-chat",
        openai_api_key = DEEPSEEK_API_KEY,
        openai_api_base = DEEPSEEK_BASE_URL,
        temperature = 0.1
    )
    res = await chat_agent(llm, prompt)
    print(res)

    return { "success": True, "msg": res }
    