from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="DT_", extra="ignore")

    environment: str = "dev"
    host: str = "0.0.0.0"
    port: int = 8080
    log_level: str = "INFO"
    database_url: str = "sqlite:///./data/digital_technical.db"
    ai_provider: str = "deterministic"
    ai_base_url: str = "https://api.openai.com/v1"
    ai_model: str = "provider-model-name"
    ai_api_key: str = ""
    api_key: str = ""
    require_api_key: bool = False
    knowledge_file: str = "examples/knowledge.json"
    cloud_provider: str = "local"


@lru_cache
def get_settings() -> Settings:
    return Settings()
