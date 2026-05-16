from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.projects.models import Project, ProjectMember


class ProjectMemberInline(admin.TabularInline):
    model = ProjectMember
    extra = 0
    fields = ("user", "role", "joined_at")
    readonly_fields = ("joined_at",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "status", "created_at", "updated_at")
    list_filter = ("status",)
    search_fields = ("name", "description", "owner__username", "owner__email")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    inlines = [ProjectMemberInline]

    fieldsets = (
        (None, {"fields": ("name", "description", "owner", "status")}),
        (_("Dates"), {"fields": ("created_at", "updated_at")}),
    )


@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ("user", "project", "role", "joined_at")
    list_filter = ("role",)
    search_fields = ("user__username", "user__email", "project__name")
    ordering = ("project", "role")
    readonly_fields = ("joined_at",)