from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra='allow'
    )

    DATABASE_URL: str = 'sqlite+aiosqlite:///./database.db'

    SECRET_KEY: str = 'your-secret-key'
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    FIRST_SUPERUSER_USERNAME: str = 'admin'
    FIRST_SUPERUSER_EMAIL: str = 'admin@admin.com'
    FIRST_SUPERUSER_PASSWORD: str = 'admin'


settings = Settings()
