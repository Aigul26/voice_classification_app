from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: str
    POSTGRES_HOST: str
    POSTGRES_DB: str
    APP_HOST_PORT: str
    SECRET_KEY: str
    ALGORITHM: str
    PATH: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    @property
    def database_url(self) -> str:
        user = self.POSTGRES_USER
        password = self.POSTGRES_PASSWORD
        host = self.POSTGRES_HOST
        port = self.POSTGRES_PORT
        db = self.POSTGRES_DB
        return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
    
settings = Settings()
