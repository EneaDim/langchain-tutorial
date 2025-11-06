import os
import requests
import streamlit as st

API_BASE = os.environ.get("API_BASE", "http://api:8000")

st.set_page_config(page_title="Smart Report Writer", layout="wide")

st.title("Smart Report Writer — SaaS")
st.caption("Streamlit UI • FastAPI • Celery (dev mode: no login)")

# ----------------------------
# Sidebar settings (dev mode)
# ----------------------------
with st.sidebar:
    st.markdown("### Settings")
    token = st.text_input("Bearer Token", value="dev-token", type="password")
    topic = st.text_input("Topic", value="Q4 Ops Review")
    model = st.text_input("Model", value=os.environ.get("OLLAMA_MODEL", "llama3.2:latest"))
    try:
        default_temp = float(os.environ.get("MODEL_TEMPERATURE", "0.2"))
    except ValueError:
        default_temp = 0.2
    temp = st.number_input("Temperature", value=default_temp, min_value=0.0, max_value=1.0, step=0.1)
    st.divider()
    st.markdown("Use the main page to upload and run jobs.")

# ----------------------------
# Upload & Organize
# ----------------------------
st.header("Upload & Organize")

uploads = st.file_uploader("Upload files", accept_multiple_files=True)
local_paths = []

if uploads:
    # Ensure shared path exists (shared volume across UI + API)
    base_dir = "/shared/uploads"
    os.makedirs(base_dir, exist_ok=True)

    for f in uploads:
        # Save each uploaded file into the shared volume
        save_path = os.path.join(base_dir, f.name)
        with open(save_path, "wb") as fh:
            fh.write(f.getbuffer())
        local_paths.append(save_path)

    st.success(f"Saved {len(local_paths)} file(s) to {base_dir}")

# ----------------------------
# Run Summary
# ----------------------------
if st.button("Run Summary"):
    if not local_paths:
        st.warning("Please upload at least one file first.")
    else:
        with st.spinner("Creating job..."):
            headers = {"Authorization": f"Bearer {token}"}
            payload = {
                "file_ids": local_paths,   # API expects local paths (dev mode)
                "topic": topic,
                "model": model,
                "temperature": temp,
            }
            try:
                r = requests.post(f"{API_BASE}/v1/jobs", json=payload, headers=headers, timeout=600)
                if r.ok:
                    data = r.json()
                    st.session_state["job_id"] = data.get("id")
                    st.success(f"Job created: {data.get('id')} (status: {data.get('status')})")
                else:
                    st.error(f"API error: {r.status_code} {r.text}")
            except Exception as e:
                st.error(f"Request failed: {e}")

# ----------------------------
# Results & Downloads
# ----------------------------
st.header("Results & Downloads")

job_id = st.text_input("Job ID", value=st.session_state.get("job_id", ""))

if st.button("Refresh Status"):
    if not job_id:
        st.warning("Enter a Job ID (or run a job first).")
    else:
        headers = {"Authorization": f"Bearer {token}"}
        try:
            r = requests.get(f"{API_BASE}/v1/jobs/{job_id}", headers=headers, timeout=60)
            if r.ok:
                data = r.json()
                st.write(f"Status: **{data.get('status')}**")
                artifacts = data.get("artifacts") or {}
                if not artifacts:
                    st.info("No artifacts yet. If status is 'running', try again in a few seconds.")
                for name, url in artifacts.items():
                    st.write(f"- **{name}**: {url}")
            else:
                st.error(f"API error: {r.status_code} {r.text}")
        except Exception as e:
            st.error(f"Request failed: {e}")
