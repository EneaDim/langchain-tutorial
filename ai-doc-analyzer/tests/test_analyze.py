import io

def test_analyze_pdf(client):
    pdf_bytes = b"%PDF-1.4\n1 0 obj\n<<>>\nendobj\ntrailer\n%%EOF"
    files = {"file": ("t.pdf", io.BytesIO(pdf_bytes), "application/pdf")}
    r = client.post("/api/v1/analyze", files=files)
    assert r.status_code == 200
    data = r.json()
    assert "summary" in data and "keywords" in data
