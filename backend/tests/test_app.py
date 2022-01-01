from fastapi.testclient import TestClient

from app.main import app
from app.core.config import get_settings

client = TestClient(app)


def test_read_item():
    response = client.get("/models")
    assert response.status_code == 200
    assert response.json() == {'model': get_settings().MODELS}
