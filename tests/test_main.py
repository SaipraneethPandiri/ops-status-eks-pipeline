from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_version_has_value():
    r = client.get("/version")
    assert r.status_code == 200
    assert "version" in r.json()


def test_status_shape():
    r = client.get("/status")
    body = r.json()
    assert r.status_code == 200
    assert {"hostname", "uptime_seconds", "disk"} <= body.keys()
    assert 0 <= body["disk"]["used_percent"] <= 100
