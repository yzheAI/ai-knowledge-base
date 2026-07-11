def clean_chunks(chunks: list[str]):
    cleaned = []
    for c in chunks:
        c = c.strip()

        if not c:
            continue

        if len(c) < 10:
            continue

        if len(c.replace("。", "").strip()) == 0:
            continue

        cleaned.append(c)
    return cleaned


def split_text(text: str, chunk_size: int = 500, overlap: int = 50):
    sentences = text.split("。")
    chunks = []

    current = ""
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        sentence += "。"

        if len(current)+len(sentence) <= chunk_size:
            current += sentence + "。"
        else:
            if current:
                chunks.append(current)
                # overlap
                overlap_text = current[-overlap:]

                current = overlap_text + sentence
                
    if current:
        chunks.append(current)

    return chunks
