import os, time, socket, requests
from typing import Dict, Any, Optional

# Prefer container DNS (api), fallback to localhost for host browsing/dev
DEFAULTS = ["http://api:8080", "http://localhost:8080"]
API_BASE = os.environ.get("SRW_API_BASE") or ""

def _pick_base() -> str:
    cand = [API_BASE] if API_BASE else []
    for base in cand + DEFAULTS:
        try:
            host = base.split("//",1)[1].split("/",1)[0].split(":")[0]
            socket.gethostbyname(host)  # DNS check
            return base
        except Exception:
            continue
    # last resort
    return DEFAULTS[-1]

BASE = _pick_base()

def _req(method: str, path: str, **kw) -> requests.Response:
    timeout = kw.pop("timeout", 15)
    backoff = 0.5
    last_ex = None
    for _ in range(5):
        try:
            return requests.request(method, f"{BASE}{path}", timeout=timeout, **kw)
        except requests.RequestException as e:
            last_ex = e
            time.sleep(backoff)
            backoff = min(4.0, backoff * 2)
    raise last_ex  # bubble up

def upload(file) -> Dict[str, Any]:
    files = {"file": (file.name, file.read())}
    r = _req("POST", "/v1/uploads", files=files)
    r.raise_for_status()
    return r.json().get("data", r.json())

def list_templates() -> Dict[str, Any]:
    r = _req("GET", "/v1/templates")
    r.raise_for_status()
    return r.json().get("data", r.json())

def providers() -> Dict[str, Any]:
    r = _req("GET", "/v1/llm/providers")
    r.raise_for_status()
    return r.json().get("data", r.json())

def generate(payload: Dict[str, Any]) -> Dict[str, Any]:
    r = _req("POST", "/v1/generate", json=payload)
    r.raise_for_status()
    return r.json().get("data", r.json())

def job_status(job_id: str) -> Dict[str, Any]:
    r = _req("GET", f"/v1/jobs/{job_id}")
    r.raise_for_status()
    return r.json().get("data", r.json())

def job_artifact(job_id: str) -> Optional[str]:
    r = _req("GET", f"/v1/jobs/{job_id}/artifact")
    if r.status_code == 404:
        return None
    r.raise_for_status()
    data = r.json().get("data", r.json())
    return data.get("download_url") or data.get("url")
