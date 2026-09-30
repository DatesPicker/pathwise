from fastapi.testclient import TestClient


def test_health_endpoint() -> None:
    from pathwise.main import create_app

    with TestClient(create_app()) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
