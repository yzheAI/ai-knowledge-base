from app.core.container import container


def test_faiss_retriever():
    results = container.faiss_retriever.retrieve(
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
    results = container.bm25_retriever.retrieve(
        query="铜基复合材料是什么？",
        kb_name="copper_based",
        top_k=5
    )

    assert len(results) > 0

    item = results[0]
    assert "text" in item
    assert "distance" in item
    assert "chunk_id" in item


def test_hybrid_retriever():
    results = container.hybrid_retriever.retrieve(
        query="铜基复合材料是什么？",
        kb_name="copper_based",
        top_k=5
    )

    assert len(results) > 0

    item = results[0]

    assert "text" in item
    assert "metadata" in item
