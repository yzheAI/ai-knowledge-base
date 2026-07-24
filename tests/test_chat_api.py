from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_chat_api():
    response = client.post(
        "/chat/chat/stream",
        json={
            "query": "铜基复合材料是什么？",
            "kb_name": "copper_based"
        }
    )

    assert response.status_code == 200
    text = response.text

    assert len(text) > 0
