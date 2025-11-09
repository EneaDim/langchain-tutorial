def test_healthz(client):
    r = client.get("/api/v1/healthz")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"
