from weasyprint import HTML

def to_html(content: str) -> bytes:
    return content.encode("utf-8")

def to_pdf(content: str) -> bytes:
    pdf = HTML(string=content).write_pdf()
    return pdf
