from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    app_name: str = 'YEG Shadow Inventory API'
    environment: str = Field(default='development', alias='ENVIRONMENT')
    database_url: str = Field(default='postgresql://user:pass@localhost:5432/yeg_shadow', alias='DATABASE_URL')
    redis_url: str = Field(default='redis://localhost:6379/0', alias='REDIS_URL')

    crawl_rate_limit: float = Field(default=2.0, alias='CRAWL_RATE_LIMIT')
    crawl_max_concurrent: int = Field(default=10, alias='CRAWL_MAX_CONCURRENT')
    cors_origins: str = Field(default='*', alias='CORS_ORIGINS')


@lru_cache
def get_settings() -> Settings:
    return Settings()
