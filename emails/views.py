from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Message
from .tasks import reply_email_task

class MessageCreateAPI(APIView):
    def post(self, request):
        email = request.data.get("email")
        subject = request.data.get("subject", "No Subject")
        body = request.data.get("body", "")

        msg = Message.objects.create(email=email, subject=subject, body=body)

        # Schedule email after 25 minutes (1500 sec)
        reply_email_task.apply_async(args=[msg.id], countdown=1500)

        return Response({"message": "Received. Auto reply will be sent after 25 min."})
