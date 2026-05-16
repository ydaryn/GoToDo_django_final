from django.contrib import admin
from .models import ActivityLog, Comment, Notification

# ---------------------------------------------------------------------------
# Comment
# ---------------------------------------------------------------------------


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("__str__", "task", "author", "edited", "created_at")
    list_filter = ("edited",)
    search_fields = ("body", "author__email", "task__title")
    ordering = ("created_at",)
    readonly_fields = ("created_at", "updated_at")


# ---------------------------------------------------------------------------
# Notification
# ---------------------------------------------------------------------------


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "recipient",
        "actor",
        "verb",
        "entity_type",
        "entity_id",
        "is_read",
        "created_at",
    )
    list_filter = ("verb", "entity_type", "is_read")
    search_fields = ("recipient__email", "actor__email", "message")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)


# ---------------------------------------------------------------------------
# ActivityLog
# ---------------------------------------------------------------------------


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = (
        "actor",
        "project",
        "action",
        "entity_type",
        "entity_id",
        "created_at",
    )
    list_filter = ("action", "entity_type", "project")
    search_fields = ("actor__email", "project__name")
    ordering = ("-created_at",)
    readonly_fields = (
        "actor",
        "project",
        "entity_type",
        "entity_id",
        "action",
        "old_value",
        "new_value",
        "created_at",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
