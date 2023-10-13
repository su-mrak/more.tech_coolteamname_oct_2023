import multiprocessing as mp

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    pg_database: str = "db_main"
    pg_host: str = "localhost"
    pg_port: int = 5432
    pg_username: str = "db_main"
    pg_password: str = "db_main"

    uvicorn_host: str = "localhost"
    uvicorn_port: int = 8000
    uvicorn_workers: int = mp.cpu_count() * 2
    uvicorn_log_level: str = "WARNING"

    redis_host: str = "localhost"
    redis_port: int = 6379

    model_config = SettingsConfigDict(env_prefix="_", env_file=".env")


app_settings = AppSettings()
