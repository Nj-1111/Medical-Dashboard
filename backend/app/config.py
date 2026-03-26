"""
Configuration Management
Environment-driven settings for the medical diagnosis pipeline
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    APP_NAME: str = "Medical Diagnosis Pipeline"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Server
    SERVER_HOST: str = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT: int = int(os.getenv("SERVER_PORT", "8000"))
    
    # Database Configuration
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "password")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_NAME: str = os.getenv("DB_NAME", "medical_diagnosis")
    DATABASE_URL: str = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    
    # Vector Store (Embeddings)
    VECTOR_DB_HOST: str = os.getenv("VECTOR_DB_HOST", "localhost")
    VECTOR_DB_PORT: int = int(os.getenv("VECTOR_DB_PORT", "6379"))
    
    # Azure Configuration
    AZURE_SUBSCRIPTION_ID: str = os.getenv("AZURE_SUBSCRIPTION_ID", "")
    AZURE_RESOURCE_GROUP: str = os.getenv("AZURE_RESOURCE_GROUP", "")
    AZURE_STORAGE_ACCOUNT: str = os.getenv("AZURE_STORAGE_ACCOUNT", "")
    AZURE_STORAGE_KEY: str = os.getenv("AZURE_STORAGE_KEY", "")
    AZURE_BLOB_CONTAINER: str = os.getenv("AZURE_BLOB_CONTAINER", "medical-images")
    AZURE_KEY_VAULT_URL: str = os.getenv("AZURE_KEY_VAULT_URL", "")
    
    # ML Model Configuration (Configurable per user)
    # These can be changed by simply updating the config
    GLAUCOMA_MODEL_NAME: str = os.getenv(
        "GLAUCOMA_MODEL_NAME", 
        "google/vit-base-patch16-224"  # HuggingFace model ID
    )
    GLAUCOMA_MODEL_VERSION: str = os.getenv("GLAUCOMA_MODEL_VERSION", "1.0.0")
    
    LLM_MODEL_NAME: str = os.getenv(
        "LLM_MODEL_NAME",
        "mistralai/Mistral-7B-Instruct-v0.1"  # HuggingFace model ID
    )
    LLM_MODEL_VERSION: str = os.getenv("LLM_MODEL_VERSION", "1.0.0")
    
    # Model Loading Configuration
    LOAD_MODELS_ON_STARTUP: bool = (
        os.getenv("LOAD_MODELS_ON_STARTUP", "True").lower() == "true"
    )
    MODEL_CACHE_DIR: str = os.getenv("MODEL_CACHE_DIR", "./model_cache")
    MODEL_DEVICE: str = os.getenv("MODEL_DEVICE", "cuda")  # cuda or cpu
    
    # Security & Authentication
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "your-secret-key-change-in-production"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # OAuth/OIDC Configuration
    OIDC_DISCOVERY_URL: str = os.getenv(
        "OIDC_DISCOVERY_URL",
        "https://login.microsoftonline.com/common/v2.0/.well-known/openid-configuration"
    )
    OAUTH_CLIENT_ID: str = os.getenv("OAUTH_CLIENT_ID", "")
    OAUTH_CLIENT_SECRET: str = os.getenv("OAUTH_CLIENT_SECRET", "")
    OAUTH_REDIRECT_URI: str = os.getenv(
        "OAUTH_REDIRECT_URI",
        "http://localhost:3000/callback"
    )
    
    # File Upload Configuration
    MAX_UPLOAD_SIZE_MB: int = 50
    ALLOWED_FILE_EXTENSIONS: list = ["jpg", "jpeg", "png", "dcm", "pdf"]
    
    # Virus Scanning
    ENABLE_VIRUS_SCAN: bool = (
        os.getenv("ENABLE_VIRUS_SCAN", "True").lower() == "true"
    )
    CLAMAV_HOST: str = os.getenv("CLAMAV_HOST", "localhost")
    CLAMAV_PORT: int = int(os.getenv("CLAMAV_PORT", "3310"))
    
    # Logging & Audit
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    AUDIT_LOG_ENABLED: bool = (
        os.getenv("AUDIT_LOG_ENABLED", "True").lower() == "true"
    )
    
    # CORS Configuration
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8000",
        os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Initialize settings
settings = Settings()
