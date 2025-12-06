from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage
from imapclient import IMAPClient
import email
from .models import IncomingEmail
from django.utils import timezone
import time

IMAP_HOST = settings.IMAP_HOST
IMAP_PORT = int(getattr(settings, "IMAP_PORT", 993))
IMAP_USER = settings.IMAP_USER
IMAP_PASSWORD = settings.IMAP_PASSWORD
IMAP_FOLDER = getattr(settings, "IMAP_FOLDER", "INBOX")


def parse_email_message(raw_bytes):
    """Return message_id, from_email, subject, plain_text_body"""
    msg = email.message_from_bytes(raw_bytes)
    message_id = msg.get("Message-ID") or msg.get("Message-Id") or ""
    subject = msg.get("Subject", "")
    from_email = email.utils.parseaddr(msg.get("From", ""))[1]
    # Extract the plain text body
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            disp = str(part.get("Content-Disposition") or "")
            if ctype == "text/plain" and "attachment" not in disp:
                charset = part.get_content_charset() or "utf-8"
                try:
                    body = part.get_payload(decode=True).decode(charset, errors="replace")
                except Exception:
                    body = part.get_payload(decode=True).decode("utf-8", errors="replace")
                break
    else:
        charset = msg.get_content_charset() or "utf-8"
        body = msg.get_payload(decode=True).decode(charset, errors="replace")
    return message_id.strip(), from_email, subject, body


@shared_task
def check_inbox_and_schedule_replies():
    """
    Poll IMAP, create IncomingEmail records for unseen messages,
    and schedule a send_autoreply task with countdown=25min for each new message.
    """
    try:
        with IMAPClient(IMAP_HOST, port=IMAP_PORT, use_uid=True, ssl=True) as client:
            client.login(IMAP_USER, IMAP_PASSWORD)
            client.select_folder(IMAP_FOLDER)
            # Search for unseen messages
            messages = client.search(["UNSEEN"])
            if not messages:
                return "no new messages"

            # fetch RFC822 raw
            response = client.fetch(messages, ["RFC822"])
            for uid, data in response.items():
                raw = data.get(b"RFC822")
                if not raw:
                    continue
                message_id, from_email, subject, body = parse_email_message(raw)
                if not message_id:
                    # fallback: combine uid + from + subject to avoid duplicates
                    message_id = f"<imap-uid-{uid}>"

                # Avoid duplication using message_id
                obj, created = IncomingEmail.objects.get_or_create(
                    message_id=message_id,
                    defaults={"from_email": from_email, "subject": subject, "body": body},
                )
                if created:
                    # schedule reply in 25 minutes (1500 seconds)
                    send_autoreply.apply_async(args=[obj.id], countdown=25 * 60)
                    obj.reply_scheduled = True
                    obj.save(update_fields=["reply_scheduled"])
                # optionally mark message as seen
                client.add_flags(uid, [b"\\Seen"])
        return "done"
    except Exception as e:
        return f"error: {e}"


@shared_task
def send_autoreply(incoming_email_id):
    """
    Compose and send the auto-reply. Mark the IncomingEmail as replied when sent.
    """
    from .models import IncomingEmail  # local import to avoid startup issues
    try:
        obj = IncomingEmail.objects.get(id=incoming_email_id)
    except IncomingEmail.DoesNotExist:
        return "no such email"

    # If already replied, do nothing
    if obj.replied:
        return "already replied"

    # Compose reply
    to_addr = obj.from_email
    subject = f"Re: {obj.subject or ''}".strip()
    # Your reply message (customize)
    body = (
        "Hello,\n\n"
        "Thank you for your email. This is an automatic response to confirm we received your message. "
        "A team member will review it and get back to you shortly.\n\n"
        "Best regards,\n"
        "Your Company"
    )

    email_msg = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_addr],
        headers={"In-Reply-To": obj.message_id or ""}
    )

    try:
        email_msg.send(fail_silently=False)
        obj.replied = True
        obj.reply_sent_at = timezone.now()
        obj.save(update_fields=["replied", "reply_sent_at"])
        return "sent"
    except Exception as e:
        # Optionally log the error; do not set replied = True
        return f"failed: {e}"
