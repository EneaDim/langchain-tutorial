from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List

class Settings(BaseSettings):
    postgres_dsn: str = Field(alias="POSTGRES_DSN")
    redis_url: str = Field(alias="REDIS_URL")
    s3_endpoint: str = Field(alias="S3_ENDPOINT")
    s3_bucket: str = Field(alias="S3_BUCKET")
    s3_region: str = Field(alias="S3_REGION")
    s3_access_key: str = Field(alias="S3_ACCESS_KEY")
    s3_secret_key: str = Field(alias="S3_SECRET_KEY")

    oidc_issuer: str = Field(alias="OIDC_ISSUER")
    oidc_audience: str = Field(alias="OIDC_AUDIENCE")
    oidc_client_id: str = Field(alias="OIDC_CLIENT_ID")
    oidc_client_secret: str = Field(alias="OIDC_CLIENT_SECRET")
    cors_origins: str = Field(default="http://localhost:8501", alias="CORS_ORIGINS")

    llm_provider: str = Field(default="ollama", alias="LLM_PROVIDER")
    ollama_base_url: str = Field(default="http://localhost:11434", alias="OLLAMA_BASE_URL")
    ollama_model: str = Field(default="llama3.2:latest", alias="OLLAMA_MODEL")
    model_temperature: float = Field(default=0.2, alias="MODEL_TEMPERATURE")

    srw_per_file_cap: int = Field(default=12000, alias="SRW_PER_FILE_CAP")
    srw_total_cap: int = Field(default=150000, alias="SRW_TOTAL_CAP")

    feature_docx: bool = Field(default=True, alias="FEATURE_DOCX")
    feature_pii_redaction: bool = Field(default=False, alias="FEATURE_PII_REDACTION")
    rate_limit_per_min: int = Field(default=60, alias="RATE_LIMIT_PER_MIN")
    max_upload_mb: int = Field(default=50, alias="MAX_UPLOAD_MB")
    allowed_mime_list: str = Field(default="text/plain", alias="ALLOWED_MIME_LIST")

    model_config = {
        'env_file': '.env',
        'case_sensitive': True,
        'protected_namespaces': ('settings_',),
    }

settings = Settings()
