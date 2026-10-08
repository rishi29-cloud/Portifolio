from fastapi.testclient import TestClient

from reels_analyst.api.main import app


def test_health_check() -> None:
    response = TestClient(app).get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_invalid_dimension_is_a_client_error() -> None:
    response = TestClient(app).get("/v1/performance/not-a-dimension")
    assert response.status_code == 400
