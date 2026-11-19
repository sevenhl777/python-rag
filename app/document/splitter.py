def splitter(content: str, chunk_size: int = 500, overlap: int = 80) -> list[str]:
    chunks = []
    start = 0
    n = len(content)
    while start < n:
        end = start + chunk_size
        chunk = content[start:end]

        # 从chunk右侧开始找换行或逗号句号，找到最大的一个下标值
        cut_pos = max(
            chunk.rfind("\n\n"),
            chunk.rfind("\n"),
            chunk.rfind("。"),
            chunk.rfind("，"),
        )

        # 如果cut_pos在chunk_size的一半以上，则切分到cut_pos为止
        if cut_pos > int(chunk_size * 0.5):
            end = start + cut_pos
            chunk = content[start:end]

        chunks.append(chunk)
        start = end - overlap # 下一次开始位置要减去重叠部分
    
    return chunks
        