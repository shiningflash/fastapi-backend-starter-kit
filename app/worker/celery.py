import os
import asyncio

from celery import Celery

from app.services.mail import send_email_async


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")


@celery.task(name="send_email_task")
def send_email_task(subject, email_to, body):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_email_async(subject, email_to, body))
    return True
