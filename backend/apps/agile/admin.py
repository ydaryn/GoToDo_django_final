from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.agile.models import Epic, Sprint, Task, SubTask
from apps.projects.models import Tag


@admin.register(Epic)
class EpicAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "project",
        "owner",
        "status",
        "start_date",
        "end_date",
        "created_at",
    )
    list_filter = ("status", "project")
    search_fields = (
        "title",
        "description",
        "project__name",
        "owner__email",
    )
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(Sprint)
class SprintAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "project",
        "status",
        "start_date",
        "end_date",
        "created_at",
    )
    list_filter = ("status", "project")
    search_fields = ("name", "goal", "project__name")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "project",
        "color",
        "created_at",
    )
    list_filter = ("project",)
    search_fields = ("name", "project__name")
    ordering = ("name",)
    readonly_fields = ("created_at",)


class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 0
    fields = (
        "title",
        "assignee",
        "status",
        "due_date",
        "order",
    )
    readonly_fields = ("created_at",)
    ordering = ("order",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "project",
        "assignee",
        "reporter",
        "status",
        "priority",
        "sprint",
        "epic",
        "due_date",
        "created_at",
    )
    list_filter = (
        "status",
        "priority",
        "project",
        "sprint",
        "epic",
    )
    search_fields = (
        "title",
        "description",
        "project__name",
        "assignee__email",
        "reporter__email",
    )
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    filter_horizontal = ("tags",)
    inlines = [SubTaskInline]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "project",
                    "title",
                    "description",
                )
            },
        ),
        (
            _("Assignment"),
            {
                "fields": (
                    "assignee",
                    "reporter",
                    "status",
                    "priority",
                    "story_points",
                    "tags",
                )
            },
        ),
        (
            _("Relations"),
            {
                "fields": (
                    "sprint",
                    "epic",
                )
            },
        ),
        (
            _("Dates"),
            {
                "fields": (
                    "due_date",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "task",
        "assignee",
        "status",
        "due_date",
        "order",
        "created_at",
    )
    list_filter = ("status",)
    search_fields = (
        "title",
        "description",
        "task__title",
        "assignee__email",
    )
    ordering = ("order", "created_at")
    readonly_fields = ("created_at", "updated_at")