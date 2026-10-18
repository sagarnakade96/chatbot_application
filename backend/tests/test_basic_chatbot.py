from fastapi.testclient import TestClient

from app.main import app


def test_basic_chatbot_placeholder():
    r = TestClient(app).get("/api/v1/basic-chatbot")
    assert r.status_code == 200
    assert r.json()["app"] == "basic_chatbot"
