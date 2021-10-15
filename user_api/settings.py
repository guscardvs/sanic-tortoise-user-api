from pydantic import BaseSettings, Field

from user_api.utils.functions import project_key_generator


class Settings(BaseSettings):
    project_key: str = Field(default_factory=project_key_generator)


config = Settings()

__all__ = ["config"]
