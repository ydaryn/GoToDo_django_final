from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin, User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from backend.apps.projects.models import Project, Tag
# Create your models here. Epic, Sprint, Task, Subtask

# ---------------------------------------------------------------------------
# Epic
# ---------------------------------------------------------------------------

class Epic(models.Model):
    class Status(models.TextChoices):
        OPEN        = "open",        _("Open")
        IN_PROGRESS = "in_progress", _("In Progress")
        CLOSED      = "closed",      _("Closed")

    project    = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="epics",
        verbose_name=_("project"),
    )
    owner      = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="owned_epics",
        verbose_name=_("owner"),
    )
    title      = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"), blank=True)
    status     = models.CharField(
        _("status"), max_length=16,
        choices=Status.choices, default=Status.OPEN,
    )
    start_date = models.DateField(_("start date"), null=True, blank=True)
    end_date   = models.DateField(_("end date"), null=True, blank=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        verbose_name        = _("epic")
        verbose_name_plural = _("epics")
        ordering            = ["-created_at"]
        indexes             = [
            models.Index(fields=["project", "status"]),
        ]
        constraints         = [
            models.CheckConstraint(
                check=models.Q(end_date__isnull=True)
                    | models.Q(start_date__isnull=True)
                    | models.Q(end_date__gte=models.F("start_date")),
                name="epic_end_date_gte_start_date",
            )
        ]

    def __str__(self):
        return f"[{self.project.name}] {self.title}"


# ---------------------------------------------------------------------------
# Sprint
# ---------------------------------------------------------------------------

class Sprint(models.Model):
    class Status(models.TextChoices):
        PLANNED   = "planned",   _("Planned")
        ACTIVE    = "active",    _("Active")
        COMPLETED = "completed", _("Completed")

    project    = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="sprints",
        verbose_name=_("project"),
    )
    name       = models.CharField(_("name"), max_length=255)
    goal       = models.TextField(_("goal"), blank=True)
    status     = models.CharField(
        _("status"), max_length=16,
        choices=Status.choices, default=Status.PLANNED,
    )
    start_date = models.DateField(_("start date"), null=True, blank=True)
    end_date   = models.DateField(_("end date"), null=True, blank=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        verbose_name        = _("sprint")
        verbose_name_plural = _("sprints")
        ordering            = ["-created_at"]
        indexes             = [
            models.Index(fields=["project", "status"]),
        ]
        constraints         = [
            models.CheckConstraint(
                check=models.Q(end_date__isnull=True)
                    | models.Q(start_date__isnull=True)
                    | models.Q(end_date__gte=models.F("start_date")),
                name="sprint_end_date_gte_start_date",
            )
        ]

    def __str__(self):
        return f"[{self.project.name}] {self.name}"





# ---------------------------------------------------------------------------
# Task
# ---------------------------------------------------------------------------

class Task(models.Model):
    class Status(models.TextChoices):
        TODO        = "todo",        _("To Do")
        IN_PROGRESS = "in_progress", _("In Progress")
        REVIEW      = "review",      _("Review")
        DONE        = "done",        _("Done")

    class Priority(models.TextChoices):
        LOW      = "low",      _("Low")
        MEDIUM   = "medium",   _("Medium")
        HIGH     = "high",     _("High")
        CRITICAL = "critical", _("Critical")

    project      = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks",
        verbose_name=_("project"),
    )
    sprint       = models.ForeignKey(
        Sprint,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="tasks",
        verbose_name=_("sprint"),
    )
    epic         = models.ForeignKey(
        Epic,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="tasks",
        verbose_name=_("epic"),
    )
    title        = models.CharField(_("title"), max_length=255)
    description  = models.TextField(_("description"), blank=True)
    assignee     = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="assigned_tasks",
        verbose_name=_("assignee"),
    )
    reporter     = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="reported_tasks",
        verbose_name=_("reporter"),
    )
    status       = models.CharField(
        _("status"), max_length=16,
        choices=Status.choices, default=Status.TODO,
    )
    priority     = models.CharField(
        _("priority"), max_length=16,
        choices=Priority.choices, default=Priority.MEDIUM,
    )
    story_points = models.PositiveSmallIntegerField(_("story points"), null=True, blank=True)
    tags         = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="tasks",
        verbose_name=_("tags"),
    )
    due_date     = models.DateField(_("due date"), null=True, blank=True)
    created_at   = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at   = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        verbose_name        = _("task")
        verbose_name_plural = _("tasks")
        ordering            = ["-created_at"]
        indexes             = [
            models.Index(fields=["project", "status"]),
            models.Index(fields=["project", "priority"]),
            models.Index(fields=["assignee", "status"]),
            models.Index(fields=["sprint"]),
            models.Index(fields=["epic"]),
        ]

    def __str__(self):
        return f"[{self.project.name}] {self.title}"


# ---------------------------------------------------------------------------
# SubTask
# ---------------------------------------------------------------------------

class SubTask(models.Model):
    class Status(models.TextChoices):
        TODO        = "todo",        _("To Do")
        IN_PROGRESS = "in_progress", _("In Progress")
        DONE        = "done",        _("Done")

    task        = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="subtasks",
        verbose_name=_("task"),
    )
    title       = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"), blank=True)
    assignee    = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="assigned_subtasks",
        verbose_name=_("assignee"),
    )
    status      = models.CharField(
        _("status"), max_length=16,
        choices=Status.choices, default=Status.TODO,
    )
    due_date    = models.DateField(_("due date"), null=True, blank=True)
    order       = models.PositiveIntegerField(_("order"), default=0)
    created_at  = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at  = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        verbose_name        = _("subtask")
        verbose_name_plural = _("subtasks")
        ordering            = ["order", "created_at"]
        indexes             = [
            models.Index(fields=["task", "status"]),
        ]

    def __str__(self):
        return f"{self.task.title} → {self.title}"
