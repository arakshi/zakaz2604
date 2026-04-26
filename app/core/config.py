from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: str = "sqlite+pysqlite:///./sales.db"
    redis_url: str = "redis://localhost:6379/0"
    secret_key: str = "dev_secret"
    access_token_expire_minutes: int = 1440
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000


settings = Settings()
