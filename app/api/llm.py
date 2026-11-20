from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain.agents import create_agent

# 上传入库的模型必须和下面转prompt的模型一致
embedding = OllamaEmbeddings(model="qwen3-embedding:4b")

# llm工具方法，查询知识库匹配结果
def query_database(prompt: str) -> str:
    """
    当用户的问题和上传文件内容相关时，使用这个工具检索知识库。
    如果是常识、问候、简单计算、闲聊类问题，不需要调用这个工具。
    """
    v_store = Chroma(
        collection_name = "document_chunks",
        embedding_function = embedding,
        persist_directory = "../chroma" # 持久化目录
    )
    # 查询数据库中与prompt向量相似度最高的3条结果
    docs = v_store.similarity_search(prompt, k=3)
    context = ""
    for doc in docs:
        context += doc.page_content + "\n\n"
    if not context:
        return "未找到相关内容"
    return f"知识库查询内容：\n{context}"

async def chat_agent(llm, prompt: str):
    
    system_prompt = """
        你是一个知识库问答助手。
        规则：
        1. 如果用户问题属于内部文档、项目资料、上传文件相关内容，优先调用 query_database 工具查询知识库，依据返回的资料回答。
        2. 如果是闲聊、问候、通用常识、简单计算，不需要调用工具，直接自己回答。
        3. 调用工具拿到资料后，只能基于资料内容回答，资料没有的信息不要编造；如果工具返回无相关内容，直接告知用户知识库查不到。
        4. 不要编造不存在的信息，不要在没有资料的时候瞎编文档内容。
    """

    agent = create_agent(
        model = llm,
        tools = [query_database],
        system_prompt = system_prompt,
    )

    res = agent.invoke({ "messages": [{ "role": "user", "content": prompt}] })
    return res["messages"][-1].content
