import streamlit as st
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

st.set_page_config(page_title="AI-Doc Analyzer", page_icon="🧠")
st.title("🧠 AI-Doc Analyzer")

with st.form("upload"):
    f = st.file_uploader("Carica un PDF", type=["pdf"])
    submitted = st.form_submit_button("Analizza")
    if submitted:
        if not f:
            st.error("Seleziona un file PDF.")
        else:
            with st.spinner("Analisi in corso..."):
                files = {"file": (f.name, f.getvalue(), "application/pdf")}
                r = requests.post(f"{BACKEND_URL}/api/v1/analyze", files=files, timeout=120)
            if r.ok:
                data = r.json()
                st.success("Analisi completata ✅")
                st.subheader("Riassunto")
                st.write(data["summary"])
                st.subheader("Parole chiave")
                st.write(", ".join(data["keywords"]))
            else:
                st.error(f"Errore API: {r.status_code} - {r.text}")
