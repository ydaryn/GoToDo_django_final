from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin, User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
# Create your models here. Project, ProjectMember, Tag

# ---------------------------------------------------------------------------
# Project
# ---------------------------------------------------------------------------

class Project(models.Model):
    class Status(models.TextChoices):
        ACTIVE    = "active",    _("Active")
        ARCHIVED  = "archived",  _("Archived")
        COMPLETED = "completed", _("Completed")

    name        = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"), blank=True)
    owner       = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="owned_projects",
        verbose_name=_("owner"),
    )
    status      = models.CharField(
        _("status"), max_length=16,
        choices=Status.choices, default=Status.ACTIVE,
    )
    created_at  = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at  = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        verbose_name        = _("project")
        verbose_name_plural = _("projects")
        ordering            = ["-created_at"]
        indexes             = [
            models.Index(fields=["owner", "status"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------
# ProjectMember
# ---------------------------------------------------------------------------

class ProjectMember(models.Model):
    class Role(models.TextChoices):
        OWNER  = "owner",  _("Owner")
        ADMIN  = "admin",  _("Admin")
        MEMBER = "member", _("Member")
        VIEWER = "viewer", _("Viewer")

    project   = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="members",
        verbose_name=_("project"),
    )
    user      = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="project_memberships",
        verbose_name=_("user"),
    )
    role      = models.CharField(
        _("role"), max_length=16,
        choices=Role.choices, default=Role.MEMBER,
    )
    joined_at = models.DateTimeField(_("joined at"), auto_now_add=True)

    class Meta:
        verbose_name        = _("project member")
        verbose_name_plural = _("project members")
        ordering            = ["project", "role"]
        unique_together     = [("project", "user")]
        indexes             = [
            models.Index(fields=["project", "user"]),
            models.Index(fields=["project", "role"]),
        ]

    def __str__(self):
        return f"{self.user.username} — {self.project.name} ({self.role})"

# ---------------------------------------------------------------------------
# Tag
# ---------------------------------------------------------------------------

class Tag(models.Model):
    project    = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tags",
        verbose_name=_("project"),
    )
    name       = models.CharField(_("name"), max_length=64)
    color      = models.CharField(_("color"), max_length=7, default="#6366f1")
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    class Meta:
        verbose_name        = _("tag")
        verbose_name_plural = _("tags")
        ordering            = ["name"]
        unique_together     = [("project", "name")]
        indexes             = [
            models.Index(fields=["project", "name"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.project.name})"
