# apps/agile/urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from apps.agile.async_views import AsyncExternalAPIView

from .views import EpicViewSet, SprintViewSet, SubTaskViewSet, TaskViewSet

router: DefaultRouter = DefaultRouter()
router.register(r"epics", EpicViewSet, basename="epic")
router.register(r"sprints", SprintViewSet, basename="sprint")
router.register(r"tasks", TaskViewSet, basename="task")
router.register(r"subtasks", SubTaskViewSet, basename="subtask")

urlpatterns = [
    path("", include(router.urls)),
    path("async-external/", AsyncExternalAPIView.as_view()),
]
