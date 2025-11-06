FROM python:3.11-slim
WORKDIR /app

COPY ui/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ui /app/ui
ENV PYTHONPATH=/app
EXPOSE 8501
CMD ["streamlit", "run", "ui/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
