from fastapi import APIRouter, BackgroundTasks

from app.services.mail import send_email_async
from app.services.mail import send_email_background


mail_router = APIRouter(prefix='/send-email', tags=['Send Mail'])


@mail_router.get('/send-email/asynchronous')
async def send_email_asynchronous():
  await send_email_async(
      subject='Invitation to Join Our Company X',
      email_to='amirul@gmail.com',
      body={"title": "Invitation", "name": "Dear Mr. X", "invitation_url": ''}
    )
  return 'Success'


@mail_router.get('/backgroundtasks')
def send_email_backgroundtasks(background_tasks: BackgroundTasks):
  send_email_background(
      background_tasks=background_tasks,
      subject='Invitation to Join Our Company X',
      email_to='amirul@gmail.com',
      body={"title": "Invitation", "name": "Dear Mr. X"}
    )
  return 'Success'