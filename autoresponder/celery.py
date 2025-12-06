import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "autoresponder.settings")

app = Celery("autoresponder")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# Optional: schedule the inbox checker every 1 minute
from celery.schedules import crontab
app.conf.beat_schedule = {
    # runs every minute
    "check-inbox-every-minute": {
        "task": "emails.tasks.check_inbox_and_schedule_replies",
        "schedule": 60.0,
    },
}
