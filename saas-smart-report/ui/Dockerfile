FROM python:3.11-slim

WORKDIR /app

COPY ui/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY ui /app/ui

ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
EXPOSE 8501

CMD ["streamlit","run","/app/ui/streamlit_app.py","--server.port=8501","--server.address=0.0.0.0"]
