from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    app_name: str = 'YEG Shadow Inventory API'
    environment: str = Field(default='development', alias='ENVIRONMENT')
    database_url: str = Field(default='postgresql://user:pass@localhost:5432/yeg_shadow', alias='DATABASE_URL')
    redis_url: str = Field(default='redis://localhost:6379/0', alias='REDIS_URL')

    api_port: int = Field(default=8000, alias='PORT')
    cors_origins: str = Field(default='http://localhost:3000', alias='BACKEND_CORS_ORIGINS')

    crawl_rate_limit: float = Field(default=2.0, alias='CRAWL_RATE_LIMIT')
    crawl_max_concurrent: int = Field(default=10, alias='CRAWL_MAX_CONCURRENT')

    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(',') if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
