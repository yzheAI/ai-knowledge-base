from app.services.loader import load_document
from app.services.splitter import split_text
from app.services.embedding import get_embeddings
from app.services.vevtor_store import VectorStore
vector_store = VectorStore(384)


def process_document(file_path: str):
    text = load_document(file_path)

    chunks = split_text(text)

    vectors = get_embeddings(chunks)

    vector_store.add(vectors, chunks)

    return {
        "total_length": len(text),
        "chunk_count": len(chunks),
        "embedding_dim": len(vectors[0]),
        "chunks": chunks[:3],
        "vectors": vectors[0][:3]
    }