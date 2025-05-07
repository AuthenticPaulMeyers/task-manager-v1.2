from celery_worker import celery
from myapp.email.reminder import send_reminder_email

@celery.task
def send_reminder(to, subject, body):
    send_reminder_email(to, subject, body)
