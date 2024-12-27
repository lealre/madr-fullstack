from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from src.core.settings import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.EMAIL_USERNAME,
    MAIL_PASSWORD=settings.EMAIL_PASSWORD,
    MAIL_FROM=settings.EMAIL_FROM,
    MAIL_PORT=settings.EMAIL_PORT,
    MAIL_SERVER=settings.EMAIL_SERVER,
    MAIL_FROM_NAME=settings.EMAIL_FROM_NAME,
    MAIL_STARTTLS=settings.EMAIL_STARTTLS,
    MAIL_SSL_TLS=settings.EMAIL_SSL_TLS,
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
    VALIDATE_CERTS=settings.VALIDATE_CERTS,
    TEMPLATE_FOLDER=settings.TEMPLATE_FOLDER,
)

email = FastMail(config=conf)


def create_email_message(
    recipients: list[str], subject: str, body: str
) -> MessageSchema:
    message = MessageSchema(
        recipients=recipients,
        subject=subject,
        body=body,
        subtype=MessageType.html,
    )

    return message
