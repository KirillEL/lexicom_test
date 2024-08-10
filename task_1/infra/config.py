import os
from pathlib import Path
from typing import Optional

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    model_config = ConfigDict(extra='ignore')
    ENV: Optional[str] = "dev"
    DEBUG: Optional[bool] = True
    APP_HOST: str
    APP_PORT: int
    REDIS_PASSWORD: str
    REDIS_USER: str
    REDIS_USER_PASSWORD: str


class LocalConfig(Config):
    pass


class DevConfig(Config):
    pass


class ProdConfig(Config):
    DEBUG: Optional[str] = False


def get_config(env_file: str):
    env = os.getenv("ENV", "local")
    env_types = {
        "local": LocalConfig(_env_file=env_file),
        "dev": DevConfig(_env_file=env_file),
        "prod": ProdConfig(_env_file=env_file)
    }
    return env_types[env]


config: Config = get_config(
    env_file=os.path.join(Path(__file__).parents[1], ".env")
)
