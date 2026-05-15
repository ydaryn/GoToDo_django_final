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
# User
# ---------------------------------------------------------------------------

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display  = ("username", "email", "full_name", "is_active", "is_staff", "date_joined")
    list_filter   = ("is_active", "is_staff", "is_superuser")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering      = ("-date_joined",)
    readonly_fields = ("date_joined", "last_login")

    fieldsets = (
        (None,           {"fields": ("email", "username", "password")}),
        (_("Personal"),  {"fields": ("first_name", "last_name", "avatar", "bio")}),
        (_("Permissions"), {
            "fields": (
                "is_active", "is_staff", "is_superuser",
                "groups", "user_permissions",
            )
        }),
        (_("Dates"), {"fields": ("date_joined", "last_login")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "password1", "password2"),
        }),
    )

