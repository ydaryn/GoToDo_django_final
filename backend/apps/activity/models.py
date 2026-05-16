from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
    PermissionsMixin,
    Project,
    Task,
    User,
)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here. Comment, Notification, ActivityLog


# ---------------------------------------------------------------------------
# Comment
# ---------------------------------------------------------------------------


class Comment(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("task"),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="comments",
        verbose_name=_("author"),
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
        verbose_name=_("parent comment"),
    )
    body = models.TextField(_("body"))
    edited = models.BooleanField(_("edited"), default=False)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["task", "created_at"]),
            models.Index(fields=["author"]),
        ]

    def __str__(self):
        return f"Comment by {self.author.username} on task #{self.task.id}"


# ---------------------------------------------------------------------------
# Notification
# ---------------------------------------------------------------------------


class Notification(models.Model):
    class Verb(models.TextChoices):
        ASSIGNED = "assigned", _("Assigned")
        COMMENTED = "commented", _("Commented")
        MENTIONED = "mentioned", _("Mentioned")
        STATUS_CHANGED = "status_changed", _("Status Changed")
        DUE_SOON = "due_soon", _("Due Soon")

    class EntityType(models.TextChoices):
        TASK = "task", _("Task")
        SUBTASK = "subtask", _("SubTask")
        COMMENT = "comment", _("Comment")
        PROJECT = "project", _("Project")
        SPRINT = "sprint", _("Sprint")

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name=_("recipient"),
    )
    actor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="triggered_notifications",
        verbose_name=_("actor"),
    )
    verb = models.CharField(_("verb"), max_length=32, choices=Verb.choices)
    entity_type = models.CharField(
        _("entity type"), max_length=16, choices=EntityType.choices
    )
    entity_id = models.PositiveIntegerField(_("entity id"))
    message = models.TextField(_("message"), blank=True)
    is_read = models.BooleanField(_("read"), default=False)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    class Meta:
        verbose_name = _("notification")
        verbose_name_plural = _("notifications")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["recipient", "is_read"]),
            models.Index(fields=["recipient", "-created_at"]),
            models.Index(fields=["entity_type", "entity_id"]),
        ]

    def __str__(self):
        return f"→ {self.recipient.username}: {self.verb} ({self.entity_type} #{self.entity_id})"


# ---------------------------------------------------------------------------
# ActivityLog
# ---------------------------------------------------------------------------


class ActivityLog(models.Model):
    class Action(models.TextChoices):
        CREATED = "created", _("Created")
        UPDATED = "updated", _("Updated")
        DELETED = "deleted", _("Deleted")
        STATUS_CHANGED = "status_changed", _("Status Changed")
        ASSIGNED = "assigned", _("Assigned")
        COMMENTED = "commented", _("Commented")

    class EntityType(models.TextChoices):
        TASK = "task", _("Task")
        SUBTASK = "subtask", _("SubTask")
        COMMENT = "comment", _("Comment")
        SPRINT = "sprint", _("Sprint")
        EPIC = "epic", _("Epic")
        PROJECT = "project", _("Project")

    actor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="activity_logs",
        verbose_name=_("actor"),
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="activity_logs",
        verbose_name=_("project"),
    )
    entity_type = models.CharField(
        _("entity type"), max_length=16, choices=EntityType.choices
    )
    entity_id = models.PositiveIntegerField(_("entity id"))
    action = models.CharField(_("action"), max_length=32, choices=Action.choices)
    old_value = models.JSONField(_("old value"), null=True, blank=True)
    new_value = models.JSONField(_("new value"), null=True, blank=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    class Meta:
        verbose_name = _("activity log")
        verbose_name_plural = _("activity logs")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["actor"]),
            models.Index(fields=["project", "-created_at"]),
            models.Index(fields=["entity_type", "entity_id"]),
        ]

    def __str__(self):
        actor = self.actor.username if self.actor else "system"
        return f"{actor} {self.action} {self.entity_type} #{self.entity_id}"
