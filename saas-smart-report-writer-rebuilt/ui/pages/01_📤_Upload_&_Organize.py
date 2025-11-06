import os, requests, streamlit as st

API_BASE = os.environ.get("STREAMLIT_API_BASE", "http://localhost:8000")
AUTH = {"Authorization": f"Bearer {os.environ.get('JWT_DEV_BEARER','devtoken-please-dont-use-in-prod')}"}

st.title("📤 Upload & Organize")

uploaded = st.file_uploader("Select files", accept_multiple_files=True)
if st.button("Upload"):
    keys = []
    for f in uploaded or []:
        init = requests.post(f"{API_BASE}/files/initiate", headers=AUTH, json={
            "filename": f.name, "mime_type": f.type or "application/octet-stream"
        }).json()
        put_url = init["upload_url"]
        r = requests.put(put_url, data=f.getvalue(), headers={"Content-Type": f.type or "application/octet-stream"})
        r.raise_for_status()
        requests.post(f"{API_BASE}/files/complete", headers=AUTH, json={"key": init["key"]})
        keys.append(init["key"])
    if keys:
        st.success("Uploaded:")
        st.code("\n".join(keys))
