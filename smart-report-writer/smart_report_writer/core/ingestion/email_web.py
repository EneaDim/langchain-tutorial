import email
from typing import Dict, Any

def parse_eml(data: bytes) -> Dict[str, Any]:
    msg = email.message_from_bytes(data)
    content = ""
    for part in msg.walk():
        if part.get_content_type() == "text/plain":
            content += part.get_payload(decode=True).decode(errors="ignore") + "\n"
    return {"subject": msg.get("Subject",""), "from": msg.get("From",""), "to": msg.get("To",""), "text": content}
