from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma


def vector_store(chunks: list[str]):
    # 使用本地ollama嵌入模型
    embedding = OllamaEmbeddings(model="qwen3-embedding:4b")

    # 在./chroma中查找名为document_chunks的集合，如果不存在则创建
    # 如果存在，不清空旧数据，默认追加
    v_store = Chroma(
        collection_name="document_chunks",
        embedding_function=embedding,
        persist_directory="../chroma" # 持久化目录
    )

    ids = v_store.add_texts(chunks)
    return ids
    

