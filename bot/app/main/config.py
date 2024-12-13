import toml

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.schemas import AdminConfig, WebConfig

from typing import Union


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
    FREEKASSA_SHOP_ID: str
    FREEKASSA_API_KEY: str
    BOT_TOKEN: str
    BRAWL_STARS_API_KEY: str
    CONFIG_PATH: str
    YANDEX_STORAGE_TOKEN: str
    YANDEX_STORAGE_SECRET: str
    YANDEX_STORAGE_BUCKET_NAME: str
    
    model_config = SettingsConfigDict(env_file=".env")

    @property
    def db_connection_url(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.DB_HOST}/{self.DB_NAME}"
    
    def referral_url(self, referral_code: Union[str, int]) -> str:
        return f"{self.BOT_URL}?start=ref_{referral_code}"


settings = Settings()


def load_toml_config() -> TomlConfig:
    with open(".config/dev.config.toml") as fd:
        cfg = TomlConfig.model_validate(toml.load(fd))
        return cfg


dev_config = load_toml_config()
