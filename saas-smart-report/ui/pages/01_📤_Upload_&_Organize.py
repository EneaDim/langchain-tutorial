import os, requests, streamlit as st, mimetypes

API_BASE = os.environ.get("STREAMLIT_API_BASE", "http://api:8000")
AUTH = {"Authorization": f"Bearer {os.environ.get('JWT_DEV_BEARER','devtoken-please-dont-use-in-prod')}"}

st.title("📤 Upload & Organize")

uploaded = st.file_uploader("Select files", accept_multiple_files=True)
if st.button("Upload"):
    keys = []
    for f in uploaded or []:
        guessed = mimetypes.guess_type(f.name)[0]
        mime = (getattr(f, "type", None) or guessed or "application/octet-stream")
        mime = mime.split(";")[0].strip()
        data = f.getvalue()
        init_resp = requests.post(
            f"{API_BASE}/files/initiate",
            headers=AUTH,
            json={"filename": f.name, "mime_type": mime, "size": len(data)},
            timeout=15,
        )
        init_resp.raise_for_status()
        init = init_resp.json()
        put_url = init["upload_url"]
        r = requests.put(put_url, data=data, headers={"Content-Type": mime}, timeout=60)
        r.raise_for_status()
        done = requests.post(f"{API_BASE}/files/complete", headers=AUTH, json={"key": init["key"]}, timeout=15)
        done.raise_for_status()
        keys.append(init["key"])
    if keys:
        st.success("Uploaded:")
        st.code("\n".join(keys))
