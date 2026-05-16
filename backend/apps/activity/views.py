import json
import time

from django.http import StreamingHttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from apps.activity.models import Notification

class NotificationSSEView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = request.user

        def event_stream():
            last_id = 0

            while True:
                notifications = Notification.objects.filter(
                    recipient=user,
                    id__gt=last_id,
                    is_read=False,
                ).order_by("id")

                for notification in notifications:
                    last_id = notification.id

                    data = {
                        "id": notification.id,
                        "message": notification.message,
                        "created_at": notification.created_at.isoformat(),
                    }

                    yield f"data: {json.dumps(data)}\n\n"
                time.sleep(3)
        
        response = StreamingHttpResponse(event_stream(), content_type="text/event-stream",)
        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no'
        return response