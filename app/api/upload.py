import os
from fastapi import UploadFile, File, HTTPException

# todo: 避免重复上传

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
    
    # # 保存文件
    # save_path = os.path.join(SAVE_DIR, file.filename)
    # with open(save_path, "wb") as f:
    #     f.write(content)
    
    return {
        "filename": file.filename,
        # "size": len(content),
        # "path": save_path,
        "message": "文件上传成功",
        "content": content,
        "filetype": ext
    }