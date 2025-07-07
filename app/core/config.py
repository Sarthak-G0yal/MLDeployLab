import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "PyTorch Model API"
    MODEL_DIR: str = os.getenv("MODEL_DIR", "resources/models")
    ENCODER_DIR: str = os.getenv("ENCODER_DIR", "resources/encoders")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
