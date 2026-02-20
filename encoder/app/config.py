from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Encoder service settings."""

    splade_model: str = "hotchpotch/japanese-splade-v2"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
