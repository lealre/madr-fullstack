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

    EMAIL_USERNAME: str
    EMAIL_PASSWORD: str
    EMAIL_FROM: str
    EMAIL_PORT: int = 587
    EMAIL_SERVER: str
    EMAIL_FROM_NAME: str
    EMAIL_STARTTLS: bool = True
    EMAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True
    TEMPLATE_FOLDER: str = 'src/email/templates'

    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str = 'http://127.0.0.1:8000/auth/callback/google'


settings = Settings()
