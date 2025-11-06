import os, streamlit as st
st.title("⚙️ Settings")
for k in ("STREAMLIT_API_BASE","JWT_DEV_BEARER"):
    st.write(k, os.environ.get(k))
