from typing import Any

from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.agile.models import Tag
from apps.projects.models import Project, ProjectMember

User = get_user_model()


class UserMinifiedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "full_name",
            "role",
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            "id",
            "name",
            "color",
        )


class ProjectListSerializer(serializers.ModelSerializer):
    owner = UserMinifiedSerializer(read_only=True)
    members_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Project
        fields = (
            "id",
            "name",
            "description",
            "owner",
            "status",
            "members_count",
            "created_at",
            "updated_at",
        )


class ProjectDetailSerializer(serializers.ModelSerializer):
    owner = UserMinifiedSerializer(read_only=True)
    members_count = serializers.IntegerField(read_only=True)
    tasks_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Project
        fields = (
            "id",
            "name",
            "description",
            "owner",
            "status",
            "members_count",
            "tasks_count",
            "created_at",
            "updated_at",
        )


class ProjectWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = (
            "name",
            "description",
            "status",
        )

    def create(self, validated_data: dict[str, Any]) -> Project:
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["owner"] = request.user
        return super().create(validated_data)


class ProjectMemberSerializer(serializers.ModelSerializer):
    user = UserMinifiedSerializer(read_only=True)

    class Meta:
        model = ProjectMember
        fields = (
            "id",
            "project",
            "user",
            "role",
            "joined_at",
        )
