from typing import Any

from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from apps.agile.models import Epic, Sprint, SubTask, Task
from apps.agile.serializers import (
    EpicReadSerializer,
    EpicWriteSerializer,
    SprintReadSerializer,
    SprintWriteSerializer,
    SubTaskReadSerializer,
    SubTaskWriteSerializer,
    TaskReadSerializer,
    TaskWriteSerializer,
)


@extend_schema_view(
    list=extend_schema(
        summary="Get epics list",
        description=(
            "Returns a list of epics. Supports filtering by project, owner and status. "
            "Supports search by title and description. Requires JWT authentication."
        ),
        responses={200: EpicReadSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Get epic details",
        description="Returns detailed information about a selected epic.",
        responses={200: EpicReadSerializer, 401: None, 404: None},
    ),
    create=extend_schema(
        summary="Create epic",
        description="Creates a new epic. Requires JWT authentication.",
        request=EpicWriteSerializer,
        responses={201: EpicReadSerializer, 400: None, 401: None},
    ),
)
class EpicViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["project", "owner", "status"]
    search_fields = ["title", "description", "project__name", "owner__email"]
    ordering_fields = ["created_at", "updated_at", "start_date", "end_date", "status"]
    ordering = ["-created_at"]

    def get_queryset(self) -> QuerySet[Epic]:
        return Epic.objects.select_related("project", "owner").order_by("-created_at")

    def get_serializer_class(self) -> Any:
        if self.action in ["list", "retrieve"]:
            return EpicReadSerializer
        return EpicWriteSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Get sprints list",
        description=(
            "Returns a list of sprints. Supports filtering by project and status. "
            "Supports search by name and goal. Requires JWT authentication."
        ),
        responses={200: SprintReadSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Get sprint details",
        description="Returns detailed information about a selected sprint.",
        responses={200: SprintReadSerializer, 401: None, 404: None},
    ),
    create=extend_schema(
        summary="Create sprint",
        description="Creates a new sprint. Requires JWT authentication.",
        request=SprintWriteSerializer,
        responses={201: SprintReadSerializer, 400: None, 401: None},
    ),
)
class SprintViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["project", "status"]
    search_fields = ["name", "goal", "project__name"]
    ordering_fields = ["created_at", "updated_at", "start_date", "end_date", "status"]
    ordering = ["-created_at"]

    def get_queryset(self) -> QuerySet[Sprint]:
        return Sprint.objects.select_related("project").order_by("-created_at")

    def get_serializer_class(self) -> Any:
        if self.action in ["list", "retrieve"]:
            return SprintReadSerializer
        return SprintWriteSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Get tasks list",
        description=(
            "Returns a list of tasks. Supports filtering by project, sprint, epic, assignee, "
            "reporter, status and priority. Supports search by title and description. "
            "Requires JWT authentication."
        ),
        responses={200: TaskReadSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Get task details",
        description="Returns detailed information about a selected task with related project, sprint, epic, assignee, reporter and tags.",
        responses={200: TaskReadSerializer, 401: None, 404: None},
    ),
    create=extend_schema(
        summary="Create task",
        description="Creates a new task. Requires JWT authentication.",
        request=TaskWriteSerializer,
        responses={201: TaskReadSerializer, 400: None, 401: None},
    ),
)
class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        "project",
        "sprint",
        "epic",
        "assignee",
        "reporter",
        "status",
        "priority",
        "due_date",
    ]
    search_fields = [
        "title",
        "description",
        "project__name",
        "sprint__name",
        "epic__title",
        "assignee__email",
        "reporter__email",
    ]
    ordering_fields = [
        "created_at",
        "updated_at",
        "due_date",
        "priority",
        "status",
        "story_points",
    ]
    ordering = ["-created_at"]

    def get_queryset(self) -> QuerySet[Task]:
        return (
            Task.objects.select_related(
                "project",
                "sprint",
                "epic",
                "assignee",
                "reporter",
            )
            .prefetch_related("tags")
            .order_by("-created_at")
        )

    def get_serializer_class(self) -> Any:
        if self.action in ["list", "retrieve"]:
            return TaskReadSerializer
        return TaskWriteSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Get subtasks list",
        description=(
            "Returns a list of subtasks. Supports filtering by task, assignee and status. "
            "Supports search by title and description. Requires JWT authentication."
        ),
        responses={200: SubTaskReadSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Get subtask details",
        description="Returns detailed information about a selected subtask.",
        responses={200: SubTaskReadSerializer, 401: None, 404: None},
    ),
    create=extend_schema(
        summary="Create subtask",
        description="Creates a new subtask. Requires JWT authentication.",
        request=SubTaskWriteSerializer,
        responses={201: SubTaskReadSerializer, 400: None, 401: None},
    ),
)
class SubTaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["task", "assignee", "status", "due_date"]
    search_fields = ["title", "description", "task__title", "assignee__email"]
    ordering_fields = ["created_at", "updated_at", "due_date", "order", "status"]
    ordering = ["order", "created_at"]

    def get_queryset(self) -> QuerySet[SubTask]:
        return SubTask.objects.select_related("task", "assignee").order_by(
            "order",
            "created_at",
        )

    def get_serializer_class(self) -> Any:
        if self.action in ["list", "retrieve"]:
            return SubTaskReadSerializer
        return SubTaskWriteSerializer