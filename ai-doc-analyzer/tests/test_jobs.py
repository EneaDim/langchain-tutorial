import io

def test_jobs_list(client):
    # ensure at least one job exists
    pdf_bytes = b"%PDF-1.4\n1 0 obj\n<<>>\nendobj\ntrailer\n%%EOF"
    files = {"file": ("t.pdf", io.BytesIO(pdf_bytes), "application/pdf")}
    client.post("/api/v1/analyze", files=files)

    r = client.get("/api/v1/jobs?limit=5")
    assert r.status_code == 200
    arr = r.json()
    assert isinstance(arr, list)
