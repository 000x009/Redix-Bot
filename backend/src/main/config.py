from typing import Union, List

from pydantic_settings import BaseSettings, SettingsConfigDict

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

    @property
    def db_connection_url(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.DB_HOST}/{self.DB_NAME}"
    
    def referral_url(self, referral_code: Union[str, int]) -> str:
        return f"{self.BOT_URL}?start=ref_{referral_code}"


settings = Settings()
