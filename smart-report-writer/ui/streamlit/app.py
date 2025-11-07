import io, json, time
import streamlit as st
from ui.streamlit import api_client as api

st.set_page_config(page_title="Smart Report Writer", layout="wide")

# State
ss = st.session_state
ss.setdefault("doc", None)
ss.setdefault("doc_meta", {})
ss.setdefault("job_id", None)
ss.setdefault("artifact_url", None)

st.title("📄 Smart Report Writer")

col_left, col_right = st.columns([5,7], gap="large")

with col_left:
    st.subheader("1) Upload")
    file = st.file_uploader("Drop a document, dataset, code, archive, or media file", type=None)
    if file and st.button("Upload", use_container_width=True):
        with st.spinner("Uploading..."):
            data = api.upload(file)
            ss.doc = data.get("document_id") or data.get("id")
            ss.doc_meta = {
                "kind": data.get("content_kind"),
                "filename": file.name,
                "size": len(file.getvalue()),
            }
        st.success(f"Uploaded {ss.doc_meta.get('filename')} (kind: {ss.doc_meta.get('kind')})")

    st.subheader("2) Configure")
    provs = api.providers()
    # Provider/model selector with sensible defaults
    prov_list = provs.get("providers") or ["LLAMA_OLLAMA","QWEN_OLLAMA","OPENAI","VLLM"]
    provider = st.selectbox("LLM Provider", prov_list, index=0)
    model = st.text_input("Model", value="llama3:8b-instruct" if provider=="LLAMA_OLLAMA" else ("qwen2:7b-instruct" if provider=="QWEN_OLLAMA" else "gpt-4o-mini"))
    temperature = st.slider("Temperature", 0.0, 1.0, 0.1, 0.1)
    max_tokens = st.number_input("Max tokens", 256, 8192, 2048, 64)

    st.subheader("3) Template")
    templates = api.list_templates()
    items = templates.get("items") or templates.get("templates") or []
    by_name = {f"{t.get('id','')}: {t.get('description','')}" or t.get('id',''): t for t in items}
    choice = st.selectbox("Pick a template", list(by_name.keys()) or ["executive_summary"])
    template_id = by_name.get(choice, {}).get("id") or "executive_summary"

    st.subheader("4) Generate")
    if st.button("Generate Report", use_container_width=True, disabled=not ss.get("doc")):
        if not ss.get("doc"):
            st.warning("Upload a file first.")
        else:
            payload = {
                "document_id": ss["doc"],
                "template_id": template_id,
                "overrides": {"provider": provider, "model": model, "temperature": temperature, "max_tokens": max_tokens},
            }
            with st.spinner("Submitting job..."):
                res = api.generate(payload)
                ss.job_id = res.get("job_id") or res.get("id")
                ss.artifact_url = None
            st.info(f"Job submitted: {ss.job_id}")

with col_right:
    st.subheader("Preview & Status")
    if ss.get("doc_meta"):
        with st.expander("Uploaded file details", expanded=True):
            st.json(ss["doc_meta"], expanded=False)

    if ss.get("job_id") and not ss.get("artifact_url"):
        with st.spinner("Processing..."):
            for _ in range(120):  # up to ~60s with sleep(0.5)
                js = api.job_status(ss["job_id"])
                status = js.get("status","unknown")
                st.write(f"Status: **{status}**")
                if status in ("succeeded","completed","done"):
                    url = api.job_artifact(ss["job_id"])
                    ss.artifact_url = url
                    break
                if status in ("failed","error"):
                    st.error(js.get("error","Generation failed"))
                    break
                time.sleep(0.5)

    if ss.get("artifact_url"):
        st.success("Report is ready!")
        st.markdown(f"[⬇️ Download artifact]({ss['artifact_url']})")
