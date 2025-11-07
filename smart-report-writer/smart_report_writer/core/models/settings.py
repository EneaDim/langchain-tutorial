from pydantic_settings import BaseSettings
from pydantic import Field

class AppSettings(BaseSettings):
    app_env: str = Field("dev", alias="APP_ENV")
    api_rate_limit_per_min: int = Field(120, alias="API_RATE_LIMIT_PER_MIN")

    db_host: str = Field("db", alias="DB_HOST")
    db_port: int = Field(5432, alias="DB_PORT")
    db_user: str = Field("srw", alias="DB_USER")
    db_password: str = Field("srwpass", alias="DB_PASSWORD")
    db_name: str = Field("srw", alias="DB_NAME")

    s3_endpoint_url: str = Field(..., alias="S3_ENDPOINT_URL")
    s3_region: str = Field("us-east-1", alias="S3_REGION")
    s3_access_key: str = Field(..., alias="S3_ACCESS_KEY")
    s3_secret_key: str = Field(..., alias="S3_SECRET_KEY")
    s3_bucket: str = Field("srw", alias="S3_BUCKET")
    s3_secure: bool = Field(False, alias="S3_SECURE")
    s3_server_side_encryption: bool = Field(False, alias="S3_SERVER_SIDE_ENCRYPTION")

    provider_default: str = Field("LLAMA_OLLAMA", alias="PROVIDER_DEFAULT")
    model_default: str = Field("llama3:8b-instruct", alias="MODEL_DEFAULT")
    secondary_provider_default: str = Field("QWEN_OLLAMA", alias="SECONDARY_PROVIDER_DEFAULT")
    secondary_model_default: str = Field("qwen2:7b-instruct", alias="SECONDARY_MODEL_DEFAULT")

    ollama_base_url: str = Field("http://ollama:11434", alias="OLLAMA_BASE_URL")
    vllm_endpoint: str = Field("http://vllm:8000", alias="VLLM_ENDPOINT")
    openai_api_key: str = Field("", alias="OPENAI_API_KEY")
    openai_base_url: str = Field("", alias="OPENAI_BASE_URL")

    feature_ocr: bool = Field(True, alias="FEATURE_OCR")
    feature_stt: bool = Field(True, alias="FEATURE_STT")
    feature_url_fetch: bool = Field(False, alias="FEATURE_URL_FETCH")
    feature_db_dumps: bool = Field(False, alias="FEATURE_DB_DUMPS")

    allowed_origins: str = Field("*", alias="ALLOWED_ORIGINS")
    max_upload_mb: int = Field(200, alias="MAX_UPLOAD_MB")

    class Config:
        env_file = ".env"
        extra = "ignore"
