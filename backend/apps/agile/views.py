# apps/agile/views.py
from typing import Any
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Epic, Sprint, Task, SubTask
from .serializers import (
    EpicReadSerializer, EpicWriteSerializer,
    SprintReadSerializer, SprintWriteSerializer,
    TaskReadSerializer, TaskWriteSerializer,
    SubTaskReadSerializer, SubTaskWriteSerializer
)

@extend_schema_view(
    list=extend_schema(summary="Получить список эпиков", responses={200: EpicReadSerializer(many=True)}),
    create=extend_schema(summary="Создать эпик", responses={201: EpicReadSerializer})
)
class EpicViewSet(viewsets.ModelViewSet):
    queryset = Epic.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self) -> Any:
        return EpicReadSerializer if self.action in ['list', 'retrieve'] else EpicWriteSerializer


@extend_schema_view(
    list=extend_schema(summary="Получить список спринтов", responses={200: SprintReadSerializer(many=True)}),
    create=extend_schema(summary="Создать спринт", responses={201: SprintReadSerializer})
)
class SprintViewSet(viewsets.ModelViewSet):
    queryset = Sprint.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self) -> Any:
        return SprintReadSerializer if self.action in ['list', 'retrieve'] else SprintWriteSerializer


@extend_schema_view(
    list=extend_schema(summary="Получить список задач (Тасок)", responses={200: TaskReadSerializer(many=True)}),
    create=extend_schema(summary="Создать задачу", responses={201: TaskReadSerializer})
)
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self) -> Any:
        return TaskReadSerializer if self.action in ['list', 'retrieve'] else TaskWriteSerializer


@extend_schema_view(
    list=extend_schema(summary="Получить список подзадач", responses={200: SubTaskReadSerializer(many=True)}),
    create=extend_schema(summary="Создать подзадачу", responses={201: SubTaskReadSerializer})
)
class SubTaskViewSet(viewsets.ModelViewSet):
    queryset = SubTask.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self) -> Any:
        return SubTaskReadSerializer if self.action in ['list', 'retrieve'] else SubTaskWriteSerializer