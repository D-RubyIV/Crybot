from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DBPATH: str = "database.db"

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()