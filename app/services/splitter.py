def split_text(text: str, chunk_size: int = 300, overlap: int = 50):
    chunks = []
    start = 0
    length = len(text)
    while start < length:
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap  # 重叠部分
    return chunks
