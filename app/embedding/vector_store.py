from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma


def vector_store(chunks: list[str]):
    # 同一个文件所有chunk的file_hash都相同
    file_hash = chunks[0].metadata["file_hash"]
    

    # 使用本地ollama嵌入模型
    embedding = OllamaEmbeddings(model="qwen3-embedding:4b")

    # 在./chroma中查找名为document_chunks的集合，如果不存在则创建
    # 如果存在，不清空旧数据，默认追加
    v_store = Chroma(
        collection_name="document_chunks",
        embedding_function=embedding,
        persist_directory="../chroma" # 持久化目录
    )

    ### 入库阶段查重，防并发 ###
    # 查重，精确匹配，找出所有chunk的metadata里面，file_hash等于当前file_hash的记录
    # get默认返回ids, embeddings, documents, metadatas，指定metadatas减少开销
    # 返回 { ids: [xxx, xxx, ...], metadatas: [{...}, {...}, ...], documents: None, embeddings: None }
    exist = v_store.get(where={"file_hash": file_hash}, include=["metadatas"])
    if exist["ids"]:
        return {"success": False, "msg": "文件已存在，跳过入库"}

    ids = v_store.add_documents(chunks)
    return {"success": True, "msg": f"入库成功，切片数量：{len(ids)}", "ids": ids}
    

