from fastapi import FastAPI, UploadFile, File, HTTPException
import os
from api.upload import upload_file
from document.splitter import splitter
from document.parser import parser
from embedding.vector_store import vector_store


app = FastAPI()

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    # 文件上传
    res = await upload_file(file)
    print("文件上传成功")

    # bytes转字符串
    parse_str = parser(res["content"], res["filetype"])
    print("文件解析成功")

    # 切分文档
    chunks = splitter(parse_str)
    print(f"分档切片成功，共切分：{len(chunks)}个")

    # 存储到向量库
    # ids = vector_store(chunks)
    # print(f"存储成功，共存储{len(ids)}个chunks")
    
    return {
        "filename": res["filename"],
        "message": "文件上传成功",
    }
