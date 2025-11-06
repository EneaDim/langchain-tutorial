import os, requests, streamlit as st

API_BASE = os.environ.get("STREAMLIT_API_BASE", "http://localhost:8000")
AUTH = {"Authorization": f"Bearer {os.environ.get('JWT_DEV_BEARER','devtoken-please-dont-use-in-prod')}"}

st.title("🧩 Templates")
st.json(requests.get(f"{API_BASE}/templates", headers=AUTH).json())
