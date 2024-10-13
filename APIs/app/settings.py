from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Uvicorn config
    HOST: str = "0.0.0.0"
    RELOAD: bool = True
    WORKERS: int = 2
    PORT: int

    class Config:
        env_file = ".env"
