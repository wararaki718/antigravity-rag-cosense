from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Batch ingestion settings."""

    # Cosense
    cosense_project: str = "stacker8"
    cosense_sid: str = ""

    # Elasticsearch
    elasticsearch_url: str = "http://localhost:9200"
    elasticsearch_index: str = "cosense_pages"

    # Encoder API
    encoder_url: str = "http://localhost:8001"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
