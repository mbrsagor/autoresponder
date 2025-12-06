from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import IncomingEmail
from .tasks import send_autoreply


@csrf_exempt
def incoming_webhook(request):
    payload = request.POST or json.loads(request.body.decode("utf-8") or "{}")
    from_email = payload.get("from")
    subject = payload.get("subject")
    body = payload.get("body-plain") or payload.get("text")
    message_id = payload.get("Message-Id") or payload.get("message-id") or payload.get("Message-ID")
    if not message_id:
        message_id = f"webhook-{int(time.time()*1000)}"
    obj, created = IncomingEmail.objects.get_or_create(
        message_id=message_id, defaults={"from_email": from_email, "subject": subject, "body": body}
    )

    if created:
        send_autoreply.apply_async(args=[obj.id], countdown=25*60)
    return JsonResponse({"ok": True})
