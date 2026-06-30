def split_text(text: str, chunk_size: int = 200):
    sentences = text.split("。")
    chunks = []

    current = ""
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        if len(current)+len(sentence) <= chunk_size:
            current += sentence + "。"
        else:
            chunks.append(current)
            current = sentence + "。"
    if current:
        chunks.append(current)

    return chunks
