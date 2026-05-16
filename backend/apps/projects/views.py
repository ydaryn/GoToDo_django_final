from typing import Any

from django.db.models import Count, QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from apps.projects.models import Project, ProjectMember
from apps.projects.serializers import (
    ProjectDetailSerializer,
    ProjectListSerializer,
    ProjectMemberSerializer,
    ProjectWriteSerializer,
)


@extend_schema_view(
    list=extend_schema(
        summary="Get projects list",
        description=(
            "Returns a list of projects. Supports filtering by status and owner, "
            "searching by name and description, and ordering by creation date. "
            "Requires JWT authentication."
        ),
        responses={200: ProjectListSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Get project details",
        description=(
            "Returns detailed project information with owner, members count "
            "and tasks count. Requires JWT authentication."
        ),
        responses={200: ProjectDetailSerializer, 401: None, 404: None},
    ),
    create=extend_schema(
        summary="Create project",
        description=(
            "Creates a new project. Current authenticated user becomes project owner. "
            "Requires JWT authentication."
        ),
        request=ProjectWriteSerializer,
        responses={201: ProjectDetailSerializer, 400: None, 401: None},
    ),
    update=extend_schema(
        summary="Update project",
        description="Fully updates project data. Requires JWT authentication.",
        request=ProjectWriteSerializer,
        responses={200: ProjectDetailSerializer, 400: None, 401: None, 404: None},
    ),
    partial_update=extend_schema(
        summary="Partially update project",
        description="Partially updates project data. Requires JWT authentication.",
        request=ProjectWriteSerializer,
        responses={200: ProjectDetailSerializer, 400: None, 401: None, 404: None},
    ),
    destroy=extend_schema(
        summary="Delete project",
        description="Deletes selected project. Requires JWT authentication.",
        responses={204: None, 401: None, 404: None},
    ),
)
class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status", "owner"]
    search_fields = ["name", "description", "owner__email"]
    ordering_fields = ["created_at", "updated_at", "status", "name"]
    ordering = ["-created_at"]

    def get_queryset(self) -> QuerySet[Project]:
        return (
            Project.objects.select_related("owner")
            .annotate(
                members_count=Count("members", distinct=True),
                tasks_count=Count("tasks", distinct=True),
            )
            .order_by("-created_at")
        )

    def get_serializer_class(self) -> Any:
        if self.action == "list":
            return ProjectListSerializer
        if self.action == "retrieve":
            return ProjectDetailSerializer
        return ProjectWriteSerializer

    def perform_create(self, serializer: ProjectWriteSerializer) -> None:
        project = serializer.save(owner=self.request.user)
        ProjectMember.objects.get_or_create(
            project=project,
            user=self.request.user,
            defaults={"role": ProjectMember.Role.OWNER},
        )


@extend_schema_view(
    list=extend_schema(
        summary="Get project members list",
        description="Returns project members list. Requires JWT authentication.",
        responses={200: ProjectMemberSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Get project member details",
        description="Returns selected project member details.",
        responses={200: ProjectMemberSerializer, 401: None, 404: None},
    ),
)
class ProjectMemberViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProjectMemberSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["project", "user", "role"]
    search_fields = ["project__name", "user__email"]
    ordering_fields = ["joined_at", "role"]
    ordering = ["-joined_at"]

    def get_queryset(self) -> QuerySet[ProjectMember]:
        return ProjectMember.objects.select_related("project", "user").order_by(
            "-joined_at"
        )