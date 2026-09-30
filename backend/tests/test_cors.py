from fastapi.testclient import TestClient


def test_configured_origin_is_allowed() -> None:
    from pathwise.main import create_app

    with TestClient(create_app()) as client:
        response = client.get("/health", headers={"Origin": "http://test.local"})

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://test.local"


def test_unconfigured_origin_is_not_allowed() -> None:
    from pathwise.main import create_app

    with TestClient(create_app()) as client:
        response = client.get(
            "/health",
            headers={"Origin": "http://unauthorized.test"},
        )

    assert response.status_code == 200
    assert "access-control-allow-origin" not in response.headers
