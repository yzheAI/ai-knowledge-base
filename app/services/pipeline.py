from app.services.loader import load_document
from app.services.splitter import split_text, clean_chunks
from app.services.embedding import get_embeddings


def process_document(file_path: str):
    text = load_document(file_path)
    if not text or len(text.strip()) == 0:
        raise ValueError("空文件")
    chunks = split_text(text)

    chunk_cleaned = clean_chunks(chunks)
    if len(chunk_cleaned) == 0:
        raise ValueError("No valid chunks after cleaning")

    vectors = get_embeddings(chunk_cleaned)

    return {
        "total_length": len(text),
        "chunk_count": len(chunk_cleaned),
        "embedding_dim": len(vectors[0]),
        "chunks": chunk_cleaned,
        "vectors": vectors
    }