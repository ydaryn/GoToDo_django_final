from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.projects.models import Project, ProjectMember

User = get_user_model()


class ProjectEndpointTests(APITestCase):
    projects_url = "/api/v1/projects/"

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="owner@example.com",
            password="StrongPassword123",
            full_name="Project Owner",
            role="developer",
        )
        self.second_user = User.objects.create_user(
            email="second@example.com",
            password="StrongPassword123",
            full_name="Second User",
            role="developer",
        )

        self.project = Project.objects.create(
            name="Existing Project",
            description="Existing project description",
            owner=self.user,
            status=Project.Status.ACTIVE,
        )
        ProjectMember.objects.create(
            project=self.project,
            user=self.user,
            role=ProjectMember.Role.OWNER,
        )

    def test_create_project_success(self) -> None:
        self.client.force_authenticate(user=self.user)

        payload = {
            "name": "New Project",
            "description": "New project description",
            "status": Project.Status.ACTIVE,
        }

        response = self.client.post(self.projects_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Project.objects.filter(name="New Project").exists())

        created_project = Project.objects.get(name="New Project")
        self.assertEqual(created_project.owner, self.user)
        self.assertTrue(
            ProjectMember.objects.filter(
                project=created_project,
                user=self.user,
                role=ProjectMember.Role.OWNER,
            ).exists()
        )

    def test_create_project_without_authentication_fails(self) -> None:
        payload = {
            "name": "Unauthorized Project",
            "description": "Should not be created",
            "status": Project.Status.ACTIVE,
        }

        response = self.client.post(self.projects_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(Project.objects.filter(name="Unauthorized Project").exists())

    def test_create_project_without_name_fails(self) -> None:
        self.client.force_authenticate(user=self.user)

        payload = {
            "description": "Project without name",
            "status": Project.Status.ACTIVE,
        }

        response = self.client.post(self.projects_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_projects_success(self) -> None:
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.projects_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_projects_without_authentication_fails(self) -> None:
        response = self.client.get(self.projects_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_projects_by_status_success(self) -> None:
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            self.projects_url,
            {"status": Project.Status.ACTIVE},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_project_success(self) -> None:
        self.client.force_authenticate(user=self.user)

        url = f"{self.projects_url}{self.project.id}/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.project.name)

    def test_retrieve_project_without_authentication_fails(self) -> None:
        url = f"{self.projects_url}{self.project.id}/"

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_not_existing_project_fails(self) -> None:
        self.client.force_authenticate(user=self.user)

        response = self.client.get(f"{self.projects_url}99999/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_project_success(self) -> None:
        self.client.force_authenticate(user=self.user)

        url = f"{self.projects_url}{self.project.id}/"
        payload = {
            "name": "Updated Project",
            "description": "Updated description",
            "status": Project.Status.COMPLETED,
        }

        response = self.client.patch(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.name, "Updated Project")
        self.assertEqual(self.project.status, Project.Status.COMPLETED)

    def test_update_project_without_authentication_fails(self) -> None:
        url = f"{self.projects_url}{self.project.id}/"
        payload = {
            "name": "Should Not Update",
        }

        response = self.client.patch(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_project_with_invalid_status_fails(self) -> None:
        self.client.force_authenticate(user=self.user)

        url = f"{self.projects_url}{self.project.id}/"
        payload = {
            "status": "invalid_status",
        }

        response = self.client.patch(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_project_success(self) -> None:
        self.client.force_authenticate(user=self.user)

        url = f"{self.projects_url}{self.project.id}/"
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Project.objects.filter(id=self.project.id).exists())

    def test_delete_project_without_authentication_fails(self) -> None:
        url = f"{self.projects_url}{self.project.id}/"

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Project.objects.filter(id=self.project.id).exists())

    def test_project_members_list_success(self) -> None:
        self.client.force_authenticate(user=self.user)

        response = self.client.get(f"{self.projects_url}members/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_project_members_list_without_authentication_fails(self) -> None:
        response = self.client.get(f"{self.projects_url}members/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)