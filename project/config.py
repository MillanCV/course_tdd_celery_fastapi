import pathlib
from functools import lru_cache
from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    BASE_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent
    DATABASE_URL: str = f"sqlite:///{BASE_DIR}/db.sqlite3"
    DATABASE_CONNECT_DICT: dict = {}
    ENVIRONMENT: str = "development"  # Default environment
    
    CELERY_BROKER_URL: str = "redis://127.0.0.1:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://127.0.0.1:6379/0"

    WS_MESSAGE_QUEUE: str = os.environ.get("WS_MESSAGE_QUEUE", "redis://127.0.0.1:6379/0")
    
    class Config:
        env_file = ".env"  # Specify the environment file to load variables from .env


class DevelopmentConfig(BaseConfig):
    DEBUG: bool = True


class ProductionConfig(BaseConfig):
    DEBUG: bool = False


class TestingConfig(BaseConfig):
    TESTING: bool = True
    DATABASE_URL: str = "sqlite:///test_db.sqlite3"


@lru_cache()
def get_settings():
    config_cls_dict = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig
    }

    # Load the environment name from the ENVIRONMENT variable
    config_name = BaseConfig().ENVIRONMENT
    config_cls = config_cls_dict.get(config_name, DevelopmentConfig) 
    return config_cls()


settings = get_settings()
