import os, requests, streamlit as st

API_BASE = os.environ.get("STREAMLIT_API_BASE", "http://localhost:8000")
AUTH = {"Authorization": f"Bearer {os.environ.get('JWT_DEV_BEARER','devtoken-please-dont-use-in-prod')}"}

st.title("🧠 Run Summary")

sources = st.text_area("Source keys (one per line, e.g., s3://srw-artifacts/...)", height=160)
templates = requests.get(f"{API_BASE}/templates", headers=AUTH).json()
template = st.selectbox("Template", [t["id"] for t in templates])

if st.button("Create Job"):
    resp = requests.post(f"{API_BASE}/jobs", headers=AUTH, json={
        "sources": [s for s in sources.splitlines() if s.strip()],
        "template": template if template != "none" else None
    }).json()
    st.success(f"Job created: {resp['job_id']}")
    st.session_state["last_job_id"] = resp["job_id"]
