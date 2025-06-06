import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Rice Classifier API"
    VERSION: str = "1.0.0"
    MODEL_DIR: str = os.getenv("MODEL_DIR", "app/resources/models")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
