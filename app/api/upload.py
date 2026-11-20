import os
from fastapi import UploadFile, File, HTTPException
from document.parser import get_file_hash
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

# # 文件保存路径
# SAVE_DIR = "./uploads"
# os.makedirs(SAVE_DIR, exist_ok=True)

# 允许后缀
ALLOW_SUFFIX = ["pdf", "txt", "md", ".docx"]
MAX_SIZE = 1024 * 1024 * 20

async def upload_file(file: UploadFile = File(...)):
    print(file.filename)
    ext = file.filename.split(".")[-1].lower()
    if ext not in ALLOW_SUFFIX: # 判断文件后缀是否合法
        raise HTTPException(status_code=400, detail="不支持该文件类型")
    
    content = await file.read()
    if len(content) > MAX_SIZE: # 判断文件大小是否超出限制
        raise HTTPException(status_code=400, detail="文件大小超出限制")

    ### 上传阶段查重 ###
    file_hash = get_file_hash(content)
    # 使用本地ollama嵌入模型
    embedding = OllamaEmbeddings(model="qwen3-embedding:4b")
    # 在./chroma中查找名为document_chunks的集合，如果不存在则创建
    # 如果存在，不清空旧数据，默认追加
    v_store = Chroma(
        collection_name="document_chunks",
        embedding_function=embedding,
        persist_directory="../chroma" # 持久化目录
    )
    exist = v_store.get(where={"file_hash": file_hash}, include=["metadatas"])
    if exist["ids"]:
        return {"success": False, "msg": "文件已存在"}
    
    # # 保存文件
    # save_path = os.path.join(SAVE_DIR, file.filename)
    # with open(save_path, "wb") as f:
    #     f.write(content)
    
    return {
        "success": True,
        "filename": file.filename,
        # "size": len(content),
        # "path": save_path,
        "content": content,
        "filetype": ext
    }