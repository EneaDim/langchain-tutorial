import streamlit as st

def init_state():
    if "document_id" not in st.session_state:
        st.session_state.document_id = None
    if "job_id" not in st.session_state:
        st.session_state.job_id = None
