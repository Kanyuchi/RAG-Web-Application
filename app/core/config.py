"""
Core configuration module using Pydantic Settings.
Loads environment variables and provides centralized configuration.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, PostgresDsn
from typing import Optional
import os
from pathlib import Path


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Application Settings
    app_name: str = Field(default="RAG Web Application", alias="APP_NAME")
    app_version: str = Field(default="1.0.0", alias="APP_VERSION")
    debug: bool = Field(default=True, alias="DEBUG")
    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8000, alias="PORT")

    # API Keys
    openai_api_key: str = Field(alias="OPENAI_API_KEY")
    anthropic_api_key: str = Field(alias="ANTHROPIC_API_KEY")
    firecrawl_api_key: Optional[str] = Field(default=None, alias="FIRECRAWL_API_KEY")
    perplexity_api_key: Optional[str] = Field(default=None, alias="PERPLEXITY_API_KEY")

    # Database Configuration
    database_url: str = Field(
        default="postgresql://user:password@localhost:5432/rag_db",
        alias="DATABASE_URL"
    )

    # MongoDB (alternative - if needed later)
    mongodb_url: Optional[str] = Field(default=None, alias="MONGODB_URL")
    mongodb_db_name: Optional[str] = Field(default="rag_database", alias="MONGODB_DB_NAME")

    # Vector Database Configuration (Qdrant)
    qdrant_host: str = Field(default="localhost", alias="QDRANT_HOST")
    qdrant_port: int = Field(default=6333, alias="QDRANT_PORT")
    qdrant_collection_name: str = Field(default="rag_documents", alias="QDRANT_COLLECTION_NAME")
    qdrant_api_key: Optional[str] = Field(default=None, alias="QDRANT_API_KEY")
    qdrant_url: Optional[str] = Field(default=None, alias="QDRANT_URL")

    # Google Drive Integration
    google_client_id: Optional[str] = Field(default=None, alias="GOOGLE_CLIENT_ID")
    google_client_secret: Optional[str] = Field(default=None, alias="GOOGLE_CLIENT_SECRET")
    google_redirect_uri: str = Field(
        default="http://localhost:8000/auth/callback",
        alias="GOOGLE_REDIRECT_URI"
    )

    # File Storage Configuration
    upload_dir: str = Field(default="./data/uploads", alias="UPLOAD_DIR")
    processed_dir: str = Field(default="./data/processed", alias="PROCESSED_DIR")
    max_file_size: int = Field(default=50000000, alias="MAX_FILE_SIZE")  # 50MB

    # Chunking Configuration
    chunk_size: int = Field(default=1000, alias="CHUNK_SIZE")
    chunk_overlap: int = Field(default=200, alias="CHUNK_OVERLAP")

    # Embedding Configuration
    embedding_model: str = Field(default="all-MiniLM-L6-v2", alias="EMBEDDING_MODEL")
    embedding_dimension: int = Field(default=384, alias="EMBEDDING_DIMENSION")

    # Query Configuration
    top_k_results: int = Field(default=5, alias="TOP_K_RESULTS")
    similarity_threshold: float = Field(default=0.7, alias="SIMILARITY_THRESHOLD")

    # Security
    secret_key: str = Field(
        default="your_secret_key_here_change_in_production",
        alias="SECRET_KEY"
    )
    algorithm: str = Field(default="HS256", alias="ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    # CORS Settings
    cors_origins: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        alias="CORS_ORIGINS"
    )

    @property
    def upload_path(self) -> Path:
        """Get upload directory as Path object."""
        path = Path(self.upload_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def processed_path(self) -> Path:
        """Get processed directory as Path object."""
        path = Path(self.processed_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def qdrant_connection_string(self) -> str:
        """Get Qdrant connection string."""
        if self.qdrant_url:
            return self.qdrant_url
        return f"http://{self.qdrant_host}:{self.qdrant_port}"

    def get_llm_config(self, provider: str = "openai") -> dict:
        """Get LLM configuration for specified provider."""
        if provider.lower() == "openai":
            return {
                "api_key": self.openai_api_key,
                "model": "gpt-4o",
                "temperature": 0.2,
                "max_tokens": 500
            }
        elif provider.lower() == "anthropic":
            return {
                "api_key": self.anthropic_api_key,
                "model": "claude-3-5-sonnet-20241022",
                "max_tokens": 1024
            }
        else:
            raise ValueError(f"Unknown LLM provider: {provider}")


# Global settings instance
settings = Settings()


# Ensure required directories exist
settings.upload_path.mkdir(parents=True, exist_ok=True)
settings.processed_path.mkdir(parents=True, exist_ok=True)
