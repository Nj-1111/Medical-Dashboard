"""
Configuration Management
Environment-driven settings for the medical diagnosis pipeline
"""
import logging
import warnings
from typing import List, Optional
from pydantic import computed_field, model_validator
from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)

_INSECURE_SECRET_KEY = "your-secret-key-change-in-production"


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application
    APP_NAME: str = "Medical Diagnosis Pipeline"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Server
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000

    # Database Configuration
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "password"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "medical_diagnosis"

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    # Vector Store (Embeddings)
    VECTOR_DB_HOST: str = "localhost"
    VECTOR_DB_PORT: int = 6379

    # Azure Configuration
    AZURE_SUBSCRIPTION_ID: str = ""
    AZURE_RESOURCE_GROUP: str = ""
    AZURE_STORAGE_ACCOUNT: str = ""
    AZURE_STORAGE_KEY: str = ""
    AZURE_BLOB_CONTAINER: str = "medical-images"
    AZURE_KEY_VAULT_URL: str = ""

    # ML Model Configuration (Configurable per user)
    # These can be changed by simply updating the config
    GLAUCOMA_MODEL_NAME: str = "google/vit-base-patch16-224"  # HuggingFace model ID
    GLAUCOMA_MODEL_VERSION: str = "1.0.0"

    LLM_MODEL_NAME: str = "mistralai/Mistral-7B-Instruct-v0.1"  # HuggingFace model ID
    LLM_MODEL_VERSION: str = "1.0.0"

    # Model Loading Configuration
    LOAD_MODELS_ON_STARTUP: bool = True
    MODEL_CACHE_DIR: str = "./model_cache"
    MODEL_DEVICE: str = "cuda"  # cuda or cpu

    # Security & Authentication
    SECRET_KEY: str = _INSECURE_SECRET_KEY
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # OAuth/OIDC Configuration
    OIDC_DISCOVERY_URL: str = (
        "https://login.microsoftonline.com/common/v2.0/.well-known/openid-configuration"
    )
    OAUTH_CLIENT_ID: str = ""
    OAUTH_CLIENT_SECRET: str = ""
    OAUTH_REDIRECT_URI: str = "http://localhost:3000/callback"

    # File Upload Configuration
    MAX_UPLOAD_SIZE_MB: int = 50
    ALLOWED_FILE_EXTENSIONS: List[str] = ["jpg", "jpeg", "png", "dcm", "pdf"]

    # Virus Scanning
    ENABLE_VIRUS_SCAN: bool = True
    CLAMAV_HOST: str = "localhost"
    CLAMAV_PORT: int = 3310

    # Logging & Audit
    LOG_LEVEL: str = "INFO"
    AUDIT_LOG_ENABLED: bool = True

    # CORS Configuration – comma-separated origins in the env var ALLOWED_ORIGINS
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:8000"

    @computed_field
    @property
    def ALLOWED_ORIGINS_LIST(self) -> List[str]:
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(",") if o.strip()]

    @model_validator(mode="after")
    def warn_insecure_secret_key(self) -> "Settings":
        if self.SECRET_KEY == _INSECURE_SECRET_KEY:
            if not self.DEBUG:
                raise ValueError(
                    "SECRET_KEY must be set to a strong random value in production. "
                    "Set the SECRET_KEY environment variable."
                )
            warnings.warn(
                "SECRET_KEY is set to the insecure default value. "
                "Set a strong random SECRET_KEY environment variable before deploying.",
                stacklevel=2,
            )
        return self

    model_config = {"env_file": ".env", "case_sensitive": True}


# Initialize settings
settings = Settings()
