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
# Project
# ---------------------------------------------------------------------------

class ProjectMemberInline(admin.TabularInline):
    model       = ProjectMember
    extra       = 0
    fields      = ("user", "role", "joined_at")
    readonly_fields = ("joined_at",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display  = ("name", "owner", "status", "created_at", "updated_at")
    list_filter   = ("status",)
    search_fields = ("name", "description", "owner__username", "owner__email")
    ordering      = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    inlines       = [ProjectMemberInline]

    fieldsets = (
        (None,         {"fields": ("name", "description", "owner", "status")}),
        (_("Dates"),   {"fields": ("created_at", "updated_at")}),
    )


# ---------------------------------------------------------------------------
# ProjectMember
# ---------------------------------------------------------------------------

@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    list_display  = ("user", "project", "role", "joined_at")
    list_filter   = ("role",)
    search_fields = ("user__username", "user__email", "project__name")
    ordering      = ("project", "role")
    readonly_fields = ("joined_at",)



# ---------------------------------------------------------------------------
# Tag
# ---------------------------------------------------------------------------

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display  = ("name", "project", "color", "created_at")
    list_filter   = ("project",)
    search_fields = ("name", "project__name")
    ordering      = ("name",)
    readonly_fields = ("created_at",)

