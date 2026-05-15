# your_app/management/commands/seed_demo_data.py

import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from faker import Faker

from your_app.models import (
    User,
    Project,
    ProjectMember,
    Sprint,
    Epic,
    Task,
    SubTask,
    Comment,
    Tag,
    Notification,
    ActivityLog,
)


fake = Faker()


class Command(BaseCommand):
    help = "Fill database with demo data"

    USER_COUNT = 12
    PROJECT_COUNT = 4
    TASKS_PER_PROJECT = 20

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete existing demo data before seeding",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["flush"]:
            self.stdout.write(self.style.WARNING("Deleting old data..."))

            Notification.objects.all().delete()
            ActivityLog.objects.all().delete()
            Comment.objects.all().delete()
            SubTask.objects.all().delete()
            Task.objects.all().delete()
            Sprint.objects.all().delete()
            Epic.objects.all().delete()
            Tag.objects.all().delete()
            ProjectMember.objects.all().delete()
            Project.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()

        self.stdout.write(self.style.NOTICE("Creating demo data..."))

        users = self.create_users()
        projects = self.create_projects(users)

        for project in projects:
            tags = self.create_tags(project)
            epics = self.create_epics(project, users)
            sprints = self.create_sprints(project)
            tasks = self.create_tasks(
                project=project,
                users=users,
                tags=tags,
                epics=epics,
                sprints=sprints,
            )

            self.create_subtasks(tasks, users)
            comments = self.create_comments(tasks, users)
            self.create_notifications(users, tasks, comments)
            self.create_activity_logs(project, users, tasks)

        self.stdout.write(
            self.style.SUCCESS("Demo database successfully created.")
        )

    # ------------------------------------------------------------------
    # USERS
    # ------------------------------------------------------------------

    def create_users(self):
        users = []

        for i in range(self.USER_COUNT):
            username = f"user{i+1}"

            user, _ = User.objects.get_or_create(
                email=f"{username}@example.com",
                defaults={
                    "username": username,
                    "first_name": fake.first_name(),
                    "last_name": fake.last_name(),
                    "bio": fake.text(max_nb_chars=120),
                    "is_active": True,
                },
            )

            user.set_password("password123")
            user.save()

            users.append(user)

        self.stdout.write(self.style.SUCCESS(f"Created {len(users)} users"))
        return users

    # ------------------------------------------------------------------
    # PROJECTS
    # ------------------------------------------------------------------

    def create_projects(self, users):
        projects = []

        statuses = [
            Project.Status.ACTIVE,
            Project.Status.COMPLETED,
            Project.Status.ARCHIVED,
        ]

        for i in range(self.PROJECT_COUNT):
            owner = random.choice(users)

            project = Project.objects.create(
                name=f"Project {i+1}",
                description=fake.text(max_nb_chars=300),
                owner=owner,
                status=random.choice(statuses),
            )

            # owner membership
            ProjectMember.objects.create(
                project=project,
                user=owner,
                role=ProjectMember.Role.OWNER,
            )

            # random members
            members = random.sample(users, random.randint(4, 8))

            for member in members:
                ProjectMember.objects.get_or_create(
                    project=project,
                    user=member,
                    defaults={
                        "role": random.choice(
                            [
                                ProjectMember.Role.ADMIN,
                                ProjectMember.Role.MEMBER,
                                ProjectMember.Role.VIEWER,
                            ]
                        )
                    },
                )

            projects.append(project)

        self.stdout.write(self.style.SUCCESS(f"Created {len(projects)} projects"))
        return projects

    # ------------------------------------------------------------------
    # TAGS
    # ------------------------------------------------------------------

    def create_tags(self, project):
        tag_names = [
            "backend",
            "frontend",
            "bug",
            "feature",
            "urgent",
            "api",
            "design",
            "testing",
        ]

        colors = [
            "#ef4444",
            "#22c55e",
            "#3b82f6",
            "#eab308",
            "#8b5cf6",
            "#14b8a6",
            "#f97316",
            "#6366f1",
        ]

        tags = []

        for name in tag_names:
            tag = Tag.objects.create(
                project=project,
                name=name,
                color=random.choice(colors),
            )
            tags.append(tag)

        return tags

    # ------------------------------------------------------------------
    # EPICS
    # ------------------------------------------------------------------

    def create_epics(self, project, users):
        epics = []

        for i in range(5):
            start = timezone.now().date() - timedelta(days=random.randint(1, 30))

            epic = Epic.objects.create(
                project=project,
                owner=random.choice(users),
                title=f"Epic {i+1} - {fake.bs().title()}",
                description=fake.text(max_nb_chars=250),
                status=random.choice(Epic.Status.values),
                start_date=start,
                end_date=start + timedelta(days=random.randint(7, 45)),
            )

            epics.append(epic)

        return epics

    # ------------------------------------------------------------------
    # SPRINTS
    # ------------------------------------------------------------------

    def create_sprints(self, project):
        sprints = []

        for i in range(4):
            start = timezone.now().date() - timedelta(days=(i * 14))

            sprint = Sprint.objects.create(
                project=project,
                name=f"Sprint {i+1}",
                goal=fake.sentence(),
                status=random.choice(Sprint.Status.values),
                start_date=start,
                end_date=start + timedelta(days=14),
            )

            sprints.append(sprint)

        return sprints

    # ------------------------------------------------------------------
    # TASKS
    # ------------------------------------------------------------------

    def create_tasks(self, project, users, tags, epics, sprints):
        tasks = []

        for i in range(self.TASKS_PER_PROJECT):
            reporter = random.choice(users)
            assignee = random.choice(users)

            due_date = timezone.now().date() + timedelta(
                days=random.randint(1, 60)
            )

            task = Task.objects.create(
                project=project,
                sprint=random.choice(sprints),
                epic=random.choice(epics),
                title=fake.sentence(nb_words=6),
                description=fake.text(max_nb_chars=500),
                assignee=assignee,
                reporter=reporter,
                status=random.choice(Task.Status.values),
                priority=random.choice(Task.Priority.values),
                story_points=random.randint(1, 13),
                due_date=due_date,
            )

            selected_tags = random.sample(tags, random.randint(1, 4))
            task.tags.set(selected_tags)

            tasks.append(task)

        self.stdout.write(
            self.style.SUCCESS(
                f"Created {len(tasks)} tasks for {project.name}"
            )
        )

        return tasks

    # ------------------------------------------------------------------
    # SUBTASKS
    # ------------------------------------------------------------------

    def create_subtasks(self, tasks, users):
        created = 0

        for task in tasks:
            for order in range(random.randint(1, 5)):
                SubTask.objects.create(
                    task=task,
                    title=fake.sentence(nb_words=4),
                    description=fake.text(max_nb_chars=120),
                    assignee=random.choice(users),
                    status=random.choice(SubTask.Status.values),
                    due_date=task.due_date,
                    order=order,
                )
                created += 1

        self.stdout.write(self.style.SUCCESS(f"Created {created} subtasks"))

    # ------------------------------------------------------------------
    # COMMENTS
    # ------------------------------------------------------------------

    def create_comments(self, tasks, users):
        comments = []

        for task in tasks:
            parent_comments = []

            for _ in range(random.randint(2, 6)):
                comment = Comment.objects.create(
                    task=task,
                    author=random.choice(users),
                    body=fake.paragraph(nb_sentences=3),
                    edited=random.choice([True, False]),
                )

                parent_comments.append(comment)
                comments.append(comment)

                # replies
                for _ in range(random.randint(0, 2)):
                    reply = Comment.objects.create(
                        task=task,
                        author=random.choice(users),
                        parent=comment,
                        body=fake.sentence(),
                    )

                    comments.append(reply)

        self.stdout.write(self.style.SUCCESS(f"Created {len(comments)} comments"))
        return comments

    # ------------------------------------------------------------------
    # NOTIFICATIONS
    # ------------------------------------------------------------------

    def create_notifications(self, users, tasks, comments):
        notifications = []

        for _ in range(60):
            task = random.choice(tasks)

            notification = Notification.objects.create(
                recipient=random.choice(users),
                actor=random.choice(users),
                verb=random.choice(Notification.Verb.values),
                entity_type=Notification.EntityType.TASK,
                entity_id=task.id,
                message=fake.sentence(),
                is_read=random.choice([True, False]),
            )

            notifications.append(notification)

        for _ in range(20):
            comment = random.choice(comments)

            notification = Notification.objects.create(
                recipient=random.choice(users),
                actor=random.choice(users),
                verb=Notification.Verb.COMMENTED,
                entity_type=Notification.EntityType.COMMENT,
                entity_id=comment.id,
                message="Someone replied to your comment",
                is_read=random.choice([True, False]),
            )

            notifications.append(notification)

        self.stdout.write(
            self.style.SUCCESS(
                f"Created {len(notifications)} notifications"
            )
        )

    # ------------------------------------------------------------------
    # ACTIVITY LOGS
    # ------------------------------------------------------------------

    def create_activity_logs(self, project, users, tasks):
        logs = []

        actions = [
            ActivityLog.Action.CREATED,
            ActivityLog.Action.UPDATED,
            ActivityLog.Action.STATUS_CHANGED,
            ActivityLog.Action.ASSIGNED,
            ActivityLog.Action.COMMENTED,
        ]

        for _ in range(80):
            task = random.choice(tasks)

            log = ActivityLog.objects.create(
                actor=random.choice(users),
                project=project,
                entity_type=ActivityLog.EntityType.TASK,
                entity_id=task.id,
                action=random.choice(actions),
                old_value={"status": "todo"},
                new_value={"status": task.status},
            )

            logs.append(log)

        self.stdout.write(
            self.style.SUCCESS(
                f"Created {len(logs)} activity logs"
            )
        )