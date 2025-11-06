import os, streamlit as st

API_BASE = os.environ.get("STREAMLIT_API_BASE", "http://localhost:8000")

st.set_page_config(page_title="Smart Report Writer", layout="wide")
st.title("Smart Report Writer")

st.sidebar.success("Use the pages to upload, run, and download artifacts.")

st.write("Welcome! Go to **Upload & Organize** to begin.")
