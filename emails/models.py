from django.db import models


class IncomingEmail(models.Model):
    message_id = models.CharField(max_length=500, unique=True)  # message-id header
    from_email = models.CharField(max_length=254)
    subject = models.CharField(max_length=500, blank=True)
    body = models.TextField(blank=True)
    received_at = models.DateTimeField(auto_now_add=True)
    reply_scheduled = models.BooleanField(default=False)
    replied = models.BooleanField(default=False)
    reply_sent_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.from_email} - {self.subject[:40]}"
