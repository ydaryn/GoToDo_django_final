from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import (
    User,
    Project,
    ProjectMember,
    Epic,
    Sprint,
    Tag,
    Task,
    SubTask,
    Comment,
    Notification,
    ActivityLog,
)



# ---------------------------------------------------------------------------
# Epic
# ---------------------------------------------------------------------------

@admin.register(Epic)
class EpicAdmin(admin.ModelAdmin):
    list_display  = ("title", "project", "owner", "status", "start_date", "end_date", "created_at")
    list_filter   = ("status", "project")
    search_fields = ("title", "description", "project__name", "owner__username")
    ordering      = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (None,       {"fields": ("project", "owner", "title", "description", "status")}),
        (_("Dates"), {"fields": ("start_date", "end_date", "created_at", "updated_at")}),
    )


# ---------------------------------------------------------------------------
# Sprint
# ---------------------------------------------------------------------------

@admin.register(Sprint)
class SprintAdmin(admin.ModelAdmin):
    list_display  = ("name", "project", "status", "start_date", "end_date", "created_at")
    list_filter   = ("status", "project")
    search_fields = ("name", "goal", "project__name")
    ordering      = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (None,       {"fields": ("project", "name", "goal", "status")}),
        (_("Dates"), {"fields": ("start_date", "end_date", "created_at", "updated_at")}),
    )


# ---------------------------------------------------------------------------
# Task
# ---------------------------------------------------------------------------

class SubTaskInline(admin.TabularInline):
    model  = SubTask
    extra  = 0
    fields = ("title", "assignee", "status", "due_date", "order")
    readonly_fields = ("created_at",)
    ordering = ("order",)


class CommentInline(admin.StackedInline):
    model   = Comment
    extra   = 0
    fields  = ("author", "parent", "body", "edited", "created_at")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display  = (
        "title", "project", "assignee", "reporter",
        "status", "priority", "sprint", "epic", "due_date", "created_at",
    )
    list_filter   = ("status", "priority", "project", "sprint", "epic")
    search_fields = (
        "title", "description",
        "project__name",
        "assignee__username", "assignee__email",
        "reporter__username",
    )
    ordering      = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    filter_horizontal = ("tags",)
    inlines       = [SubTaskInline, CommentInline]

    fieldsets = (
        (None,            {"fields": ("project", "title", "description")}),
        (_("Assignment"), {"fields": ("assignee", "reporter", "status", "priority", "story_points", "tags")}),
        (_("Relations"),  {"fields": ("sprint", "epic")}),
        (_("Dates"),      {"fields": ("due_date", "created_at", "updated_at")}),
    )


# ---------------------------------------------------------------------------
# SubTask
# ---------------------------------------------------------------------------

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display  = ("title", "task", "assignee", "status", "due_date", "order", "created_at")
    list_filter   = ("status",)
    search_fields = ("title", "description", "task__title", "assignee__username")
    ordering      = ("order", "created_at")
    readonly_fields = ("created_at", "updated_at")
