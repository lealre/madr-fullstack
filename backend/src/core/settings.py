from pathlib import Path

from pydantic import DirectoryPath, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )

    DATABASE_URL: str = 'sqlite+aiosqlite:///./database.db'

    SECRET_KEY: str = 'your-secret-key'
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    FIRST_SUPERUSER_USERNAME: str = 'admin'
    FIRST_SUPERUSER_EMAIL: str = 'admin@admin.com'
    FIRST_SUPERUSER_PASSWORD: str = 'admin'

    EMAIL_USERNAME: str = ''
    EMAIL_PASSWORD: SecretStr = SecretStr('')
    EMAIL_FROM: str = ''
    EMAIL_PORT: int = 587
    EMAIL_SERVER: str = ''
    EMAIL_FROM_NAME: str = ''
    EMAIL_STARTTLS: bool = True
    EMAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True
    TEMPLATE_FOLDER: DirectoryPath = Path('src/email/templates')


settings = Settings()
