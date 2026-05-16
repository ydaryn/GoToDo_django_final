from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.agile.models import Epic, Sprint, SubTask, Task
from apps.projects.models import Project, ProjectMember, Tag

User = get_user_model()


class AgileEndpointTests(APITestCase):
    epics_url = "/api/v1/agile/epics/"
    sprints_url = "/api/v1/agile/sprints/"
    tasks_url = "/api/v1/agile/tasks/"
    subtasks_url = "/api/v1/agile/subtasks/"

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="developer@example.com",
            password="StrongPassword123",
            full_name="Developer User",
            role="developer",
        )
        self.second_user = User.objects.create_user(
            email="second@example.com",
            password="StrongPassword123",
            full_name="Second User",
            role="developer",
        )

        self.project = Project.objects.create(
            name="Test Project",
            description="Project for agile endpoint tests",
            owner=self.user,
            status=Project.Status.ACTIVE,
        )
        ProjectMember.objects.create(
            project=self.project,
            user=self.user,
            role=ProjectMember.Role.OWNER,
        )

        self.epic = Epic.objects.create(
            project=self.project,
            owner=self.user,
            title="Existing Epic",
            description="Existing epic description",
            status=Epic.Status.OPEN,
        )

        self.sprint = Sprint.objects.create(
            project=self.project,
            name="Sprint 1",
            goal="Finish core API",
            status=Sprint.Status.PLANNED,
        )

        self.tag = Tag.objects.create(
            project=self.project,
            name="backend",
            color="#6366f1",
        )

        self.task = Task.objects.create(
            project=self.project,
            sprint=self.sprint,
            epic=self.epic,
            title="Existing Task",
            description="Existing task description",
            assignee=self.user,
            reporter=self.user,
            status=Task.Status.TODO,
            priority=Task.Priority.MEDIUM,
            story_points=3,
        )
        self.task.tags.add(self.tag)

        self.subtask = SubTask.objects.create(
            task=self.task,
            title="Existing SubTask",
            description="Existing subtask description",
            assignee=self.user,
            status=SubTask.Status.TODO,
            order=1,
        )

    # ------------------------------------------------------------------
    # Epic endpoint tests
    # ------------------------------------------------------------------

    def test_create_epic_success(self) -> None:
        self.client.force_authenticate(user=self.user)

        payload = {
            "project": self.project.id,
            "owner": self.user.id,
            "title": "New Epic",
            "description": "New epic description",
            "status": Epic.Status.OPEN,
        }

        response = self.client.post(self.epics_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Epic.objects.filter(title="New Epic").exists())

    def test_create_epic_without_authentication_fails(self) -> None:
        payload = {
            "project": self.project.id,
            "owner": self.user.id,
            "title": "Unauthorized Epic",
            "description": "Should not be created",
            "status": Epic.Status.OPEN,
        }

        response = self.client.post(self.epics_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_epic_without_title_fails(self) -> None:
        self.client.force_authenticate(user=self.user)

        payload = {
            "project": self.project.id,
            "owner": self.user.id,
            "description": "Epic without title",
            "status": Epic.Status.OPEN,
        }

        response = self.client.post(self.epics_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_epics_success(self) -> None:
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.epics_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_epic_success(self) -> None:
        self.client.force_authenticate(user=self.user)

        response = self.client.get(f"{self.epics_url}{self.epic.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.epic.title)

    # ------------------------------------------------------------------
    # Sprint endpoint tests
    # ------------------------------------------------------------------

    def test_create_sprint_success(self) -> None:
        self.client.force_authenticate(user=self.user)

        payload = {
            "project": self.project.id,
            "name": "Sprint 2",
            "goal": "Add tests",
            "status": Sprint.Status.PLANNED,
        }

        response = self.client.post(self.sprints_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Sprint.objects.filter(name="Sprint 2").exists())

    def test_create_sprint_without_authentication_fails(self) -> None:
        payload = {
            "project": self.project.id,
            "name": "Unauthorized Sprint",
            "goal": "Should not be created",
            "status": Sprint.Status.PLANNED,
        }

        response = self.client.post(self.sprints_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_sprint_without_name_fails(self) -> None:
        self.client.force_authenticate(user=self.user)

        payload = {
            "project": self.project.id,
            "goal": "Sprint without name",
            "status": Sprint.Status.PLANNED,
        }

        response = self.client.post(self.sprints_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_sprints_success(self) -> None:
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.sprints_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_sprint_success(self) -> None:
        self.client.force_authenticate(user=self.user)

        response = self.client.get(f"{self.sprints_url}{self.sprint.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.sprint.name)

    # ------------------------------------------------------------------
    # Task endpoint tests
    # ------------------------------------------------------------------

    def test_create_task_success(self) -> None:
        self.client.force_authenticate(user=self.user)

        payload = {
            "project": self.project.id,
            "sprint": self.sprint.id,
            "epic": self.epic.id,
            "title": "New Task",
            "description": "New task description",
            "assignee": self.user.id,
            "reporter": self.user.id,
            "status": Task.Status.TODO,
            "priority": Task.Priority.HIGH,
            "story_points": 5,
            "tags": [self.tag.id],
        }

        response = self.client.post(self.tasks_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Task.objects.filter(title="New Task").exists())

    def test_create_task_without_authentication_fails(self) -> None:
        payload = {
            "project": self.project.id,
            "sprint": self.sprint.id,
            "epic": self.epic.id,
            "title": "Unauthorized Task",
            "description": "Should not be created",
            "assignee": self.user.id,
            "reporter": self.user.id,
            "status": Task.Status.TODO,
            "priority": Task.Priority.HIGH,
        }

        response = self.client.post(self.tasks_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_task_without_title_fails(self) -> None:
        self.client.force_authenticate(user=self.user)

        payload = {
            "project": self.project.id,
            "sprint": self.sprint.id,
            "epic": self.epic.id,
            "description": "Task without title",
            "assignee": self.user.id,
            "reporter": self.user.id,
            "status": Task.Status.TODO,
            "priority": Task.Priority.HIGH,
        }

        response = self.client.post(self.tasks_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_tasks_success(self) -> None:
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.tasks_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_tasks_by_status_success(self) -> None:
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            self.tasks_url,
            {"status": Task.Status.TODO},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_tasks_success(self) -> None:
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            self.tasks_url,
            {"search": "Existing"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_task_success(self) -> None:
        self.client.force_authenticate(user=self.user)

        response = self.client.get(f"{self.tasks_url}{self.task.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.task.title)

    def test_update_task_success(self) -> None:
        self.client.force_authenticate(user=self.user)

        payload = {
            "status": Task.Status.IN_PROGRESS,
            "priority": Task.Priority.CRITICAL,
        }

        response = self.client.patch(
            f"{self.tasks_url}{self.task.id}/",
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, Task.Status.IN_PROGRESS)
        self.assertEqual(self.task.priority, Task.Priority.CRITICAL)

    def test_update_task_with_invalid_status_fails(self) -> None:
        self.client.force_authenticate(user=self.user)

        payload = {
            "status": "invalid_status",
        }

        response = self.client.patch(
            f"{self.tasks_url}{self.task.id}/",
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_task_success(self) -> None:
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(f"{self.tasks_url}{self.task.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    # ------------------------------------------------------------------
    # SubTask endpoint tests
    # ------------------------------------------------------------------

    def test_create_subtask_success(self) -> None:
        self.client.force_authenticate(user=self.user)

        payload = {
            "task": self.task.id,
            "title": "New SubTask",
            "description": "New subtask description",
            "assignee": self.user.id,
            "status": SubTask.Status.TODO,
            "order": 2,
        }

        response = self.client.post(self.subtasks_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(SubTask.objects.filter(title="New SubTask").exists())

    def test_create_subtask_without_authentication_fails(self) -> None:
        payload = {
            "task": self.task.id,
            "title": "Unauthorized SubTask",
            "description": "Should not be created",
            "assignee": self.user.id,
            "status": SubTask.Status.TODO,
            "order": 2,
        }

        response = self.client.post(self.subtasks_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_subtask_without_title_fails(self) -> None:
        self.client.force_authenticate(user=self.user)

        payload = {
            "task": self.task.id,
            "description": "SubTask without title",
            "assignee": self.user.id,
            "status": SubTask.Status.TODO,
            "order": 2,
        }

        response = self.client.post(self.subtasks_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_subtasks_success(self) -> None:
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.subtasks_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_subtask_success(self) -> None:
        self.client.force_authenticate(user=self.user)

        response = self.client.get(f"{self.subtasks_url}{self.subtask.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.subtask.title)