from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.projects.views import ProjectMemberViewSet, ProjectViewSet

router = DefaultRouter()
router.register("members", ProjectMemberViewSet, basename="project-member")
router.register("", ProjectViewSet, basename="project")

app_name = "projects"

urlpatterns = [
    path("", include(router.urls)),
]