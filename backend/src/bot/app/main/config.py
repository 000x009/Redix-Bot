import toml

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.bot.app.schemas import AdminConfig, WebConfig


class TomlConfig(BaseModel):
    admin: AdminConfig
    web: WebConfig


class Settings(BaseSettings):
    DB_NAME: str
    POSTGRES_USER: str
    DB_HOST: str
    DB_PORT: str
    POSTGRES_PASSWORD: str
    BOT_URL: str
    BILEE_SHOP_ID: str
    BILEE_PASSWORD: str
    BOT_TOKEN: str
    CONFIG_PATH: str
    YANDEX_STORAGE_TOKEN: str
    YANDEX_STORAGE_SECRET: str
    YANDEX_STORAGE_BUCKET_NAME: str
    
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()


def load_toml_config() -> TomlConfig:
    with open(settings.CONFIG_PATH) as fd:
        cfg = TomlConfig.model_validate(toml.load(fd))
        return cfg


dev_config = load_toml_config()
