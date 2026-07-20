from app.core.container import faiss_retriever, bm25_retriever, hybrid_retriever


def test_faiss_retriever():
    results = faiss_retriever.retrieve(
        query="铜基复合材料是什么？",
        kb_name="copper_based",
        top_k=5
    )

    assert len(results) > 0

    item = results[0]
    assert "text" in item
    assert "metadata" in item
    assert "score" in item


def test_bm25_retriever():
    results = bm25_retriever.retrieve(
        query="铜基复合材料是什么？",
        kb_name="copper_based",
        top_k=5
    )

    assert len(results) > 0

    item = results[0]
    assert "text" in item
    assert "score" in item
    assert "chunk_id" in item


def test_hybrid_retriever():
    results = hybrid_retriever.retrieve(
        query="铜基复合材料是什么？",
        kb_name="copper_based",
        top_k=5
    )

    assert len(results) > 0

    item = results[0]

    assert "text" in item
    assert "metadata" in item
