# apps/agile/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EpicViewSet, SprintViewSet, TaskViewSet, SubTaskViewSet

router: DefaultRouter = DefaultRouter()
router.register(r'epics', EpicViewSet, basename='epic')
router.register(r'sprints', SprintViewSet, basename='sprint')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'subtasks', SubTaskViewSet, basename='subtask')

urlpatterns = [
    path('', include(router.urls)),
]