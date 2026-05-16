from rest_framework import serializers

from apps.agile.models import Epic, Sprint, SubTask, Task
from apps.projects.models import Tag
from apps.agile.tasks import send_task_created_notification

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            "id",
            "name",
            "color",
        )


# ---------------------------------------------------------------------------
# Epic serializers
# ---------------------------------------------------------------------------


class EpicReadSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source="project.name", read_only=True)
    owner_email = serializers.EmailField(source="owner.email", read_only=True)
    tasks_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Epic
        fields = (
            "id",
            "project",
            "project_name",
            "owner",
            "owner_email",
            "title",
            "description",
            "status",
            "start_date",
            "end_date",
            "tasks_count",
            "created_at",
            "updated_at",
        )


class EpicWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Epic
        fields = (
            "project",
            "owner",
            "title",
            "description",
            "status",
            "start_date",
            "end_date",
        )


# ---------------------------------------------------------------------------
# Sprint serializers
# ---------------------------------------------------------------------------


class SprintReadSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source="project.name", read_only=True)
    tasks_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Sprint
        fields = (
            "id",
            "project",
            "project_name",
            "name",
            "goal",
            "status",
            "start_date",
            "end_date",
            "tasks_count",
            "created_at",
            "updated_at",
        )


class SprintWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = (
            "project",
            "name",
            "goal",
            "status",
            "start_date",
            "end_date",
        )


# ---------------------------------------------------------------------------
# Task serializers
# ---------------------------------------------------------------------------


class TaskReadSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source="project.name", read_only=True)
    sprint_name = serializers.CharField(source="sprint.name", read_only=True)
    epic_title = serializers.CharField(source="epic.title", read_only=True)
    assignee_email = serializers.EmailField(source="assignee.email", read_only=True)
    reporter_email = serializers.EmailField(source="reporter.email", read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    subtasks_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Task
        fields = (
            "id",
            "project",
            "project_name",
            "sprint",
            "sprint_name",
            "epic",
            "epic_title",
            "title",
            "description",
            "assignee",
            "assignee_email",
            "reporter",
            "reporter_email",
            "status",
            "priority",
            "story_points",
            "tags",
            "subtasks_count",
            "due_date",
            "created_at",
            "updated_at",
        )


class TaskWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            "project",
            "sprint",
            "epic",
            "title",
            "description",
            "assignee",
            "reporter",
            "status",
            "priority",
            "story_points",
            "tags",
            "due_date",
        )


# ---------------------------------------------------------------------------
# SubTask serializers
# ---------------------------------------------------------------------------


class SubTaskReadSerializer(serializers.ModelSerializer):
    task_title = serializers.CharField(source="task.title", read_only=True)
    assignee_email = serializers.EmailField(source="assignee.email", read_only=True)

    class Meta:
        model = SubTask
        fields = (
            "id",
            "task",
            "task_title",
            "title",
            "description",
            "assignee",
            "assignee_email",
            "status",
            "due_date",
            "order",
            "created_at",
            "updated_at",
        )


class SubTaskWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = (
            "task",
            "title",
            "description",
            "assignee",
            "status",
            "due_date",
            "order",
        )

def create(self, validated_data):
    task = Task.objects.create(**validated_data)
    send_task_created_notification.delay(task.id)
    return task