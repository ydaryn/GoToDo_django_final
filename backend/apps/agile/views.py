from typing import Any

from django.db.models import Count, QuerySet
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
    update=extend_schema(
        summary="Update epic",
        description="Fully updates epic data. Requires JWT authentication.",
        request=EpicWriteSerializer,
        responses={200: EpicReadSerializer, 400: None, 401: None, 404: None},
    ),
    partial_update=extend_schema(
        summary="Partially update epic",
        description="Partially updates epic data. Requires JWT authentication.",
        request=EpicWriteSerializer,
        responses={200: EpicReadSerializer, 400: None, 401: None, 404: None},
    ),
    destroy=extend_schema(
        summary="Delete epic",
        description="Deletes selected epic. Requires JWT authentication.",
        responses={204: None, 401: None, 404: None},
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
        return (
            Epic.objects.select_related(
                "project",
                "owner",
            )
            .annotate(
                tasks_count=Count("tasks", distinct=True),
            )
            .order_by("-created_at")
        )

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
    update=extend_schema(
        summary="Update sprint",
        description="Fully updates sprint data. Requires JWT authentication.",
        request=SprintWriteSerializer,
        responses={200: SprintReadSerializer, 400: None, 401: None, 404: None},
    ),
    partial_update=extend_schema(
        summary="Partially update sprint",
        description="Partially updates sprint data. Requires JWT authentication.",
        request=SprintWriteSerializer,
        responses={200: SprintReadSerializer, 400: None, 401: None, 404: None},
    ),
    destroy=extend_schema(
        summary="Delete sprint",
        description="Deletes selected sprint. Requires JWT authentication.",
        responses={204: None, 401: None, 404: None},
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
        return (
            Sprint.objects.select_related(
                "project",
            )
            .annotate(
                tasks_count=Count("tasks", distinct=True),
            )
            .order_by("-created_at")
        )

    def get_serializer_class(self) -> Any:
        if self.action in ["list", "retrieve"]:
            return SprintReadSerializer
        return SprintWriteSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Get tasks list",
        description=(
            "Returns a list of tasks. Supports filtering by project, sprint, epic, "
            "assignee, reporter, status and priority. Supports search by title and "
            "description. Requires JWT authentication."
        ),
        responses={200: TaskReadSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Get task details",
        description=(
            "Returns detailed task information with related project, sprint, epic, "
            "assignee, reporter, tags and annotated subtasks count."
        ),
        responses={200: TaskReadSerializer, 401: None, 404: None},
    ),
    create=extend_schema(
        summary="Create task",
        description="Creates a new task. Requires JWT authentication.",
        request=TaskWriteSerializer,
        responses={201: TaskReadSerializer, 400: None, 401: None},
    ),
    update=extend_schema(
        summary="Update task",
        description="Fully updates task data. Requires JWT authentication.",
        request=TaskWriteSerializer,
        responses={200: TaskReadSerializer, 400: None, 401: None, 404: None},
    ),
    partial_update=extend_schema(
        summary="Partially update task",
        description="Partially updates task data. Requires JWT authentication.",
        request=TaskWriteSerializer,
        responses={200: TaskReadSerializer, 400: None, 401: None, 404: None},
    ),
    destroy=extend_schema(
        summary="Delete task",
        description="Deletes selected task. Requires JWT authentication.",
        responses={204: None, 401: None, 404: None},
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
        "subtasks_count",
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
            .prefetch_related(
                "tags",
                "subtasks",
            )
            .annotate(
                subtasks_count=Count("subtasks", distinct=True),
            )
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
            "Returns a list of subtasks. Supports filtering by task, assignee, status "
            "and due date. Supports search by title and description. Requires JWT authentication."
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
    update=extend_schema(
        summary="Update subtask",
        description="Fully updates subtask data. Requires JWT authentication.",
        request=SubTaskWriteSerializer,
        responses={200: SubTaskReadSerializer, 400: None, 401: None, 404: None},
    ),
    partial_update=extend_schema(
        summary="Partially update subtask",
        description="Partially updates subtask data. Requires JWT authentication.",
        request=SubTaskWriteSerializer,
        responses={200: SubTaskReadSerializer, 400: None, 401: None, 404: None},
    ),
    destroy=extend_schema(
        summary="Delete subtask",
        description="Deletes selected subtask. Requires JWT authentication.",
        responses={204: None, 401: None, 404: None},
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
        return (
            SubTask.objects.select_related(
                "task",
                "task__project",
                "assignee",
            )
            .order_by("order", "created_at")
        )

    def get_serializer_class(self) -> Any:
        if self.action in ["list", "retrieve"]:
            return SubTaskReadSerializer
        return SubTaskWriteSerializer