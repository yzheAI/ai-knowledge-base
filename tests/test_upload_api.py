from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_upload_api():
    file = {
        "file": (
            "test.txt",
            "铜基复合材料是一种复合材料",
            "text/plain"
        )
    }
    data = {
        "kb_name": "test_kb"
    }

    response = client.post(
        "/files/",
        files=file,
        data=data,
    )

    assert response.status_code == 200
    result = response.json()
    assert result["code"] == 200
