from unittest.mock import Mock

from fastapi.testclient import TestClient

import api


client = TestClient(api.app)


def test_root():

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert "message" in data


def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    assert (
        response.json()["status"]
        == "healthy"
    )


def test_chat(monkeypatch):

    mock_pipeline = Mock()

    mock_pipeline.run.return_value = {
        "answer": (
            "Artificial intelligence is a branch "
            "of computer science."
        ),
        "sources": [],
        "model": "gemini-test",
        "grounded": False,
        "metrics": {},
    }

    monkeypatch.setattr(
        api,
        "get_pipeline",
        lambda: mock_pipeline,
    )

    response = client.post(
        "/chat",
        json={
            "query": (
                "What is artificial intelligence?"
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data

    assert "request_id" in data