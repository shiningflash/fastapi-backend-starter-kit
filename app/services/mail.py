from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pathlib import Path
from fastapi.templating import Jinja2Templates

from core.config import settings


# Landing page template
templates = Jinja2Templates(directory=Path(__file__).parent / '../../templates/email')


conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER='./templates/email'
)


async def send_email_async(subject: str, email_to: str, body: dict):
    try:
        message = MessageSchema(
            subject=subject,
            recipients=[email_to],
            template_body=body,
            subtype='html',
        )
        fm = FastMail(conf)
        await fm.send_message(message, template_name='invitation.html')
    except:
        raise Exception("Email Service Down")


def send_email_background(background_tasks: BackgroundTasks, subject: str, email_to: str, body: dict):
    try:
        message = MessageSchema(
            subject=subject,
            recipients=[email_to],
            body='body',
            subtype='html',
        )
        fm = FastMail(conf)
        background_tasks.add_task(
            fm.send_message, message, template_name='invitation.html')
    except:
        raise Exception("Email Service Down")
