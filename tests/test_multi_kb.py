from app.core.container import vector_manager
from app.embedding.embedding import get_embedding


def test_multi_kb_isolation():
    copper_store = vector_manager.get_store(
        "copper_based"
    )
    medical_store = vector_manager.get_store(
        "medical"
    )

    assert copper_store is not medical_store


def test_multi_kb_data_isolation():
    copper_store = vector_manager.get_store(
        "copper_based"
    )
    medical_store = vector_manager.get_store(
        "medical"
    )

    query = "铜基复合材料是什么？"

    embedding = get_embedding(query)

    copper_result = copper_store.search(
        embedding,
        top_k=5
    )
    medical_result = medical_store.search(
        embedding,
        top_k=5
    )

    copper_texts = [
        r["text"]
        for r in copper_result
    ]

    medical_texts = [
        r["text"]
        for r in medical_result
    ]

    assert any(
        "铜" in text
        for text in copper_texts
    )

    assert not any(
        "铜" in text
        for text in medical_texts
    )
