FROM python:3.11-slim
WORKDIR /app

# Install API deps
COPY api/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Add shared code and API
COPY common /app/common
COPY api /app/api

ENV PYTHONPATH=/app
EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
