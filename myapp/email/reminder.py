from flask_mail import Message
from myapp import mail
from flask import current_app

def send_reminder_email(to, subject, body):
    with current_app.app_context():
        msg = Message(subject, recipients=[to], body=body)
        mail.send(msg)
