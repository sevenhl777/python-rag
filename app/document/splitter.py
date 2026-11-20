# def splitter(content: str, chunk_size: int = 500, overlap: int = 80) -> list[str]:
#     chunks = []
#     start = 0
#     n = len(content)
#     while start < n:
#         end = start + chunk_size
#         chunk = content[start:end]

#         # 从chunk右侧开始找换行或逗号句号，找到最大的一个下标值
#         cut_pos = max(
#             chunk.rfind("\n\n"),
#             chunk.rfind("\n"),
#             chunk.rfind("。"),
#             chunk.rfind("，"),
#         )

#         # 如果cut_pos在chunk_size的一半以上，则切分到cut_pos为止
#         if cut_pos > int(chunk_size * 0.5):
#             end = start + cut_pos
#             chunk = content[start:end]

#         chunks.append(chunk)
#         start = end - overlap # 下一次开始位置要减去重叠部分
    
#     return chunks

from langchain_core.documents import Document

def splitter(pages: list[Document], chunk_size: int = 500, overlap: int = 80, min_chunk_size: int = 120) -> list[str]:
    chunks = []

    for page in pages:
        text = page.page_content
        metadata = page.metadata
        text_len = len(text)
        start = 0
        while start < text_len:
            end = start + chunk_size
            chunk_text = text[start:end]
            cut_index = max(
                chunk_text.rfind("\n\n"),
                chunk_text.rfind("\n"),
                chunk_text.rfind("。"),
                chunk_text.rfind("，"),
            )
            if cut_index > start + int(chunk_size * 0.5):
                end = start + cut_index
                chunk_text = text[start:end]
            
            # 如果是当前页的最后一个chunk，且chunk_text长度小于min_chunk_size，且chunks中已有切片数据
            if end >= text_len and len(chunk_text) < min_chunk_size and len(chunks) > 0:
                prev_chunk = chunks[-1] # 上一个切片
                # 将上一个切片的文本和当前文本合并
                merge_text =  prev_chunk.page_content + "\n" + chunk_text
                chunks[-1] = Document(
                    page_content = merge_text,
                    metadata = prev_chunk.metadata
                )
            else: # 否则创建新切片
                chunks.append(Document(
                    page_content = chunk_text,
                    metadata = metadata.copy()
                ))
            
            start = end - overlap

    return chunks

    
        