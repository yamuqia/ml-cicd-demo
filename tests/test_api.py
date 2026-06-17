from fastapi.testclient import TestClient
import pytest
from app.main import app

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "ok"
    assert data["model_loaded"] is True


def test_predict(client):
    response = client.post(
        "/predict",
        json={"features": [5.1, 3.5, 1.4, 0.2]},
    )

    assert response.status_code == 200

    data = response.json()
    assert "label" in data
    assert "class_name" in data
    assert "probability" in data


def test_predict_wrong_feature_length(client):
    response = client.post(
        "/predict",
        json={"features": [5.1, 3.5]},
    )

    assert response.status_code == 400