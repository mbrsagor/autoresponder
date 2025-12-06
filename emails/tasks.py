from celery import shared_task
from django.core.mail import EmailMessage
from .models import Message


@shared_task
def reply_email_task(msg_id):
    msg = Message.objects.get(id=msg_id)
    if msg.replied:
        return "Already replied"

    email = EmailMessage(
        subject=f"Re: {msg.subject}",
        body="Thank you for contacting us. We will get back to you soon!",
        to=[msg.email]
    )
    email.send()

    msg.replied = True
    msg.save()
    return "Reply sent"
