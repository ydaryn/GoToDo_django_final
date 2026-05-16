from django.urls import path
from apps.activity.views import NotificationSSEView

urlpatterns = [
    path("notifications/stream/", NotificationSSEView.as_view()),
    
]