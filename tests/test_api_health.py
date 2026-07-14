from fastapi.testclient import TestClient

from app.infrastructure.api.app import app


def test_root_endpoint_returns_ok_status():
    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "active"


def test_docs_endpoint_is_available():
    client = TestClient(app)
    response = client.get("/docs")

    assert response.status_code == 200
