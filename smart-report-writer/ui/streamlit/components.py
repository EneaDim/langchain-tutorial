import streamlit as st
from ui.streamlit import api_client as api

def uploader():
    st.subheader("Upload")
    f = st.file_uploader("Upload a file", type=None)
    if f and st.button("Send"):
        data = api.upload(f)
        st.success(f"Uploaded. Document ID: {data['document_id']}")
        return data
    return None

def generator(document_id: str):
    st.subheader("Generate Report")
    tpls = api.templates()
    tpl = st.selectbox("Template", tpls, format_func=lambda t: f"{t['title']} ({t['content_kind']})")
    if st.button("Generate"):
        resp = api.generate(document_id, tpl["id"])
        st.info(f"Job ID: {resp['job_id']}")
        return resp
    return None

def status(job_id: str):
    st.subheader("Status")
    st.write(api.job(job_id))
