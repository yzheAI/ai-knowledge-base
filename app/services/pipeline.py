from app.services.loader import load_document
from app.services.splitter import split_text


def process_document(file_path: str):
    text = load_document(file_path)

    chunks = split_text(text)

    return {
        "total_length": len(text),
        "chunk_count": len(chunks),
        "chunks": chunks[:3]
    }