import os, requests, streamlit as st

API_BASE = os.environ.get("STREAMLIT_API_BASE", "http://localhost:8000")
AUTH = {"Authorization": f"Bearer {os.environ.get('JWT_DEV_BEARER','devtoken-please-dont-use-in-prod')}"}

st.title("📦 Results & Downloads")

jid = st.text_input("Job ID", value=st.session_state.get("last_job_id",""))
if st.button("Check"):
    if not jid:
        st.warning("Enter a job id")
    else:
        data = requests.get(f"{API_BASE}/jobs/{jid}", headers=AUTH).json()
        st.write(data)
        if data.get("artifacts"):
            st.write("Artifacts:")
            for url in data["artifacts"]:
                st.write(url)
